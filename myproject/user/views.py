from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.db import transaction
from user.serializers import AuthSerializer 
from user.models import User

from django.contrib.auth.hashers import make_password, check_password
import json

# 登入、註冊的 ViewSet
class AuthViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_summary='使用者註冊',
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

        # Check user whether is duplicate
        exists_user = User.objects.filter(username=data["username"])
        if len(exists_user) > 0:
            raise serializers.ValidationError("User already exists.")
        
        # TODO Redis count user mistakes in a specific time.


        # Encrypt
        user = User(username=data["username"], password=make_password(data["password"]))

        # Atomic
        # No user have same name
        with transaction.atomic():
            user.save()
        return Response({}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='使用者登入',
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

        # Filter
        exists_user = User.objects.filter(username=data["username"])
        if len(exists_user) == 0:
            raise serializers.ValidationError("Incorrect Username or Password.")
        if not check_password(data["password"], exists_user[0].password):
            raise serializers.ValidationError("Incorrect Username or Password.")

        return Response({}, status=status.HTTP_200_OK)

