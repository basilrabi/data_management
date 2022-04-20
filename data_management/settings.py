from os import environ
from os.path import abspath, dirname, join

from .local import db_host, db_name, db_password, db_user, db_port

DB_HOST = db_host
DB_NAME = db_name
DB_PSWD = db_password
DB_PORT = db_port
DB_USER = db_user

BASE_DIR = dirname(dirname(abspath(__file__)))
SECRET_KEY = '+f4&9j&@%p7kdj%##z^(!v%_)w($)vv8*dn57%6zj3@1n7hea7'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'billing.apps.BillingConfig',
    'custom.apps.CustomConfig',
    'fleet.apps.FleetConfig',
    'inventory.apps.InventoryConfig',
    'location.apps.LocationConfig',
    'map.apps.MapConfig',
    'organization.apps.OrganizationConfig',
    'personnel.apps.PersonnelConfig',
    'sampling.apps.SamplingConfig',
    'shipment.apps.ShipmentConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django_admin_multiple_choice_list_filter',
    'import_export'
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

ROOT_URLCONF = 'data_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'data_management.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': db_name,
        'USER': db_user,
        'PASSWORD': db_password,
        'HOST': db_host,
        'PORT': db_port,
    }
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

AUTH_USER_MODEL = 'custom.User'
DATA_UPLOAD_MAX_NUMBER_FIELDS = None
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LANGUAGE_CODE = 'en-us'
DATA_UPLOAD_MAX_MEMORY_SIZE = 50000000
MEDIA_ROOT = environ['DATA_MANAGEMENT_MEDIA_ROOT']
MEDIA_URL = environ['DATA_MANAGEMENT_MEDIA_URL']
STATIC_ROOT = join(BASE_DIR, 'static/')
STATIC_URL = '/static/'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_L10N = True
USE_THOUSAND_SEPARATOR = True
USE_TZ = True
