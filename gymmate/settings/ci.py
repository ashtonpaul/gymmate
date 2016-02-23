# Settings for production environment
from .production import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gymmate',
        'USER': 'root',
        'PASSWORD': 'semaphoredb',
        'HOST': 'localhost',
        'PORT': '',
    }
}
