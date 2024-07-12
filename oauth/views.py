import requests
import jwt
import time
import random
import string

from django.conf import settings
from django.shortcuts import redirect
from django.middleware.csrf import get_token
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from users.models import UserModel
from users.views import LoginView, UserView
from rest_framework.exceptions import APIException


def login_api(social_type: str, social_id: str, email: str = None, phone: str = None):
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


kakao_login_uri = "https://kauth.kakao.com/oauth/authorize"
kakao_token_uri = "https://kauth.kakao.com/oauth/token"
kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"

class KakaoLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        '''
        kakao code 요청
        '''
        client_id = settings.KAKAO_REST_API_KEY
        redirect_uri = settings.KAKAO_REDIRECT_URI
        uri = f"{kakao_login_uri}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"


        return redirect(uri)


class KakaoCallbackView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(query_serializer=CallbackUserInfoSerializer)
    def get(self, request):
        '''
        kakao access_token 및 user_info 요청
        '''
        data = request.query_params

        # access_token 발급 요청
        code = data.get('code')
        if not code:
            print("No code parameter found")
            return Response({"error": "No code parameter found"}, status=status.HTTP_400_BAD_REQUEST)

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
        token_req = requests.post(kakao_token_uri, data=request_data, headers=token_headers)

        if token_req.status_code != 200:
            print("Failed to get access token:", token_req.status_code, token_req.text)
            return Response({"error": "Failed to get access token"}, status=token_req.status_code)

        token_json = token_req.json()
        access_token = token_json.get('access_token')

        if not access_token:
            print("Access token not found in the response")
            return Response({"error": "Access token not found in the response"}, status=status.HTTP_400_BAD_REQUEST)

        profile_request = requests.get(
            kakao_profile_uri,
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if profile_request.status_code != 200:
            print("Failed to get user profile:", profile_request.status_code, profile_request.text)
            return Response({"error": "Failed to get user profile"}, status=profile_request.status_code)

        user_info_json = profile_request.json()
        print("User info json:", user_info_json)

        # 이메일 정보 가져오기
        kakao_account = user_info_json.get('kakao_account')
        if not kakao_account or 'email' not in kakao_account:
            print("Kakao email does not contain email information")
            return Response({"error": "kakao email does not contain email information"},
                            status=status.HTTP_400_BAD_REQUEST)

        user_email = kakao_account.get('email')
        print("Kakao account info:", kakao_account)

        # 회원가입 및 로그인 처리
        res = login_api(social_type='kakao', social_id=f"kakao_{user_info_json.get('id')}", email=user_email)

        if res.status_code == 200:
            print("Login or registration successful")
            return redirect('http://127.0.0.1:8000/')
        else:
            print("Failed to process login or registration:", res.status_code, res.text)
            return Response({"message": "Failed to process login or registration."}, status=status.HTTP_400_BAD_REQUEST)


naver_login_url = "https://nid.naver.com/oauth2.0/authorize"
naver_token_url = "https://nid.naver.com/oauth2.0/token"
naver_profile_url = "https://openapi.naver.com/v1/nid/me"

def generate_state():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))


class NaverLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        '''
        naver code 요청

        ---
        '''

        client_id = settings.NAVER_CLIENT_ID
        redirect_uri = settings.NAVER_REDIRECT_URI
        state = generate_state()
        print(state)

        uri = f"{naver_login_url}?client_id={client_id}&redirect_uri={redirect_uri}&state={state}&response_type=code"
        res = redirect(uri)
        return res


class NaverCallbackView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(query_serializer=CallbackUserCSRFInfoSerializer)
    def get(self, request):
        '''
        naver access_token 및 user_info 요청

        ---
        '''
        data = request.query_params

        # access_token 발급 요청
        code = data.get('code')
        user_state = data.get('state')
        if (not code) or (user_state != user_state):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        request_data = {
            'grant_type': 'authorization_code',
            'client_id': settings.NAVER_CLIENT_ID,
            'redirect_uri': settings.NAVER_REDIRECT_URI,
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



        # naver 회원정보 요청
        auth_headers = {
            "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
            "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
            "Authorization": access_token,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        user_info_res = requests.get(naver_profile_url, headers=auth_headers)
        user_info_json = user_info_res.json()
        user_info_res.raise_for_status()

        # 이메일 정보 가져오기
        naver_account = user_info_json.get('response')
        if not naver_account or 'email' not in naver_account:
            return Response({"error": "naver email does not contain email information"})

        user_email = naver_account.get('email')

        # 회원가입 및 로그인
        res = login_api(social_type='naver', social_id=f"naver_{user_info_json.get('response').get('id')}", email=user_email)
        if res.status_code == 200:
            return redirect('http://127.0.0.1:8000/users/register/')
        else:
            return Response({"message": "Failed to process login or registration."},
                            status=status.HTTP_400_BAD_REQUEST)


google_login_url = "https://accounts.google.com/o/oauth2/v2/auth"
google_scope = "https://www.googleapis.com/auth/userinfo.email"
google_token_url = "https://oauth2.googleapis.com/token"
google_profile_url = "https://www.googleapis.com/oauth2/v2/tokeninfo"


class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        '''
        google code 요청

        ---
        '''
        client_id = settings.GOOGLE_CLIENT_ID
        redirect_uri = settings.GOOGLE_REDIRECT_URI
        uri = f"{google_login_url}?client_id={client_id}&redirect_uri={redirect_uri}&scope={google_scope}&response_type=code"

        res = redirect(uri)
        return res


class GoogleCallbackView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(query_serializer=CallbackUserInfoSerializer)
    def get(self, request):
        '''
        google access_token 및 user_info 요청

        ---
        '''
        data = request.query_params

        # access_token 발급 요청
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
        access_token = token_json.get('access_token')

        if not access_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # google 회원정보 요청
        query_string = {
            'access_token': access_token
        }
        user_info_res = requests.get(google_profile_url, params={'access_token': access_token})
        user_info_json = user_info_res.json()
        if (user_info_res.status_code != 200) or (not user_info_json):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        social_type = 'google'
        social_id = f"{social_type}_{user_info_json.get('user_id')}"
        user_email = user_info_json.get('email')

        # 회원가입 및 로그인
        res = login_api(social_type=social_type, social_id=social_id, email=user_email)
        return res


