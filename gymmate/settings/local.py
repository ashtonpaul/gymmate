# Settings for local development environment
from .base import *

# Debug True for development
DEBUG = True

# Installed apps particualr to local/dev
INSTALLED_APPS += (
    "debug_toolbar",
    "kombu.transport.django",
)


# Broker settings for celery
# https://django-celery.readthedocs.org/en/2.4/getting-started/first-steps-with-django.html
BROKER_URL = "django://"

# Set callable toolbar callback to shor Django debug toolbar
# https://stackoverflow.com/questions/10517765/django-debug-toolbar-not-showing-up/10518040#10518040

def show_toolbar(request):
    return True

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}
