from config.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'itbrat',
        'USER': 'postgres',
        "PASSWORD": "1",
        "HOST": "127.0.0.1",
        "PORT": 5432,
    }
}