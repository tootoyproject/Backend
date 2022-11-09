from rest_framework import serializers
from .models import Users
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

# Signup
class JWTSignupSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        required=True,
        write_only=True,
        max_length=20
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    

    subscription_date = serializers.DateField(
        required=False,
        write_only=True,
    )

    class Meta(object):
        model = Users
        fields = ['id', 'password', 'subscription_date']

    def save(self, request):
        user = super().save()

        user.id = self.validated_data['id']
        user.subscription_date = self.validated_data['subscription_date']

        user.set_password(self.validated_data['password'])
        user.save()

        return user

    def validate(self, data):
        id = data.get('id', None)

        if Users.objects.filter(id=id).exists():
            raise serializers.ValidationError("user already exists")

        data['subscription_date'] = timezone.now()

        return data

# Login

class JWTLoginSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        required=True,
        write_only=True,
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    class Meta(object):
        model = Users
        fields = ['phone', 'password']
    
    def validate(self, data):
        id = data.get('id', None)
        password = data.get('password', None)

        if Users.objects.filter(id=id).exists():
            user = Users.objects.get(id=id)

            if not user.check_password(password):
                raise serializers.ValidationError("wrong password")
        else:
            raise serializers.ValidationError("user account not exist")
        
        token = RefreshToken.for_user(user)
        refresh = str(token)
        access = str(token.access_token)

        data = {
            'user': user,
            'refresh': refresh,
            'access': access,
        }

        return data