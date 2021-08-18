import environ

env = environ.Env()

environ.Env.read_env()

from blog_food.settings.base import *

DEBUG = False

env = environ.Env(
    ALLOWED_HOSTS=(list, [
        'mysite.com',
    ]),
    DATABASE_URL=str,
)

# Database
if "DATABASE_URL" in os.environ:

    DATABASES = {
        'default': env.db(),
    }

else:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

#STATIC_ROOT = 'static'

#email config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = True