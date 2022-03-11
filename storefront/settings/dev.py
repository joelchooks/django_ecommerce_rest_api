from flask import request
from .common import *


DEBUG = True

SECRET_KEY = 'django-insecure-hs6j037urx6iav+7#10%-vu4l4f5@@-1_zo)oft4g7$vf2$jmp'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# MySQL ENGINE
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': config('NAME'),
#         'HOST': 'localhost',
#         'USER': config('USER'),
#         'PASSWORD': config('PASSWORD')
#     }
# }

# postgreSQL ENGINE

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'storefront3',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

# CELERY_BROKER_URL = 'redis://localhost:6379/1' #'redis:6379' (for docker)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/2", #'redis:6379' (for docker)
        "TIMEOUT": 10* 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_HOST = 'localhost' #'smtp4dev' (for docker)
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_PORT = 2525


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True
}