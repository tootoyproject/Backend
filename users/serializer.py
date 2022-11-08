from rest_framework import serializers
from .models import Users
from rest_framework_simplejwt.tokens import RefreshToken

class UsersJWSSignupSerializer(serializers.ModelSerializer) :
    username = serializers.CharField(
        required = True,
        write_only=True,
        max_length=20
    )

    pw = serializers.CharField(
        required = True,
        write_only=True,
        style={'input_type' : 'password'}
    )

    class Meta(object):
        model = Users
        fields = ['username', 'pw']
    
    def save(self, request):
        user = super().save()
        user.username = self.validated_data['username']
        user.set_password(self.validated_data['pw'])
        user.save
        return user

    def validate(self, data):
        username = data.get('username', None)
        if Users.objects.filter(id=username).exists():
            raise serializers.ValidationError("있는 계정")
        return data

class UsersLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required = True,
        write_only=True,
        max_length=20
    )

    pw = serializers.CharField(
        required = True,
        write_only=True,
        style={'input_type' : 'password'}
    )
    class Meta(object):
        model = Users
        fields = ['username','pw']
    
    def create(self, validated_date):
        pass

    def update(self, validated_date):
        pass

    def validate(self, data):
        username = data.get('username', None)
        pw = data.get('pw', None)
        
        if Users.objects.filter(id=username).exists():
            user = Users.objects.get(id=username)

            if not user.check_password(pw):
                raise serializers.ValidationError("틀린 비밀번호")
        else:
            raise serializers.ValidationError("계정이 없습니다")
        
        token = RefreshToken.for_user(user)
        refresh = str(token)
        access = str(token.access_token)

        data = {
            'user' : user,
            'access' : access,
            'refresh' : refresh,
        }

        return data