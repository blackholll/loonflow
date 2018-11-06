from settings.common import *

MIDDLEWARE = [
    'service.permission.api_permission.ApiPermissionCheck',
    'service.csrf_service.DisableCSRF',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'test_loonflownew',  # Or path to database file if using sqlite3.
            'USER': 'loonflownew',  # Not used with sqlite3.
            'PASSWORD': '123456',  # Not used with sqlite3.
            'HOST': '127.0.0.1',  # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
        }
}

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = ''
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/1'
