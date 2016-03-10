"""
Django settings for phageregistry project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').strip() == 'True'

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', 'cpt.tamu.edu']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'haystack',
    'raven.contrib.django.raven_compat',
    'fontawesome',
    'registry',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'phageregistry.urls'

WSGI_APPLICATION = 'phageregistry.wsgi.application'


import os
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index', 'docker'),
    },
}

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DOCKER_DB_NAME'],
        'USER': os.environ['DOCKER_DB_USER'],
        'HOST': os.environ['DOCKER_DB_HOST'],
        'PASSWORD': os.environ['DOCKER_DB_PASS']
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# The URL to make ./static/ accessible at
STATIC_URL = '/phage-registry/static/'
# Things compile to
# static/
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# Folders to include (app/static/ seems to be included automatically)
STATICFILES_DIRS = (
    #os.path.join(BASE_DIR, "datatables"),
)

LOGIN_REDIRECT_URL = '/phage-registry/'
LOGIN_URL = '/phage-registry/login/'
USE_X_FORWARDED_HOST = True



LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

RAVEN_CONFIG = {}
if 'SENTRY_DSN' in os.environ:
    RAVEN_CONFIG['dsn'] = os.environ['SENTRY_DSN']
    LOGGING['root']['handlers'] = ['sentry']
    LOGGING['handlers']['sentry'] = {
        'level': 'WARNING',
        'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
    }
    LOGGING['loggers']['raven'] = {
        'level': 'DEBUG',
        'handlers': ['console'],
        'propagate': False,
    }
    LOGGING['loggers']['sentry.errors'] = {
        'level': 'DEBUG',
        'handlers': ['console'],
        'propagate': False,
    }
