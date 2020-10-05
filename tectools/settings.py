"""
Django settings for tectools project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import subprocess
from pathlib import Path
from django.contrib import messages 
import django_heroku

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@aav9ai4j44^!6o(zoz^-j9ha=ihcc!gow2ps6pxxxa626sm#j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['django3-tectools.herokuapp.com','localhost','LAPTOP-7KDAHV3M.PITSolution.local']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap4',
    'fontawesome_5',
    'bootstrap_datepicker_plus',
    'report',
    'core',
]

BOOTSTRAP4 = {
    'include_jquery': True,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tectools.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'tectools.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'tectoolsdb.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo' # Default: UTC

USE_I18N = True

USE_L10N = True

USE_TZ = False # Default: True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR,'media')

OS_SEPARATOR = os.sep

PDF_ROOT = os.path.join(BASE_DIR,'media'+os.sep+'pdf')

CSS_REPORT_ROOT = os.path.join(BASE_DIR,'report'+os.sep+'static'+os.sep+'css')

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'media'),
)

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/'

# Esta configurado o envio de email para o console até que se tenha um provedor real de email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MSG_TAGS = {
    messages.INFO:'text-info',
    messages.SUCCESS:'text-success',
    messages.ERROR:'text-danger',
    messages.DEBUG:'text-default',
    messages.WARNING:'text-warning',
}

FONTAWESOME_5_CSS = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.14.0/css/all.min.css'

"""
FONTAWESOME_5_CSS_ADMIN = None
    default: 'fontawesome_5/css/django-fontawesome.css'
FONTAWESOME_5_CSS_ADMIN = URL or path
    default: None
FONTAWESOME_5_ICON_CLASS = 'default' or 'semantic_ui' 
    default: 'default'
FONTAWESOME_5_PREFIX = 'custom_prefix'
    default: 'fa'
"""


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

"""This combines automatic compression with the caching behaviour provided by Django’s ManifestStaticFilesStorage backend. 
   If you want to apply compression but don’t want the caching behaviour then you can use:
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
"""


if 'DYNO' in os.environ:


    WKHTMLTOPDF_CMD = subprocess.Popen(
    ['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf-pack')], # Note we default to 'wkhtmltopdf' as the binary name
    stdout=subprocess.PIPE).communicate()[0].strip()    

    print('ENVIRONMENT DYNO: {}'.FORMAT(WKHTMLTOPDF_CMD))
    
    WKHTMLTOPDF_CMD = "bin/wkhtmltopdf"

else:
    print ('loading wkhtmltopdf path on localhost')
    WKHTMLTOPDF_CMD = "wkhtmltopdf"
    
WKHTMLTOPDF_CMD_OPTIONS = {
    'quiet': True,
}    

django_heroku.settings(locals())