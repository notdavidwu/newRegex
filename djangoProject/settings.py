"""
Django settings for djangoProject project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from pickle import FALSE, TRUE
# Build paths inside the project like this: BASE_DIR / 'subdir'.


BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(s2g%#sj&n2#04eb%m4*3zcv0qg=l15aq@qrl82i^ys52+%-x6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []



import mimetypes
mimetypes.add_type("text/css", ".css", True)

COMPRESS_OFFLINE = False 
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'demo.apps.DemoConfig',
    'DICOM.apps.DicomConfig',
    'Upload.apps.UploadConfig',
    'pool.apps.poolConfig',
    'confirm.apps.confirmConfig',
    'LabNLP.apps.LabNLPConfig',
    'tube.apps.TubeConfig',
    'tube2.apps.Tube2Config',
    'administrator.apps.AdministratorConfig',
    'Classify.apps.ClassifyConfig',
    'Search.apps.SearchConfig',
    'categorize.apps.categorizeConfig',
    'eventDefinition.apps.eventDefinitionConfig',
    'warehousing.apps.warehousingConfig',
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    'channels',
    'channels_redis',
    'MEWS.apps.MEWSConfig',
    'subjectPatientDecide.apps.subjectPatientDecideConfig',
    'appeal.apps.appealConfig',
]
X_FRAME_OPTIONS = 'SAMEORIGIN'
ASGI_APPLICATION = 'djangoProject.routing.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379),],
        },
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_globals.middleware.Global',
    'django_plotly_dash.middleware.BaseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

ROOT_URLCONF = 'djangoProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates').replace('\\', '/')],
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

WSGI_APPLICATION = 'djangoProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'NAME': 'Django',
            'USER': 'TEST',
            'PASSWORD': '81218',
            'HOST': '172.31.6.22',
            'PORT': '1433',
            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',  # ODBC連線應用驅動
                'MARS_Connection': True,
            },
        },
        'TUBE': {
            'ENGINE': 'mssql',
            'NAME': 'Tube',
            'USER': 'TEST',
            'PASSWORD': '81218',
            'HOST': '172.31.6.157',
            'PORT': '1433',
            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',  # ODBC連線應用驅動
                'MARS_Connection': True,
            },
        },
        'AIC_Infection': {
            'ENGINE': 'mssql',
            'NAME': 'AIC_Infection',
            'USER': 'TEST',
            'PASSWORD': '81218',
            'HOST': '172.31.6.22',
            'PORT': '1433',
            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',  # ODBC連線應用驅動
                'MARS_Connection': True,
            },
        },

        'MEWS': {
            'ENGINE': 'mssql',
            'NAME': 'MEWS',
            'USER': 'TEST',
            'PASSWORD': '81218',
            'HOST': '172.31.6.22',
            'PORT': '1433',
            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',  # ODBC連線應用驅動
                'MARS_Connection': True,
            },
        },
        'HealthData': {
            'ENGINE': 'mssql',
            'NAME': 'HealthData',
            'USER': 'TEST',
            'PASSWORD': '81218',
            'HOST': '172.31.6.22',
            'PORT': '1433',
            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',  # ODBC連線應用驅動
                'MARS_Connection': True,
            },
        },



        'dbDesigning': {
            'ENGINE': 'mssql',
            'NAME': 'dbDesigning',
            'USER': 'TEST',
            'PASSWORD': '81218',
            'HOST': '172.31.6.22',
            'PORT': '1433',
            'OPTIONS': { 
                'driver': 'ODBC Driver 17 for SQL Server',  # ODBC連線應用驅動
                'MARS_Connection': True,
            },
        },
        'coreDB': {
            'ENGINE': 'mssql',
            'NAME': 'coreDB',
            'USER': 'TEST',
            'PASSWORD': '81218',
            'HOST': '172.31.6.22',
            'PORT': '1433',
            'OPTIONS': { 
                'driver': 'ODBC Driver 17 for SQL Server',  # ODBC連線應用驅動
                'MARS_Connection': True,
            },
        },
        'AIC': {
            'ENGINE': 'mssql',
            'NAME': 'AIC',
            'USER': 'TEST',
            'PASSWORD': '81218',
            'HOST': '172.31.6.22',
            'PORT': '1433',
            'OPTIONS': { 
                'driver': 'ODBC Driver 17 for SQL Server',  # ODBC連線應用驅動
                'MARS_Connection': True,
            },
        },
        'practiceDB': {
            'ENGINE': 'mssql',
            'NAME': 'practiceDB',
            'USER': 'TEST',
            'PASSWORD': '81218',
            'HOST': '172.31.6.22',
            'PORT': '1433',
            'OPTIONS': { 
                'driver': 'ODBC Driver 17 for SQL Server',  # ODBC連線應用驅動
                'MARS_Connection': True,
            },
        },
        
        'AIC_Infection2': {
            'ENGINE': 'mssql',
            'NAME': 'AIC_Infection',
            'USER': 'Lex',
            'PASSWORD': 'lexlex5284',
            'HOST': '172.31.6.157',
            'PORT': '1433',
            'OPTIONS': {
                'driver': 'SQL Server Native Client 11.0',  # ODBC連線應用驅動
                'MARS_Connection': True,
            },
        },
        'NursingRecord': {
            'ENGINE': 'mssql',
            'NAME': 'NursingRecord',
            'USER': 'TEST',
            'PASSWORD': '81218',
            'HOST': '172.31.6.22',
            'PORT': '1433',
            'OPTIONS': {
                'driver': 'SQL Server Native Client 11.0',  # ODBC連線應用驅動
                'MARS_Connection': True,
            },
        },
    }
DATABASE_CONNECTION_POOLING  =  False

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hant'



USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_plotly_dash.finders.DashAssetFinder',
    'django_plotly_dash.finders.DashComponentFinder',
]

PLOTLY_COMPONENTS = [
    'dash_core_components',
    'dash_html_components',
    'dash_renderer',
    'dpd_components'
]

DICOM_URL = '/DICOM/'
DICOM_ROOT = os.path.join(BASE_DIR,'DICOM')
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
TIME_ZONE = 'Asia/Taipei'
ALLOWED_HOSTS = ['*']

STATIC_URL = '/static/'
COMPRESS_ROOT = '/static/'
HERE = os.path.dirname(os.path.abspath(__file__))
HERE = os.path.join(HERE, '../')
if DEBUG:
    STATICFILES_DIRS = (
        # Put strings here, like "/home/html/static" or "C:/www/django/static".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        os.path.join(BASE_DIR, 'static/'),
    )
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880
DATA_UPLOAD_MAX_NUMBER_FIELDS = 5242880

