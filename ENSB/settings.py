"""
Django settings for ENSB project, adapté pour déploiement sur PythonAnywhere.
"""

from pathlib import Path
import os

# =======================
# BASE DIR
# =======================
BASE_DIR = Path(__file__).resolve().parent.parent

# =======================
# SECRET KEY
# =======================
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-8ab$ad!=9*g1f6o_$&zro3#-uhit8p_!7*^g3e$wcg58k&1gp-')

# =======================
# DEBUG & ALLOWED HOSTS
# =======================
DEBUG = False
ALLOWED_HOSTS = ['geg.pythonanywhere.com']

# =======================
# APPLICATIONS
# =======================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

# =======================
# MIDDLEWARE
# =======================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ENSB.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'ENSB.wsgi.application'

# =======================
# DATABASE (MySQL PythonAnywhere)
# =======================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'geg$ensb_db',
        'USER': 'geg',
        'PASSWORD': 'Informatique@1991',
        'HOST': 'geg.mysql.pythonanywhere-services.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# =======================
# PASSWORD VALIDATION
# =======================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# =======================
# INTERNATIONALIZATION
# =======================
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# =======================
# STATIC & MEDIA
# =======================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')   # pour collectstatic sur PythonAnywhere

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# =======================
# EMAIL (Gmail)
# =======================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'gegoubemapagne@gmail.com'
EMAIL_HOST_PASSWORD = 'Informatique@1991'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
