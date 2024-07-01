import jwt
import time
import requests

from django.conf import settings
from django.shortcuts import redirect
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


from .serializers import *
from users.models import UserModel
from users.views import LoginView, UserView

def login_api(social_type: str, social_id: str, email: str=None, phone: str=None):
    '''
    회원가입 및 로그인
    '''
    login_view = LoginView()
    try:
        UserModel.objects.get(social_id=social_id)
        data = {
            'social_id': social_id,
            'email': email,
        }
        response = login_view.object(data=data)

    except UserModel.DoesNotExist:
        data = {
            'social_type': social_type,
            'social_id': social_id,
            'email': email,
        }
        user_view = UserView()
        login = user_view.get_or_create_user(data=data)

        response = login_view.object(data=data) if login.status_code == 201 else login

    return response


# Kakao
kakao_login_uri = "https://kauth.kakao.com/oauth/authorize"
kakao_token_uri = "https://kauth.kakao.com/oauth/token"
kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"


class KakaoLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        client_id = settings.KAKAO_REST_API_KEY
        redirect_uri = settings.KAKAO_REDIRECT_URI
        uri = f"{kakao_login_uri}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"

        return redirect(uri)


class KakaoCallbackView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(query_serializer=CallbackUserInfoSerializer)
    def get(self, request):
        data = request.query_params
        code = data.get('code')
        if not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        request_data = {
            'grant_type': 'authorization_code',
            'client_id': settings.KAKAO_REST_API_KEY,
            'redirect_uri': settings.KAKAO_REDIRECT_URI,
            'client_secret': settings.KAKAO_CLIENT_SECRET_KEY,
            'code': code,
        }
        token_headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        token_res = requests.post(kakao_token_uri, data=request_data, headers=token_headers)

        token_json = token_res.json()
        access_token = token_json.get('access_token')

        if not access_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        access_token = f"Bearer {access_token}"

        auth_headers = {
            "Authorization": access_token,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        user_info_res = requests.get(kakao_profile_uri, headers=auth_headers)
        user_info_json = user_info_res.json()

        social_type = 'kakao'
        social_id = f"{social_type}_{user_info_json.get('id')}"

        kakao_account = user_info_json.get('kakao_account')
        if not kakao_account:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_email = kakao_account.get('email')

        res = login_api(social_type=social_type, social_id=social_id, email=user_email)
        return res


# Naver
naver_login_url = "https://nid.naver.com/oauth2.0/authorize"
naver_token_url = "https://nid.naver.com/oauth2.0/token"
naver_profile_url = "https://openapi.naver.com/v1/nid/me"


class NaverLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        client_id = settings.NAVER_CLIENT_ID
        redirect_uri = settings.NAVER_REDIRECT_URI
        state = settings.STATE

        uri = f"{naver_login_url}?client_id={client_id}&redirect_uri={redirect_uri}&state={state}&response_type=code"

        return redirect(uri)


class NaverCallbackView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(query_serializer=CallbackUserCSRFInfoSerializer)
    def get(self, request):
        data = request.query_params
        code = data.get('code')
        user_state = data.get('state')
        if (not code) or (user_state != settings.STATE):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        request_data = {
            'grant_type': 'authorization_code',
            'client_id': settings.NAVER_CLIENT_ID,
            'client_secret': settings.NAVER_CLIENT_SECRET,
            'code': code,
            'state': user_state,
        }
        token_headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        token_res = requests.post(naver_token_url, data=request_data, headers=token_headers)

        token_json = token_res.json()
        access_token = token_json.get('access_token')

        if not access_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        access_token = f"Bearer {access_token}"

        auth_headers = {
            "X-naver-Client-Id": settings.NAVER_CLIENT_ID,
            "X-naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
            "Authorization": access_token,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        user_info_res = requests.get(naver_profile_url, headers=auth_headers)
        user_info_json = user_info_res.json()

        social_type = 'naver'
        social_id = f"{social_type}_{user_info_json.get('id')}"
        user_email = user_info_json.get('email')

        res = login_api(social_type=social_type, social_id=social_id, email=user_email)
        return res


# Google
google_login_url = "https://accounts.google.com/o/oauth2/v2/auth"
google_scope = "https://www.googleapis.com/auth/userinfo.email"
google_token_url = "https://oauth2.googleapis.com/token"
google_profile_url = "https://www.googleapis.com/oauth2/v2/tokeninfo"


class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        client_id = settings.GOOGLE_CLIENT_ID
        redirect_uri = settings.GOOGLE_REDIRECT_URI
        uri = f"{google_login_url}?client_id={client_id}&redirect_uri={redirect_uri}&scope={google_scope}&response_type=code"

        return redirect(uri)


class GoogleCallbackView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(query_serializer=CallbackUserInfoSerializer)
    def get(self, request):
        data = request.query_params
        code = data.get('code')
        if not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        request_data = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        }
        token_res = requests.post(google_token_url, data=request_data)

        token_json = token_res.json()
        access_token = token_json['access_token']

        if not access_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        query_string = {
            'access_token': access_token
        }
        user_info_res = requests.get(google_profile_url, params=query_string)
        user_info_json = user_info_res.json()

        social_type = 'google'
        social_id = f"{social_type}_{user_info_json.get('user_id')}"
        user_email = user_info_json.get('email')

        res = login_api(social_type=social_type, social_id=social_id, email=user_email)
        return res
