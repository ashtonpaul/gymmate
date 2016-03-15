# Settings for production environment
from .base import *

# RabbitMQ Broker settings
# http://www.marinamele.com/2014/02/how-to-install-celery-on-django-and.html
BROKER_URL =  get_secret("CLOUDAMQP_URL")

CELERY_BACKEND = "amqp" 
CELERY_RESULT_DBURI = ""

ALLOWED_HOSTS = [".herokuapp.com", ".jusdev.com"]