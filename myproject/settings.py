"""
Django settings for source project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import json
import sys
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_BASE_DIR = Path(__file__).resolve().parent

SECRET_BASE_FILE = os.path.join(CONFIG_BASE_DIR, 'secrets/secrets.json')
secrets = json.loads(open(SECRET_BASE_FILE).read())
for key, value in secrets.items():
    setattr(sys.modules[__name__], key, value)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = True if os.environ.get('DJANGO_DEBUG', 'False') == 'True' else False

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # external library
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',

    'oauth',
    'users',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [  # 기본 Permission 설정
        # 'rest_framework.permissions.AllowAny',  # 모든 계정 액세스 허용
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (  # Authenticationt 설정
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': [  # api 결과 전달 방식
        'rest_framework.renderers.JSONRenderer',  # json 방식
    ],
    'DEFAULT_PARSER_CLASSES': [  # 요청 받을 때 body 형태
        'rest_framework.parsers.JSONParser',
        # 'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',  # serializer datetime format
}

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_PASSWORD_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'

REST_USE_JWT = False
ACCOUNT_LOGOUT_ON_GET = False
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS512',
    'SIGNING_KEY': '',

    'AUTH_HEADER_TYPES': ('Bearer',),  # 인증 헤더 유형
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',  # 인증 헤더 명칭
    'USER_ID_FIELD': 'social_id',  # 사용자 식별을 위한 토큰에 포함할 사용자 모델의 DB 필드명
    'USER_ID_CLAIM': 'social_id',  # 사용자 식별을 저장하는 데 사용할 생성된 토큰의 클레임

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),  # 토큰 유형 지정 클래스
    'TOKEN_TYPE_CLAIM': 'token_type',  # 토큰 유형 저장 클레임 명칭

    'JTI_CLAIM': 'jti',
}

AUTH_USER_MODEL = 'users.UserModel'
AUTHENTICATION_BACKENDS = (
    'users.lib.backends.SettingsBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },

    'LOGIN_URL': 'users:login',
    'LOGOUT_URL': 'users:logout',
    'USE_SESSION_AUTH': False,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'source.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'diary',  # 사용할 MongoDB 데이터베이스 이름
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': 'mongodb://localhost',  # MongoDB 호스트 주소 (기본적으로는 localhost)
            'port': 27017,  # MongoDB 포트 (기본적으로는 27017)
        }
    }
}
# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
