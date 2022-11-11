from rest_framework import serializers
from .models import Users
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login

# Signup
Users = get_user_model()

class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    def create(self, validated_data):
        user = Users.objects.create( # User 생성
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# Login

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)

        if user is None:
            return {
                'username': 'None'
            }
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload) # 토큰 발행
            update_last_login(None, user)
        except Users.DoesNotExist:
            raise serializers.ValidationError(
                'User with given username and password does not exists'
            )
        return {
            'username': user.username,
            'token': jwt_token
            }