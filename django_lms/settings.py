import django_heroku
import dj_database_url

from pathlib import Path
import os,django
from django.utils.encoding import force_str
django.utils.encoding.force_text = force_str
import environ
env = environ.Env()
environ.Env.read_env()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-j7xv%)66l8u0^8sxnj7()z$zll8&a2*_h2r84yeo9f2fidx8^7'

DEBUG = False

ALLOWED_HOSTS = ['*']

#####################RUNNING DEV SERVER###################
# DJANGO_SETTINGS_MODULE=django_lms.dev_settings python3 manage.py runserver
##########################################################

# Application definition
INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'django.contrib.humanize',
  'lmsApp.apps.lmsAppConfig',
  'crispy_forms',
  'github_storages',
]

####GIT-HUB STORAGE####
if DEBUG ==False:
    DEFAULT_FILE_STORAGE = "github_storages.backend.BackendStorages"
    GITHUB_HANDLE =env('GITHUB_HANDLE')
    ACCESS_TOKEN =env('ACCESS_TOKEN')
    GITHUB_REPO_NAME =env('GITHUB_REPO_NAME')
    MEDIA_BUCKET_NAME =env('MEDIA_BUCKET_NAME')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_lms.urls'
AUTH_USER_MODEL = 'lmsApp.Profile'
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_lms.wsgi.application'

DATABASES = {
    'default':dj_database_url.config()
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Kampala'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = 'static/'
STATICFILES_DIRS = [ 
  BASE_DIR / "static",]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = '/login'
django_heroku.settings(locals())