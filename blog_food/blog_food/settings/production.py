import os

#env = environ.Env()
#environ.Env.read_env()

from blog_food.settings.base import *

DEBUG = False

#env = environ.Env(ALLOWED_HOSTS=(list, ['*',]),
# SECRET_KEY=str,
#)

ALLOWED_HOSTS = [
    '127.0.0.1', 'localhost', 'www.foodingemotion.com', 'foodingemotion.com'
]

#SECRET_KEY = env.str('SECRET_KEY')
SECRET_KEY = 'hr808$*z)hlsz@vkjkw!laua+8yvc9r7&8_@pk@u)oua%=yd0@'

# Database
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'foodemotion',
        'USER': 'jovamna',
        'PASSWORD': 'Palmira@67',
        'HOST': 'localhost',
        'PORT': '3306',
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



#MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
#configuracion para los archivos media, esto esta hecho antes de hacer los modelos despues de la appfo>
#luego de haber creado la carpeta media en el fichero raiz

STATIC_URL = '/static/'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#CON NGNIX
#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_ROOT = '/home/jovamna/myprojectdir/foodemotions/blog_food/blog_food/staticfiles/'
STATICFILES_DIRS = [
    '/home/jovamna/myprojectdir/foodemotions/blog_food/appfood/static',
]

#MEDIA_URL = '/media/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_ROOT = '/home/jovamna/myprojectdir/foodemotions/blog_food/media'

#email config
EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = '208b46a9cbb412'
EMAIL_HOST_PASSWORD = 'e350193eb5faa7'
EMAIL_PORT = '2525'
EMAIL_USE_TLS = True
