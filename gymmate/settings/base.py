"""
Django settings for gymmate project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import json

from django.core.exceptions import ImproperlyConfigured


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# JSON-based secrets module
with open("secrets.json") as f:
    secrets = json.loads(f.read())


# Get settings file secrets from json file to avoid secrets in repo
# Two Scoops of Django 1.8 - Section 5.4.1
def get_secret(setting, secrets=secrets):
    """
    Get the secret variable or return explicit exception.
    """
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

# Base settings shared by all other environments
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'django_filters',
    'oauth2_provider',
    'apps.accounts',
    'apps.metrics',
    'apps.exercises',
    'apps.workouts',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gymmate.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'gymmate.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_secret("DATABASE_NAME"),
        'USER': get_secret("DATABASE_USER"),
        'PASSWORD': get_secret("DATABASE_PASSWORD"),
        'HOST': get_secret("DATABASE_HOST"),
        'PORT': get_secret("DATABASE_PORT"),
        'TEST': {
            'NAME': 'test_database',
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Central'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


# Media files (Images, Documents, Media)
# https://docs.djangoproject.com/en/1.9/topics/files/

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Django REST framework (API)
# http://django-rest-framework.com

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated', ),
    'DEFAULT_AUTHENTICATION_CLASSES': ('oauth2_provider.ext.rest_framework.OAuth2Authentication',),
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': ('apps.core.pagination.LinkHeaderPagination'),
    'DEFAULT_VERSIONING_CLASS': ('rest_framework.versioning.NamespaceVersioning'),
    'ALLOWED_VERSIONS': ('v1', 'rest_framework_swagger'),
    'PAGE_SIZE': 10,
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '120/minute',
        'user': '120/minute'
    }
}


# Django rest framework settings
# http://django-rest-swagger.readthedocs.org/en/latest/settings.html

SWAGGER_SETTINGS = {
    'api_version': 'v1',
    'api_key': '',
    'info': {
        'contact': 'ashton@ashtonpaul.com',
        'description': 'The gym goers best friend. Quickly track '
                       'your workout and progress when you go workout. '
                       'This provides as the documentation for the endpoints.',
        'title': 'GymMate',
    },
    'token_type': 'Bearer'
}


# this is the list of available scopes
# https://django-oauth-toolkit.readthedocs.org/en/latest/rest-framework/getting_started.html

OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'exercises': 'Exercise scope',
        'metrics': 'Metric scope',
        'workouts': 'Workout scope',
    },
    'ACCESS_TOKEN_EXPIRE_SECONDS': 36000
}


# system and app logging formats
# https://docs.python.org/2/library/logging.html#formatter-objects

gymmate_log = '[%(stamp)s] %(user)s %(ip)s %(method)s %(path)s %(params)s %(status_code)d %(response_time)dms %(data)s'
django_log = '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'


# logging setup for the codebase for errors and apps for requests
# https://gist.github.com/JasonGiedymin/887364

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'api': {
            'format': gymmate_log,
        },
        'django': {
            'format': django_log,
        },
    },
    'handlers': {
        'request': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/gymmate.log',
            'when': 'midnight',
            'formatter': 'api',
            'backupCount': '365',
        },
        'code': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/django.log',
            'when': 'midnight',
            'formatter': 'django',
            'backupCount': '365',
        }
    },
    'loggers': {
        'apps.core.loggers': {
            'handlers': ['request'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['code'],
            'propagate': True,
            'level': 'ERROR',
        },
    },
}