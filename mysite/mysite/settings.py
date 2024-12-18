"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import logging.config
from os import getenv
from pathlib import Path

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = BASE_DIR / 'database'
DATABASE_DIR.mkdir(exist_ok=True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-utr!fp#5bvj$f65nr38262)u+%04ef6ni^3+u3+^1rbmt=a)9j'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv('DJANGO_DEBUG', '0') == '1'

ALLOWED_HOSTS = ["*"] + getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

INTERNAL_IPS = [
    "127.0.0.1",
]

# для Django Debug Toolbar
if DEBUG:
    import socket

    hostname, _trash, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS.append("10.0.2.2")
    INTERNAL_IPS.extend(
        [ip[: ip.find(".")] + ".1" for ip in ips]
    )

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    'rest_framework',
    'django_filters',
    'drf_spectacular',
    'debug_toolbar',

    'shopapp.apps.ShopappConfig',
    'user_auth.apps.UserAuthConfig',
    'blogapp.apps.BlogappConfig',

]

MIDDLEWARE = [
    # 'django.middleware.cache.UpdateCacheMiddleware',  # для кэширования
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    #     'django.middleware.cache.FetchFromCacheMiddleware',  # для кэширования

    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'mysite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_DIR / 'db.sqlite3',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var//tmp/django_cache',
    }
}
# время жизни кэша в секундах
CACHE_MIDDLEWARE_SECONDS = 30 * 60

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

USE_L10N = True
# путь для хранения файлов локализации
LOCALE_PATHS = [
    BASE_DIR / 'locale'
]
LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'uploads'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# для перенаправления после удачного входа в систему (app: user_auth)
LOGIN_REDIRECT_URL = reverse_lazy('user_auth:redirect_for_logged_user')
LOGOUT_REDIRECT_URL = reverse_lazy('user_auth:login')
LOGIN_URL = reverse_lazy('user_auth:login')

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'My site Project Zomboid',
    'DESCRIPTION': 'My site with shop app and custom auth',
    'VERSION': '1.0.0',
    'SERF_INCLUDE_SCHEMA': False,  # не включать информацию об этой странице в саму докуменатацию
}

LOGFILE_NAME = BASE_DIR / "logs.txt"
LOGFILE_SIZE = 5 * 1024 * 1024
LOGFILE_COUNT = 10

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': 'log: %(asctime)s [%(levelname)s] %(name)s: %(message)s', }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'logfile': {
            # 'class': "logging.handlers.TimedRotatingFileHandler",
            'class': "logging.handlers.RotatingFileHandler",
            'filename': LOGFILE_NAME,
            'maxBytes': LOGFILE_SIZE,
            'backupCount': LOGFILE_COUNT,
            'formatter': 'verbose',
        }
    },
    'root': {
        'handlers': [
            'console',
            'logfile',
        ],
        'level': 'INFO',
    },

}

LOGLEVEL = getenv('DJANGO_LOGLEVEL', 'info').upper()

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'console': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(message)s',
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
    },

    'loggers': {
        '': {
            'level': LOGLEVEL,
            'handlers': ['console'],
        },
    },
})
