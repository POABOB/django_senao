from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.db import transaction
from user.serializers import AuthSerializer 
from user.models import User
from utils.throttle import VisitThrottle

from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
import json

# 登入、註冊的 ViewSet
class AuthViewSet(viewsets.ViewSet):

    throttle_classes = [VisitThrottle]

    @swagger_auto_schema(
        operation_summary='使用者註冊',
        operation_description='註冊請注意，密碼至少需要一個大寫字母、一個小寫字母和一個數字來組成。',
        tags=['Auth'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, minLength=3, maxLength=32, description='使用者名稱'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, minLength=8, maxLength=32, description='密碼')
            },
            required=['username', 'password']
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='操作狀態')},
                required=['success']
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='操作狀態'),
                    'reason': openapi.Schema(type=openapi.TYPE_STRING, description='原因描述')
                },
                required=['success', 'reason']
            )
        }
    )
    @action(detail=False, methods=['post'])
    def signup(self, request, pk=None):
        data = json.loads(request.body)
        
        # Validator
        serializer = AuthSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Cache get data
        if cache.get(data["username"]):
            print("cached")
            raise serializers.ValidationError("User already exists.")

        # Check user whether is duplicate
        exists_user = User.objects.filter(username=data["username"])
        if len(exists_user) > 0:
            raise serializers.ValidationError("User already exists.")

        # Encrypt
        user = User(username=data["username"], password=make_password(data["password"]))

        # Atomic
        # No user have same name
        with transaction.atomic():
            user.save()

        # Cahce set data
        cache.set(
            key=user.username,
            value=user.password,
            timeout=60 * 5,  # in seconds (300s or 5min)
        )

        return Response({}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='使用者登入',
        operation_description='登入請注意，如果輸入錯誤次數超過5次，將會被鎖定1分鐘。',
        tags=['Auth'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, minLength=3, maxLength=32, description='使用者名稱'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, minLength=8, maxLength=32, description='密碼')
            },
            required=['username', 'password']
        ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='操作狀態')},
                required=['success']
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='操作狀態'),
                    'reason': openapi.Schema(type=openapi.TYPE_STRING, description='原因描述')
                },
                required=['success', 'reason']
            ),
        }
    )
    @action(detail=False, methods=['post'])
    def login(self, request, pk=None):
        data = json.loads(request.body)

        # Validator
        serializer = AuthSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Cache get username if he/she input incorrect password over 5 times in 1 minutes.
        times = cache.get(data["username"] + "_times")
        self.block_if_too_many_times(times)

        # Cache
        passwaord = cache.get(data["username"])
        if passwaord is None:
            print("no cached")
            # Filter
            exists_user = User.objects.filter(username=data["username"])
            # User is not existed.
            if len(exists_user) == 0:
                # Cache will count the error times
                times = self.check_password_error_times(times, data)
                raise serializers.ValidationError("Incorrect Username or Password.")
            
            passwaord = exists_user[0].password
            cache.set(
                key=data["username"],
                value=passwaord,
                timeout=60 * 5,  # in seconds (5min)
            )

        # User is existed, but password is incorrect.
        if not check_password(data["password"], passwaord):
            # Cache will count the error times
            times = self.check_password_error_times(times, data)
            raise serializers.ValidationError("Incorrect Username or Password.")

        return Response({}, status=status.HTTP_200_OK)
    
    # Count the error times
    def check_password_error_times(self, times, data):
        if times is None:
            times = 1
        else:
            times = times + 1
        
        cache.set(
            key=data["username"]+"_times",
            value=times,
            timeout=60 * 1,  # in seconds (1min)
        )
        self.block_if_too_many_times(times)

    # Block
    def block_if_too_many_times(self, times):
        if times is not None and times >= 5:
            raise serializers.ValidationError("Failed too many times, please wait one minute.")
