# Settings for production environment
from .base import *

# change allowed hosts to accomodate production environment
# http://stackoverflow.com/questions/23252733/i-get-an-error-400-bad-request-on-custom-heroku-domain-but-works-fine-on-foo-h

ALLOWED_HOSTS = [".herokuapp.com", ".jusdev.com"]


# RabbitMQ Broker settings
# http://www.marinamele.com/2014/02/how-to-install-celery-on-django-and.html
# http://www.marinamele.com/2014/03/install-celery-with-django-on-heroku.html
BROKER_URL =  get_secret("CLOUDAMQP_URL")
BROKER_POOL_LIMIT = 20

CELERY_RESULT_BACKEND = "amqp://"
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
