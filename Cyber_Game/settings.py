"""
Django settings for Cyber_Game project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import datetime
import os
from decouple import config 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DJOSER = {
    # "SEND_ACTIVATION_EMAIL": False,
    'PASSWORD_RESET_CONFIRM_URL': "{uid}/{token}",
    # 'USERNAME_RESET_CONFIRM_URL': "reset/username/{uid}/{token}",
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SERIALIZERS': {
        'user_create': 'core.serializers.UserCreateSerializer',
        'current_user': 'core.serializers.UserSerializer',
    }
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=300),
}

# REST_KNOX = {
#   'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
#   'AUTH_TOKEN_CHARACTER_LENGTH': 64,
#   'TOKEN_TTL': None,
#   'USER_SERIALIZER': 'knox.serializers.UserSerializer',
#   'TOKEN_LIMIT_PER_USER': None,
#   'AUTO_REFRESH': False,
#   'EXPIRY_DATETIME_FORMAT': None,
# }

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')

ALLOWED_HOSTS = ['*']


# Application definition

SUBSCRIPTION_AUTO_DISCOVER = True
SUBSCRIPTION_MODULE  = 'subscription'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com" 
EMAIL_USE_TLS = True                 
EMAIL_PORT = 587
EMAIL_HOST_USER = "cypartapy@gmail.com"
EMAIL_HOST_PASSWORD = "okdfrdtfhxedfrhj"
DEFAULT_FROM_EMAIL = 'cypercube@localhost'

INSTALLED_APPS = [
    "daphne",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'djoser',
    'django_filters',
    # 'knox',
    'django_countries',
    'Security_Cube_app',
    'subscription',
    'core',
    'corsheaders',
    # 'model_subscription',
    'phonenumber_field',   
    'django_crontab',

]

# CORS_ALLOWED_ORIGINS = [
#     "http://127.0.0.1:8000",
#     "http://localhost:8000",
#     "http://127.0.0.1:3000",
#     "http://localhost:3000",
#     "https://cyber-cube-x4tmr.ondigitalocean.app",
# ]

CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:8001',
#     'http://127.0.0.1:8001',
#     'http://localhost:3000',
#     'http://127.0.0.1:3000',
#     'https://meat-shop-4bdp9.ondigitalocean.app',
#     'https://stingray-app-ojidz.ondigitalocean.app',
#     'https://sadakatcdn.cyparta.com',
#     'https://floridahalalmeat.com',
#     'https://api.floridahalalmeat.com'
# ]

CSRF_TRUSTED_ORIGINS = [
    'https://cybercube-backend.cyparta.com',
    'https://cybercube-backend.cyparta.com/',
    'https://sadakatcdn.cyparta.com',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'

}


AUTH_USER_MODEL = "core.User"

ROOT_URLCONF = 'Cyber_Game.urls'

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

WSGI_APPLICATION = 'Cyber_Game.wsgi.application'
ASGI_APPLICATION = 'Cyber_Game.asgi.application'


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

AUTH_PASSWORD_VALIDATORS = [{
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    'OPTIONS': {
        'min_length': 6,
    }
}]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# CronJobs 
CRONJOBS = [
    ('0 0 * * *', 'core.management.commands.reset_daily_targets'),
]


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

####################################################################FOR DEPLOYMENT####################################################################

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("MYSQL_DATABASE"),
        "USER": config("MYSQL_USER"),
        "PASSWORD": config("MYSQL_PASSWORD"),
        "HOST": config("MYSQL_HOSTNAME"),
        "PORT": config("MYSQL_PORT"),
        "CONN_MAX_AGE": 90,
        "OPTIONS": {"charset": "utf8mb4"},
    }
}

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "globalcdn"
AWS_S3_ENDPOINT_URL = "https://nyc3.digitaloceanspaces.com"
AWS_S3_CUSTOM_DOMAIN = "sadakatcdn.cyparta.com"
AWS_DEFAULT_ACL = "public-read"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_LOCATION = "Cyber_Game"
STATIC_URL = "https://%s/%s/" % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
DEFAULT_FILE_STORAGE = "Cyber_Game.storage_backends.MediaStorage"
