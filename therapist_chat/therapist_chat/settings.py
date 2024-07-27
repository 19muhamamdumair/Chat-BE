# therapist_chat/settings.py

"""
Django settings for therapist_chat project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME', 'postgres'),
        'USER': os.getenv('DB_USER', 'postgres.kuouxptesxeklwdavkdy'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'eTpRseb4zc4uNZvu'),
        'HOST': os.getenv('DB_HOST', 'aws-0-eu-west-1.pooler.supabase.com'),  # e.g., 'your-db-host.rds.amazonaws.com'
        'PORT': os.getenv('DB_PORT', '6543'),  # e.g., '5432'
    }
}


# Set the token lifetimes
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-i371l*@*!un=g%o56w$p%%d3^g&b^cx-ahblzbl*%1(ph=$(qe'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['13.60.35.232','127.0.0.1','13.48.27.232']

# settings.py

# AWS S3 settings
AWS_ACCESS_KEY_ID = 'AKIAU6GDUVAZP33CTNYC'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'chat-app-new'
AWS_S3_REGION_NAME = 'eu-north-1'

# Additional settings for S3
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None  # This ensures no ACLs are applied
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# For serving static files directly from S3
AWS_S3_URL_PROTOCOL = 'https'
AWS_S3_USE_SSL = True
AWS_S3_VERIFY = True

# Static and media file configuration
# STATIC_URL = f'{AWS_S3_URL_PROTOCOL}://{AWS_S3_CUSTOM_DOMAIN}/static/'
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = f'{AWS_S3_URL_PROTOCOL}://{AWS_S3_CUSTOM_DOMAIN}/media/'

# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

APPEND_SLASH = True

ASGI_APPLICATION = "therapist_chat.routing.application" #routing.py will handle the ASGI
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': "channels.layers.InMemoryChannelLayer"
        }
    }

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'chat',
    'channels',
    'storages',
    'corsheaders',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_ALL_HEADERS = True
CORS_ALLOW_ALL_METHODS = True

ROOT_URLCONF = 'therapist_chat.urls'

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

WSGI_APPLICATION = 'therapist_chat.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases




# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
