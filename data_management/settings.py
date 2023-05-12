from os import environ
from os.path import abspath, dirname, join

try:
    from .developer import DEVELOPER
    if DEVELOPER:
        DEBUG = True
except:
    pass


from .local import (
    db_host,
    db_name,
    db_password,
    db_user,
    db_port,
    email_address,
    email_password
)

BASE_DIR = dirname(dirname(abspath(__file__)))
DB_HOST = db_host
DB_NAME = db_name
DB_PSWD = db_password
DB_PORT = db_port
DB_USER = db_user

ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'custom.User'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]
DATA_UPLOAD_MAX_MEMORY_SIZE = 50000000
DATA_UPLOAD_MAX_NUMBER_FIELDS = None
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': db_name,
        'USER': db_user,
        'PASSWORD': db_password,
        'HOST': db_host,
        'PORT': db_port,
        'TEST': {
            'TEMPLATE': 'data_management_template',
        },
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = email_address
EMAIL_HOST_PASSWORD = email_password
INSTALLED_APPS = [
    'billing',
    'camp_admin',
    'comptrollership',
    'custom',
    'fleet',
    'inventory',
    'local_calendar',
    'location',
    'map',
    'material_management',
    'organization',
    'personnel',
    'sampling',
    'shipment',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django_admin_multiple_choice_list_filter',
    'djcelery_email',
    'import_export',
    'nested_admin',
    'phonenumber_field'
]
LANGUAGE_CODE = 'en-us'
MEDIA_ROOT = environ['DATA_MANAGEMENT_MEDIA_ROOT']
MEDIA_URL = environ['DATA_MANAGEMENT_MEDIA_URL']
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
PHONENUMBER_DB_FORMAT = 'INTERNATIONAL'
ROOT_URLCONF = 'data_management.urls'
SECRET_KEY = '+f4&9j&@%p7kdj%##z^(!v%_)w($)vv8*dn57%6zj3@1n7hea7'
STATIC_ROOT = join(BASE_DIR, 'static/')
STATIC_URL = '/static/'
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
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_L10N = True
USE_THOUSAND_SEPARATOR = True
USE_TZ = True
WSGI_APPLICATION = 'data_management.wsgi.application'
