from user.models import User
from rest_framework import serializers
import re

# Auth 的序列化與反序列化 class
class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    password_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')
    
    def validate(self, attrs):
        if len(attrs["username"]) < 3 or len(attrs["username"]) > 32:
            raise serializers.ValidationError("username field must be the length of 3~32.")   
        
        if len(attrs["password"]) < 8 or len(attrs["password"]) > 32:
            raise serializers.ValidationError("password field must be the length of 8~32.")   
        
        if not bool(self.password_pattern.match(attrs["password"])):
            raise serializers.ValidationError("password field must contain at least 1 uppercase letter, 1 lowercase letter, and 1 number.")   
        return attrs