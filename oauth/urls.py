from django.urls import path

from .views import *


urlpatterns = [
    path('kakao/login/', KakaoLoginView.as_view()),
    path('kakao/login/callback/', KakaoCallbackView.as_view()),

    path('naver/login/', NaverLoginView.as_view()),
    path('naver/login/callback/', NaverCallbackView.as_view()),

    path('google/login/', GoogleLoginView.as_view()),
    path('google/login/callback/', GoogleCallbackView.as_view()),

]