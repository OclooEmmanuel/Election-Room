import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from django.templatetags.static import static

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-1bm-^p+%-^m18+9^9!i3!+zq@2u!x+md197@m9myaf9z+=5#q5',
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('1', 'true', 'yes')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost,testserver').split(',')

# CSRF origin allowlist (Deployment on Render / custom domains)
CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in os.environ.get('CSRF_TRUSTED_ORIGINS', 'https://*.onrender.com,https://*.render.com').split(',')
    if o.strip()
]


# Application definition

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'unfold.contrib.inlines',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'voting',
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

ROOT_URLCONF = 'prefect_voting.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'prefect_voting.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases
#
# Production (Render): set DJANGO_DB=postgres and the POSTGRES_* vars.
# Local development defaults to SQLite.
USE_POSTGRES = os.environ.get('DJANGO_DB', 'sqlite') == 'postgres'

if USE_POSTGRES:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB', 'postgres'),
            'USER': os.environ.get('POSTGRES_USER', ''),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
            'HOST': os.environ.get('POSTGRES_HOST', ''),
            'PORT': os.environ.get('POSTGRES_PORT', '5432'),
            'OPTIONS': {'sslmode': os.environ.get('POSTGRES_SSLMODE', 'require')},
            'CONN_MAX_AGE': 600,
            'CONN_HEALTH_CHECKS': True,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
            'OPTIONS': {
                'timeout': 30,
            },
        }
    }



# Password validation
# https://docs.djangoproject.com/en/6.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Accra'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [BASE_DIR / 'static']

STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Media storage
# https://docs.djangoproject.com/en/6.1/topics/files/
#
# Production (Render): set DJANGO_STORAGE=s3 and the AWS_* vars
# (Supabase Storage / S3-compatible). Local development uses MediaRoot on disk.
USE_S3 = os.environ.get('DJANGO_STORAGE', 'local') == 's3'

if USE_S3:
    # Supabase Storage S3 credentials come from .env (gitignored)
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
    AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL', '')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'eu-west-1')
    AWS_S3_ADDRESSING_STYLE = 'path'
    AWS_S3_FILE_OVERWRITE = False
    AWS_QUERYSTRING_AUTH = False
    # Serve media via the public (non-authenticated) object URL:
    # https://<ref>.supabase.co/storage/v1/object/public/<bucket>/<key>
    AWS_S3_CUSTOM_DOMAIN = os.environ.get(
        'AWS_S3_CUSTOM_DOMAIN',
        AWS_S3_ENDPOINT_URL.replace('https://', '').replace('/storage/v1/s3', '')
        + '/storage/v1/object/public/'
        + AWS_STORAGE_BUCKET_NAME,
    )
    DEFAULT_STORAGE_BACKEND = 'storages.backends.s3boto3.S3Boto3Storage'
else:
    DEFAULT_STORAGE_BACKEND = 'django.core.files.storage.FileSystemStorage'

# WhiteNoise serves static assets at production scale; the manifest backend
# needs `collectstatic` (only required in non-DEBUG environments).
STATICFILES_BACKEND = (
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
    if not DEBUG
    else 'django.contrib.staticfiles.storage.StaticFilesStorage'
)

STORAGES = {
    'default': {
        'BACKEND': DEFAULT_STORAGE_BACKEND,
        'OPTIONS': {},
    },
    'staticfiles': {
        'BACKEND': STATICFILES_BACKEND,
    },
}


# Security hardening for production (Render sits behind the platform proxy)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True


# django-unfold admin theme
# https://unfoldadmin.com/docs/

UNFOLD = {
    'SITE_TITLE': 'Election Room',
    'SITE_HEADER': 'Election Room',
    'SITE_SUBHEADER': 'Election administration',
    'SITE_URL': '/',
    'SITE_SYMBOL': 'how_to_vote',
    'SITE_FAVICONS': [
        {'rel': 'icon', 'href': lambda *args: static('img/favicon-box.png'), 'type': 'image/png'},
        {'rel': 'apple-touch-icon', 'href': lambda *args: static('img/favicon-box.png'), 'type': 'image/png'},
    ],
    'SHOW_HISTORY': True,
    'SHOW_VIEW_ON_SITE': True,
    'SHOW_BACK_BUTTON': False,
    'ENVIRONMENT': None,
    'COLORS': {
        'primary': {
            '50': '#eef4fb',
            '100': '#dceaf5',
            '200': '#bad7ec',
            '300': '#8cbce0',
            '400': '#5c9bd1',
            '500': '#3b7fbe',
            '600': '#2d67a2',
            '700': '#264f83',
            '800': '#22446c',
            '900': '#11375a',
            '950': '#0b2134',
        },
    },
    'STYLES': [lambda request: str(static('css/admin.css'))],
    'SIDEBAR': {
        'show_search': True,
        'show_all_applications': False,
        'navigation': [
            {
                'title': 'Shortcuts',
                'separator': True,
                'collapsible': True,
                'items': [
                    {
                        'title': 'Dashboard',
                        'icon': 'dashboard',
                        'link': '/dashboard/',
                    },
                    {
                        'title': 'View public site',
                        'icon': 'public',
                        'link': '/',
                    },
                    {
                        'title': 'Live results',
                        'icon': 'leaderboard',
                        'link': '/results/',
                    },
                ],
            },
        ],
    },
    'TABS': [
        {
            'models': [
                'voting.election',
                'voting.position',
                'voting.candidate',
                'voting.student',
                'voting.vote',
            ],
            'items': [
                {'title': 'Dashboard', 'link': '/dashboard/'},
            ],
        },
    ],
}


# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

MAILERS = {
    'default': {
        'BACKEND': (
            'django.core.mail.backends.console.EmailBackend'
            if DEBUG
            else os.environ.get(
                'EMAIL_BACKEND',
                'django.core.mail.backends.smtp.EmailBackend',
            )
        ),
        'HOST': os.environ.get('EMAIL_HOST', 'localhost'),
        'PORT': int(os.environ.get('EMAIL_PORT', '25')),
        'USER': os.environ.get('EMAIL_HOST_USER', ''),
        'PASSWORD': os.environ.get('EMAIL_HOST_PASSWORD', ''),
        'USE_TLS': os.environ.get('EMAIL_USE_TLS', 'True').lower() in ('1', 'true', 'yes'),
        'DEFAULT_FROM_EMAIL': os.environ.get('DEFAULT_FROM_EMAIL', 'webmaster@localhost'),
    },
}
