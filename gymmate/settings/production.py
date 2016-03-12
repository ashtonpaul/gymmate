# Settings for production environment
from .base import *

# RabbitMQ Broker settings
# http://www.marinamele.com/2014/02/how-to-install-celery-on-django-and.html
BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = get_secret("RABBITMQ_USER")
BROKER_PASSWORD = get_secret("RABBITMQ_PASSWORD")
BROKER_VHOST = "/"

CELERY_BACKEND = "amqp" 
CELERY_RESULT_DBURI = ""
