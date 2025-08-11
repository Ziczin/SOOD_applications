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
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '[::1]',
    '192.168.101.102'  # с www
]

####################
##### SETTINGS #####
####################

ROOT_URLCONF = 'SOOD_applications.urls'
WSGI_APPLICATION = 'SOOD_applications.wsgi.application'
ASGI_APPLICATION = 'SOOD_applications.asgi.application'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'apps.users',
    'apps.forms',
    'apps.application',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'SOOD_applications.middleware.DisableCacheMiddleware'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = db_config

################
##### AUTH #####
################

AUTH_USER_MODEL = 'users.CustomUser'
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend',]

AUTH_PASSWORD_VALIDATORS = []

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

##### LANG #####
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

##### FILES #####
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

##### FORMS #####
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

##### CUSTOM #####
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
