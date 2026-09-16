from pathlib import Path
from django.templatetags.static import static
from dotenv import load_dotenv
import dj_database_url
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = "True"
# DEBUG = "False"
# DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS","localhost,127.0.0.1").split(",")

SITE_URL = os.getenv("SITE_URL", "").strip().rstrip("/")


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
    "whitenoise.middleware.WhiteNoiseMiddleware",
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

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#         'OPTIONS': {
#             'timeout': 30,
#         },
#     }
# }



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#         'OPTIONS': {
#             'timeout': 30,
#         },
#     }
# }

DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
    # Force SSL (Supabase requires it)
DATABASES['default']['OPTIONS'] = {
    'sslmode': 'require',
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

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

# production
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"



# devmode
# STORAGES = {
#     'default': {
#         'BACKEND': 'django.core.files.storage.FileSystemStorage',
#         'OPTIONS': {},
#     },
#     'staticfiles': {
#         'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
#     },
# }

# production
STORAGES = {
"default": {
    "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
},
"staticfiles": {
    "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
},
}

# supabase storage config
AWS_ACCESS_KEY_ID = os.getenv("SUPABASE_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("SUPABASE_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("SUPABASE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = os.getenv("SUPABASE_S3_ENDPOINT_URL")
AWS_S3_CUSTOM_DOMAIN = os.getenv("SUPABASE_S3_CUSTOM_DOMAIN")
AWS_S3_REGION_NAME = "eu-west-1"
AWS_DEFAULT_ACL = "public-read"
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False


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


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}
