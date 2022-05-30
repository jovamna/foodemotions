import os
import environ

env = environ.Env()
environ.Env.read_env()

from blog_food.settings.base import *

DEBUG = False

#env = environ.Env(ALLOWED_HOSTS=(list, ['*',]),
# SECRET_KEY=str,
#)

ALLOWED_HOSTS = [
    '127.0.0.1', 'localhost', 'www.foodingemotion.com', 'foodingemotion.com'
]

SECRET_KEY = env.str('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASS'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    }
}

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

STATIC_URL = '/static/'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#CON NGNIX
#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_ROOT = '/home/jovamna/myprojectdir/foodemotions/blog_food/blog_food/staticfiles/'
STATICFILES_DIRS = [
    '/home/jovamna/myprojectdir/foodemotions/blog_food/appfood/static',
]

MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = '/home/jovamna/myprojectdir/foodemotions/blog_food/media/'

#email config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
#EMAIL_USE_TLS = False
