from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import (render)
from .serializers import *
from users.lib.permission import LoginRequired

user_retrieve_response = openapi.Response('', UserInfoSerializer)

class Register(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'users/register.html')

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return JsonResponse({'message': '계정이 성공적으로 생성되었습니다.'}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)




class UserView(APIView):
    permission_classes = [AllowAny]

    def get_or_create_user(self, data: dict):
        serializer = CreateUserSerializer(data=data)


        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data
        serializer.create(validated_data=user)

        return Response(data=user, status=status.HTTP_201_CREATED)

    def post(self, request):
        '''
        계정 조회 및 등록

        ---
        '''
        return self.get_or_create_user(data=request.data)


class LoginView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        '''
        최초 로그인 화면을 렌더링합니다.
        '''
        return render(request, 'users/login.html')

    def object(self, data: dict):
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data

        return Response(data=user, status=status.HTTP_200_OK)

    # def post(self, request):
    #     '''
    #     로그인
    #
    #     ---
    #     '''
    #
    #     username = request.data.get('username')
    #     password = request.data.get('password')
    #
    #     if user is not None:
    #         login(request, user)
    #         return JsonResponse({'message': '로그인 성공'}, status=status.HTTP_200_OK)
    #     else:
    #         return JsonResponse({'message': '아이디 또는 비밀번호가 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [LoginRequired]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(request_body=LogoutSerializer)
    def post(self, request):
        '''
        로그아웃

        ---
        '''
        serializer = LogoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.validated_data.blacklist()
        logout(request)

        return Response({'message': '로그아웃이 성공적으로 처리되었습니다.'}, status=status.HTTP_200_OK)


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RefreshTokenSerializer)
    def post(self, request):
        '''
        Access Token 재발급

        ---
        '''
        serializer = RefreshTokenSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        token = serializer.validated_data

        return Response(data=token, status=status.HTTP_201_CREATED)


# class UserView(APIView):
#     '''
#     계정 정보
#     '''
#     @swagger_auto_schema(responses={200: user_retrieve_response})
#     def get(self, request):
#         '''
#         로그인한 계정 정보 조회
#
#         ---
#         사용자 계정 ID, 이메일, 가입일자, 최근 로그인 일자 조회
#         '''
#         serializer = UserInfoSerializer(request.user)
#         response_data = serializer.data
#
#         return Response(data=response_data, status=status.HTTP_200_OK)
#
#     @swagger_auto_schema(request_body=UserInfoPhoneSerializer, responses={200: ''})
#     def patch(self, request, *args, **kwargs):
#         '''
#         계정 정보 수정
#
#         ---
#         '''
#         data = request.data
#
#         serializer = UserInfoPhoneSerializer(request.user, data=data, partial=True)
#         if not serializer.is_valid():
#             return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         serializer.save()
#
#         return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        '''
        계정 삭제

        ---
        '''
        request.user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)