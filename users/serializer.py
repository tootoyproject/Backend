from rest_framework import serializers
from .models import Users
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login

# Signup
Users = get_user_model()

class UserCreateSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    def create(self, validated_data):
        user = Users.objects.create( # User 생성
            id=validated_data['id'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# Login

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserLoginSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        id = data.get("id", None)
        password = data.get("password", None)
        user = authenticate(id=id, password=password)

        if user is None:
            return {
                'id': 'None'
            }
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload) # 토큰 발행
            update_last_login(None, user)
        except Users.DoesNotExist:
            raise serializers.ValidationError(
                'User with given id and password does not exists'
            )
        return {
            'id': user.id,
            'token': jwt_token
            }