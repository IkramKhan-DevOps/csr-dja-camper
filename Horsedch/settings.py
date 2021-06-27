"""
Django settings for Horsedch project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if not DEBUG:
    ALLOWED_HOSTS = ['horsedch.pythonanywhere.com']
else:
    ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Horsedch',
    'Landlord',
    'Shop',
    'Authentication',
    'ckeditor',
    'decouple',
    "django.contrib.sites",
    'autoslug',

    # Mailing App
    'post_office',
    'newsletter',

    # Social Authenticator App
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # social providers
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.google",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Horsedch.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'Horsedch.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# if DEBUG:
#     STATIC_URL = '/static/'
#     STATIC_ROOT = '/home/horsedch/csr-dja-camper/static'
#     MEDIA_URL = '/media/'
#     MEDIA_ROOT = '/home/horsedch/csr-dja-camper/media'
# else:
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

FB_APP_ID = '180914477204180'
FB_APP_SECRET = '81791c807c513a62297d5854ac1b7ef2'

SECRET_KEY = 'w&n#ay4(z705%os2x0cau!o@g$bh@xdu!kb@_z_s^u$xn_o1@='

SITE_ID = 2

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]

EMAIL_BACKEND = 'post_office.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'osmanamin689@gmail.com'
EMAIL_HOST_PASSWORD = 'pggcziywzyrwelzm'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

LOGIN_REDIRECT_URL = 'choose_role'
LOGOUT_REDIRECT_URL = '/'

STRIPE_PUBLISHABLE_KEY = 'pk_test_51I4VXzBZftcMcbw17MKX2VPqdOLFIWVKNkp7AUFCsGCPxmg3Q3zqOt9MtZSZDP2W8L0J4BJAPqe9zILBNb0h22Ov00C2rQSKPK'
STRIPE_SECRET_KEY = 'sk_test_51I4VXzBZftcMcbw1r4Es8h1XlpU4r06RGvREPKztp86MUCPZJsq1IB8dE76jxa3yNe5SBaxzU8j7U3t0EChE1yjA00WpzQbrzD'
STRIPE_WEBHOOK_SECRET = "whsec_NxQLEqptBcpR2fWDbVmCGZzY45wtzfp8"
STRIPE_CONNECT_CLIENT_ID = "ca_JUYeYqcKau0UEr0D16PUhjGSvEBBJe4M"
