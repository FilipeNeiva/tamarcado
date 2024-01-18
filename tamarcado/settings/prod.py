from tamarcado.settings.base import *
from decouple import config

DEBUG = False
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "agenda",
        "USER": config('user'),
        "PASSWORD": config('password'),
        "HOST": config('host'),
        "PORT": config('port'),
    }
}
