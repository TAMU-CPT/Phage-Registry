# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []
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


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DOCKER_DB_NAME'],
        'USER': os.environ['DOCKER_DB_USER'],
        'HOST': os.environ['DOCKER_DB_HOST'],
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
STATIC_ROOT = '/opt/static/'
# Folders to include (app/static/ seems to be included automatically)
STATICFILES_DIRS = (
    #os.path.join(BASE_DIR, "datatables"),
)

LOGIN_REDIRECT_URL = '/phage-registry/'
LOGIN_URL = '/phage-registry/login/'
USE_X_FORWARDED_HOST = True


#RAVEN_CONFIG = {
    #'dsn': 'https://5fc6f2b594dc4705843ec9f1e501a431:eed2d64de57346d4a5d1d05cba07bc3c@biobio-monitor.tamu.edu/sentry/8',
#}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        #'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        #'sentry': {
            #'level': 'WARNING',
            #'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        #},
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
        #'raven': {
            #'level': 'DEBUG',
            #'handlers': ['console'],
            #'propagate': False,
        #},
        #'sentry.errors': {
            #'level': 'DEBUG',
            #'handlers': ['console'],
            #'propagate': False,
        #},
    },
}
