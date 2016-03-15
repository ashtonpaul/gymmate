# Settings for production environment
import dj_database_url

from .base import *

# production database url
# https://github.com/kennethreitz/dj-database-url#usage

DATABASES['default'] = dj_database_url.config(default=get_secret("JAWSDB_URL"))


# RabbitMQ Broker settings
# http://www.marinamele.com/2014/02/how-to-install-celery-on-django-and.html
BROKER_URL =  get_secret("CLOUDAMQP_URL")

CELERY_BACKEND = "amqp" 
CELERY_RESULT_DBURI = ""
