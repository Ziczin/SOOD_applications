from pathlib import Path
from django.core.management.utils import get_random_secret_key

from .db_config import params as db_config

BASE_DIR = Path(__file__).resolve().parent.parent

##################
##### CONFIG #####
##################

SECRET_KEY = get_random_secret_key()
DEBUG = True
SITE_ID = 1

"""
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '[::1]',
    '192.168.200.16'
]
"""
ALLOWED_HOSTS = ["*"]

####################
##### SETTINGS #####
####################

ROOT_URLCONF = "SOOD_applications.urls"
WSGI_APPLICATION = "SOOD_applications.wsgi.application"
ASGI_APPLICATION = "SOOD_applications.asgi.application"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_rq",
    "rest_framework",
    "apps.users",
    "apps.forms",
    "apps.application",
]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

RQ_QUEUES = {
    "default": {
        "HOST": "127.0.0.1",
        "PORT": 6379,
        "DB": 2,
        "DEFAULT_TIMEOUT": 360,
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
        "": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

WHITENOISE_MAX_AGE = 31536000
WHITENOISE_USE_FINDERS = True

DATABASES = db_config

################
##### AUTH #####
################

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
}

CSRF_USE_SESSIONS = True
# Параметры сессий (пример, можно оставить дефолтные или настроить по нуждам)
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_SECURE = False  # True на проде с HTTPS
SESSION_COOKIE_SAMESITE = "Lax"  # или 'Strict' / None при необходимости
SESSION_COOKIE_DOMAIN = None


AUTH_USER_MODEL = "users.CustomUser"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_PASSWORD_VALIDATORS = []

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
]

##### LANG #####
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

##### FILES #####
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

COLLECTED_URL = "/collected/"
COLLECTED_ROOT = BASE_DIR / "collected"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]

##### FORMS #####
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

##### CUSTOM #####
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/users/login/"
