from pathlib import Path
from django.templatetags.static import static

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1bm-^p+%-^m18+9^9!i3!+zq@2u!x+md197@m9myaf9z+=5#q5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']


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

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
        'OPTIONS': {},
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}


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
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}