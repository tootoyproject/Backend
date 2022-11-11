from .serializer import UserCreateSerializer, UserLoginSerializer
from django.http.response import JsonResponse
from django.db import IntegrityError
from rest_framework.views import APIView, Response
from rest_framework import status

# Create your views here.

class UserCreateView(APIView):
    def post(self, request):
        try:
            serializer = UserCreateSerializer(data=request.data) 
            if serializer.is_valid(raise_exception=True):
                serializer.save() # DB 저장
                return Response({"msg":"회원가입에 성공하셨습니다.","status" : 200}, status=201)
        except IntegrityError:
            return Response({"msg" : "회원가입에 실패하셨습니다", "status" : 400})

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response({"msg": "로그인에 실패했습니다.","status" : 400}, status=status.HTTP_409_CONFLICT)
        if serializer.validated_data["id"] == "None": # username required
            return Response({"msg": "로그인에 실패했습니다.(아이디가 없거나 비밀번호가 틀림)","status" : 400}, status=status.HTTP_200_OK)

        response = {
            "status": 200,
            "msg" : "로그인에 성공하셨습니다.",
            "accessToken": serializer.data["token"] # 시리얼라이저에서 받은 토큰 전달
        }
        return Response(response, status=status.HTTP_200_OK)