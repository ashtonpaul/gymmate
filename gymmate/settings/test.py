# Settings for test environment
from .base import *

# Disable all logging for testing
LOGGING = {}

# Installed apps particualr to testing
INSTALLED_APPS += (
    "kombu.transport.django",
)

# Broker settings for celery
# https://django-celery.readthedocs.org/en/2.4/getting-started/first-steps-with-django.html
BROKER_URL = "django://"