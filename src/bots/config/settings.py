# -*- coding: utf-8 -*-


import os
import bots
# Django settings for bots project.
PROJECT_PATH = os.path.abspath(os.path.dirname(bots.__file__))

#*******settings for sending bots error reports via email**********************************
ADMINS = (    #bots will send error reports to the ADMINS
    ('name_manager', 'adress@test.com'),
    )
MANAGERS = ADMINS
EMAIL_HOST = 'localhost'             #Default: 'localhost'
EMAIL_PORT = '25'             #Default: 25
EMAIL_USE_TLS = False       #Default: False
EMAIL_HOST_USER = ''        #Default: ''. Username to use for the SMTP server defined in EMAIL_HOST. If empty, Django won't attempt authentication.
EMAIL_HOST_PASSWORD = ''    #Default: ''. PASSWORD to use for the SMTP server defined in EMAIL_HOST. If empty, Django won't attempt authentication.
#~ SERVER_EMAIL = 'user@gmail.com'           #Sender of bots error reports. Default: 'root@localhost'
#~ EMAIL_SUBJECT_PREFIX = ''   #This is prepended on email subject.

#*********database settings*************************
# Determine database engine based on environment variable or default to PostgreSQL
DB_ENGINE = os.environ.get('BOTS_DB_ENGINE', 'postgres').lower()

if DB_ENGINE == 'sqlite':
    # SQLite database settings
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(PROJECT_PATH, 'botssys/sqlitedb/botsdb'),
            'USER': '',         #not needed for SQLite
            'PASSWORD': '',     #not needed for SQLite
            'HOST': '',         #not needed for SQLite
            'PORT': '',         #not needed for SQLite
            'OPTIONS': {},      #not needed for SQLite
            }
        }
elif DB_ENGINE == 'mysql':
    # MySQL database settings
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('BOTS_DB_NAME', 'botsdb'),
            'USER': os.environ.get('BOTS_DB_USER', 'bots'),
            'PASSWORD': os.environ.get('BOTS_DB_PASSWORD', 'botsbots'),
            'HOST': os.environ.get('BOTS_DB_HOST', 'localhost'),
            'PORT': os.environ.get('BOTS_DB_PORT', '3306'),
            'OPTIONS': {'charset': 'utf8mb4'},
            }
        }
else:
    # PostgreSQL database settings (default)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('BOTS_DB_NAME', 'botsdb'),
            'USER': os.environ.get('BOTS_DB_USER', 'bots'),
            'PASSWORD': os.environ.get('BOTS_DB_PASSWORD', 'botsbots'),
            'HOST': os.environ.get('BOTS_DB_HOST', 'postgres' if os.path.exists('/.dockerenv') else '127.0.0.1'),
            'PORT': os.environ.get('BOTS_DB_PORT', '5432'),
            'OPTIONS': {},
            }
        }

#*********setting date/time zone and formats *************************
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Amsterdam'

#~ *********language code/internationalization*************************
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
#~ LANGUAGE_CODE = 'nl'
USE_I18N = True
USE_L10N = True
USE_TZ = True

#*************************************************************************
#*********other django setting. please consult django docs.***************
#*************************************************************************
#*************************************************************************

#*********path settings*************************
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
ROOT_URLCONF = 'bots.urls'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/home/'
LOGOUT_URL = '/logout/'
LOGOUT_REDIRECT_URL = '/'
ALLOWED_HOSTS = ['*']
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

#*********sessions, cookies, log out time*************************
SESSION_EXPIRE_AT_BROWSER_CLOSE = True      #True: always log in when browser is closed
SESSION_COOKIE_AGE = 3600                   #seconds a user needs to login when no activity
SESSION_SAVE_EVERY_REQUEST = True           #if True: SESSION_COOKIE_AGE is interpreted as: since last activity

#set in bots.ini
#~ DEBUG = True
#~ TEMPLATE_DEBUG = DEBUG
SITE_ID = 1
# Make this unique, and don't share it with anybody.
SECRET_KEY = 'm@-u37qiujmeqfbu$daaaaz)sp^7an4u@h=wfx9dd$$$zl2i*x9#awojdc'

#*******template handling and finding*************************************************************************
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_PATH, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'bots.bots_context.set_context',
            ],
        },
    },
]

#*******includes for django*************************************************************************
LOCALE_PATHS = (
    os.path.join(PROJECT_PATH, 'locale'),
    )
#save uploaded file (=plugin) always to file. no path for temp storage is used, so system default is used.
FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
    )
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bots',
]
