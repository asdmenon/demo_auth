import os

from .base import *  # noqa


DEBUG = True
ALLOWED_HOSTS = ["*"]
DEV = DEBUG

INSTALLED_APPS += ("debug_toolbar", "auth_app")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "demo_auth.db",
    }
}

MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

SECRET_KEY = "devel"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SITE_ID = 2

AUTH_PASSWORD_VALIDATORS = []
CIVILID_AUTH_URL = ""