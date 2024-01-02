"""
Django settings for awm_project project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
from django.contrib.gis import gdal
from django.conf import settings
from django.shortcuts import resolve_url
from django.urls import get_script_prefix
from django.utils.functional import lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
os.environ['GDAL_DATA'] = f"{os.environ.get('CONDA_PREFIX', '')}/share"
GDAL_LIBRARY_PATH = r'/opt/conda/envs/geodjango/lib/libgdal.so'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-n8%(-aj02cd90hqoj0)ezhcw%sq4@9v%hg5biz5dsow*29+hy_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'awm_app',
    'django.contrib.gis',
    'crispy_forms',
    'leaflet',
    'rest_framework',
    'pwa',
]

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'awm_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'awm_app' / 'templates']
        ,
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

WSGI_APPLICATION = 'awm_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'gis',
        'USER': 'orinmcd',
        'PASSWORD': 'docker',
        'HOST': 'awm_postgis_alias',
        'PORT': 5432
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Adjust based on your project structure
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_FAIL_SILENTLY = not DEBUG

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (53.0, -8.0),
    'DEFAULT_ZOOM': 6,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 18,
    'RESET_VIEW': False,
    'SCALE': None,
    'OPACITY': 0.5,
}


LOGIN_REDIRECT_URL = "index"
LOGOUT_REDIRECT_URL = "index"


# PWA Settings

# Lazy-evaluate URLs so including pwa.urls in root urlconf works
resolve_url = lazy(resolve_url, str)

# Get script prefix for apps not mounted under /
_PWA_SCRIPT_PREFIX = get_script_prefix()

# Path to the service worker implementation.  Default implementation is empty.
#PWA_SERVICE_WORKER_PATH = getattr(
#    settings,
#    "PWA_SERVICE_WORKER_PATH",
#    os.path.join(os.path.abspath(os.path.dirname(__file__)), "awm_app/templates", "serviceworker.js"),
#)
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR / 'awm_app' / 'templates' / 'serviceworker.js')

# App parameters to include in manifest.json and appropriate meta tags
PWA_APP_NAME = getattr(settings, "PWA_APP_NAME", "MyApp")
PWA_APP_DESCRIPTION = getattr(settings, "PWA_APP_DESCRIPTION", "My Progressive Web App")
PWA_APP_ROOT_URL = resolve_url(getattr(settings, "PWA_APP_ROOT_URL", _PWA_SCRIPT_PREFIX))
PWA_APP_THEME_COLOR = getattr(settings, "PWA_APP_THEME_COLOR", "#000")
PWA_APP_BACKGROUND_COLOR = getattr(settings, "PWA_APP_BACKGROUND_COLOR", "#fff")
PWA_APP_DISPLAY = getattr(settings, "PWA_APP_DISPLAY", "standalone")
PWA_APP_SCOPE = resolve_url(getattr(settings, "PWA_APP_SCOPE", _PWA_SCRIPT_PREFIX))
PWA_APP_DEBUG_MODE = getattr(settings, "PWA_APP_DEBUG_MODE", True)
PWA_APP_ORIENTATION = getattr(settings, "PWA_APP_ORIENTATION", "any")
PWA_APP_START_URL = resolve_url(getattr(settings, "PWA_APP_START_URL", _PWA_SCRIPT_PREFIX))
PWA_APP_FETCH_URL = resolve_url(getattr(settings, "PWA_APP_FETCH_URL", _PWA_SCRIPT_PREFIX))
PWA_APP_STATUS_BAR_COLOR = getattr(settings, "PWA_APP_STATUS_BAR_COLOR", "default")
PWA_APP_ICONS = getattr(
    settings,
    "PWA_APP_ICONS",
    [
        {"src": "/static/images/icons/icon-72x72.png", "sizes": "72x72"},
        {"src": "/static/images/icons/icon-96x96.png", "sizes": "96x96"},
        {"src": "/static/images/icons/icon-128x128.png", "sizes": "128x128"},
        {"src": "/static/images/icons/icon-144x144.png", "sizes": "144x144"},
        {"src": "/static/images/icons/icon-152x152.png", "sizes": "152x152"},
        {"src": "/static/images/icons/icon-192x192.png", "sizes": "192x192"},
        {"src": "/static/images/icons/icon-384x384.png", "sizes": "384x384"},
        {"src": "/static/images/icons/icon-512x512.png", "sizes": "512x512"},
    ],
)
PWA_APP_SPLASH_SCREEN = getattr(
    settings,
    "PWA_APP_SPLASH_SCREEN",
    [
        {
            "src": "/static/images/icons/splash-640x1136.png",
            "media": "(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)",
        },
        {
            "src": "/static/images/icons/splash-750x1334.png",
            "media": "(device-width: 375px) and (device-height: 667px) and (-webkit-device-pixel-ratio: 2)",
        },
        {
            "src": "/static/images/icons/splash-1242x2208.png",
            "media": "(device-width: 621px) and (device-height: 1104px) and (-webkit-device-pixel-ratio: 3)",
        },
        {
            "src": "/static/images/icons/splash-1125x2436.png",
            "media": "(device-width: 375px) and (device-height: 812px) and (-webkit-device-pixel-ratio: 3)",
        },
        {
            "src": "/static/images/icons/splash-828x1792.png",
            "media": "(device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 2)",
        },
        {
            "src": "/static/images/icons/splash-1242x2688.png",
            "media": "(device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 3)",
        },
        {
            "src": "/static/images/icons/splash-1536x2048.png",
            "media": "(device-width: 768px) and (device-height: 1024px) and (-webkit-device-pixel-ratio: 2)",
        },
        {
            "src": "/static/images/icons/splash-1668x2224.png",
            "media": "(device-width: 834px) and (device-height: 1112px) and (-webkit-device-pixel-ratio: 2)",
        },
        {
            "src": "/static/images/icons/splash-1668x2388.png",
            "media": "(device-width: 834px) and (device-height: 1194px) and (-webkit-device-pixel-ratio: 2)",
        },
        {
            "src": "/static/images/icons/splash-2048x2732.png",
            "media": "(device-width: 1024px) and (device-height: 1366px) and (-webkit-device-pixel-ratio: 2)",
        },
    ],
)
PWA_APP_DIR = getattr(settings, "PWA_APP_DIR", "auto")
PWA_APP_LANG = getattr(settings, "PWA_APP_LANG", "en-US")
PWA_APP_SCREENSHOTS = getattr(settings, "PWA_APP_SCREENSHOTS", [])
PWA_APP_SHORTCUTS = getattr(settings, "PWA_APP_SHORTCUTS", [])
