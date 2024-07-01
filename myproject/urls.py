"""
URL configuration for myproject myproject.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from drf_yasg.generators import OpenAPISchemaGenerator
from app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("oauth/", include('oauth.url')),
    path("users/", include('users.url')),
    path('', include('app.urls')),
    path('create/', views.your_model_create, name='create'),
    path('form/', views.your_form_view, name='your_form'),
    path('diary/', include('diaryapp.urls'))
]
