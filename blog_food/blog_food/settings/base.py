import os
import environ

env = environ.Env()

environ.Env.read_env()

DEBUG = (bool, False)

#ROOT_DIR = BASE_DIR
# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = env.bool('DEBUG', default=False)
#SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)

SITE_ID = 1

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appfood',
    'appblog',
    'apprecetas',
    'apprecetasalzum',
    'appperderpeso',
    'appturismo',
    'appcontact',
    'ckeditor',
    'apppages.apps.ApppagesConfig',
    'mptt',
    'appservices.apps.AppservicesConfig',  #esto le indicamos que esta configurado en español .apps.ServicesConfig
    'appsocial.apps.AppsocialConfig',  #esto le indicamos que esta configurado como redes socailes en apps.py .apps.ServicesConfig
    'django.contrib.sitemaps',
    'django.contrib.sites',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
DEBUG_TOOLBAR_CONFIG = {
    "JQUERY_URL": '//cdn.bootcss.com/jquery/2.2.4/jquery.min.js',
}

ROOT_URLCONF = 'blog_food.urls'

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
                'appsocial.processors.ctx_dict'
            ],
            'libraries': {
                'staticfiles': 'django.templatetags.static',
            }
        },
    },
]

TEMPLATE_DEBUG = True

WSGI_APPLICATION = 'blog_food.wsgi.application'

# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CKEDITOR_CONFIGS = {
    'default': {
        'height':
        '500px',
        # tab key conversion space number
        'tabSpaces':
        4,
        # Toolbar Style
        'toolbar':
        'Custom',
        # Toolbar buttons
        'toolbar_Custom':
        [['Format'], ['Smiley', 'CodeSnippet'],
         ['Bold', 'Italic', 'Underline', 'RemoveFormat', 'Blockquote'],
         ['TextColor', 'BGColor'], ['Link', 'Unlink'],
         ['NumberedList', 'BulletedList'], ['Maximize']],
        # Add Code Block Plug-ins
        'extraPlugins':
        ','.join(['codesnippet']),
        'codeSnippet_languages': {
            'bash': 'Bash',
            'css': 'CSS',
            'django': 'Django',
            'html': 'HTML',
            'javascript': 'JavaScript',
            'php': 'PHP',
            'python': 'Python',
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

# Build paths inside the project like this: os.path.join(BASE_DIR, ..
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = '/home/jovamna/myprojectdir/foodemotions/blog_food/blog_food/staticfiles/'
STATICFILES_DIRS = [
    '/home/jovamna/myprojectdir/foodemotions/blog_food/appfood/static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#CONFIGURACION DE CKEDITOR PARA QUE TENGA TODAS LAS OPCIONES
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'none',
    },
}

# https://docs.djangoproject.com/en/1.6/topics/email/#console-backend
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#email config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = int(env('EMAIL_PORT'))
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
#EMAIL_USE_TLS = False