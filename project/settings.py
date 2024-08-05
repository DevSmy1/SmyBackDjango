"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
import warnings
from decouple import config, Csv
import oracledb

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")


AMBIENTE = config("AMBIENTE", default="DEV", cast=str)
DEBUG = AMBIENTE != "PROD"

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="*", cast=Csv())


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Meus APPS
    "project.controleUni",
    "project.barcode",
    "project.intranet",
    "project.c5",
    # Others
    "ninja",
    "corsheaders",
]
if AMBIENTE != "PROD":
    INSTALLED_APPS.append("django_extensions")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Others middlewares
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database

if AMBIENTE == "DEV":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
if AMBIENTE == "HOMOLOG":
    oracledb.init_oracle_client()
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.oracle",
            "USER": config("USER_DB"),
            "PASSWORD": config("PASSWORD_DB"),
            "HOST": config("HOST_DB"),
            "PORT": config("PORT_DB"),
            "NAME": config("NAME_DB"),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Cors settings
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "credentials",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    ".AuthCookie",  # Add this line to allow the authcookie header
]

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

warnings.filterwarnings("ignore", message="Signature .* does not match any known type")


# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "cargo": {
            "handlers": [
                "cargoLog",
            ],
            "level": "WARNING",
        },
        "colab": {
            "handlers": [
                "colabLog",
            ],
            "level": "WARNING",
        },
        "agrupador": {
            "handlers": [
                "agrupadorLog",
            ],
            "level": "WARNING",
        },
    },
    "handlers": {
        "cargoLog": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/cargo.log"),
            "formatter": "simpleRe",
        },
        "colabLog": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/colab.log"),
            "formatter": "simpleRe",
        },
        "agrupadorLog": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/colab.log"),
            "formatter": "simpleRe",
        },
    },
    "formatters": {
        "simpleRe": {
            "format": "{levelname} {asctime} {module} {funcName} {lineno} {message}",
            "style": "{",
            "datefmt": "%d/%m/%Y %H:%M:%S",
        }
    },
}

# API
NINJA_PAGINATION_PER_PAGE = 15
