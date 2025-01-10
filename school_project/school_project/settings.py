"""
Django settings for school_project project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import environ



env = environ.Env(  
    # set casting, default value  
    DEBUG=(bool, False)  
)  

BASE_DIR = Path(__file__).resolve().parent.parent  
# Take environment variables from .env file  
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))  

SECRET_KEY = env("SECRET_KEY", default="change_me")  

DEBUG = env("DEBUG", default=False)  

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

AUTH_USER_MODEL = 'school_app.CustomUser'


# Expire sessions after 30 minutes of inactivity
SESSION_COOKIE_AGE = 60 * 30  # 30 minutes
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # End session when browser is closed
LOGIN_URL = '/login/'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap4',
    'school_app',
    'dbbackup',  
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

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

ROOT_URLCONF = 'school_project.urls'

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

WSGI_APPLICATION = 'school_project.wsgi.application'


WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = DEBUG


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        **env.db(default="sqlite:///db.sqlite3"),
        "OPTIONS": {
            "timeout": 20,
            "pragmas": {
                "journal_mode": "wal",
                "synchronous": "normal",
                "cache_size": -64 * 1000,  # 64MB cache
                "foreign_keys": 1
            }
        }
    }
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

LOGGING = {  
    "version": 1,  
    "disable_existing_loggers": False,  
    "handlers": {"console": {"class": "logging.StreamHandler"}},  
    "loggers": {"": {"handlers": ["console"], "level": "DEBUG"}},  
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = env.str("STATIC_URL", default="/static/")  
STATIC_ROOT = env.str("STATIC_ROOT", default=BASE_DIR / "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'school_app/static'),
    os.path.join(BASE_DIR, 'school_app/content'),
]
CONTENT_DIR = os.path.join(BASE_DIR, 'school_app/content')

# Media settings
MEDIA_ROOT = env("MEDIA_ROOT", default=BASE_DIR / "media")  
MEDIA_URL = env("MEDIA_PATH", default="/media/")


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Backup settings
DBBACKUP_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
DBBACKUP_STORAGE_OPTIONS = {
    'oauth2_access_token': env("DROPBOX_ACCESS_TOKEN"),
}

# Optional: Configure backup filename template
DBBACKUP_FILENAME_TEMPLATE = '{datetime}.{extension}'
DBBACKUP_CLEANUP_KEEP = 10  # Keep last 10 backups

# Optional: Backup Media Files too
DBBACKUP_CONNECTORS = {
    'default': {
        'ENGINE': 'dbbackup.db.sqlite.SqliteConnector',
    }
}
