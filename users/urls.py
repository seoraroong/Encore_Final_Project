from django.urls import path
from .views import *
from django.contrib import admin

app_name = 'users'

urlpatterns = [
    path('', UserView.as_view(), name='user'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', Register.as_view(), name='Register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]