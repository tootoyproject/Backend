from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import UsersJWSSignupSerializer
from django.http.response import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class JWTSignupView(APIView):
    serializer_class = UsersJWSSignupSerializer

    def post(self, request):
        serializer = self. serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            user = serializer.save(request)
            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)

            return JsonResponse({'user': user, 'access': access, 'refresh' : refresh})