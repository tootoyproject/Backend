from rest_framework import serializers
from .models import Users
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken

# Signup
Users = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=True, write_only=True, max_length=20)
    password = serializers.CharField(required=True, write_only=True,style= {'input_type':'password'})

    class Meta(object):
        model = Users
        fields = ['id', 'password']

    def save(self, request):
        user = super().save()
        user.id = self.validated_data['id']
        user.set_password(self.validated_data['password'])
        user.save()
        return user
    def validate(self, data):
        id = data.get('id', None)

        if Users.objects.filter(id=id).exists():
            raise serializers.ValidationError({"msg": "이미 존재하는 계정입니다."})

        return data
# Login

class UserLoginSerializer(serializers.Serializer):
    id = serializers.CharField(required=True, write_only=True, max_length=20)
    password = serializers.CharField(required=True, write_only=True,style= {'input_type':'password'})

    class Meta(object):
        model = Users
        fields = ['id', 'password']

    def validate(self, data):
        id = data.get("id", None)
        password = data.get("password", None)

        if Users.objects.filter(id=id).exists():
            user = Users.objects.get(id=id)
            if not user.check_password(password):
                raise serializers.ValidationError({"msg":"틀린 비밀번호입니다."})
        else:
            raise serializers.ValidationError({"msg":"계정이 존재하지 않습니다."})
        
        token = RefreshToken.for_user(user)
        refresh = str(token)
        access = str(token.access_token)

        data = {
            'user' : str(user),
            'refresh' : refresh,
            'access' : access
        }
        return data