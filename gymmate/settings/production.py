# Settings for production environment
from .base import *

# change allowed hosts to accomodate production environment
# http://stackoverflow.com/questions/23252733/i-get-an-error-400-bad-request-on-custom-heroku-domain-but-works-fine-on-foo-h

ALLOWED_HOSTS = [".herokuapp.com", ".jusdev.com"]


# production static file settings
# http://stackoverflow.com/questions/21141315/django-static-files-on-heroku

STATICFILES_DIRS = (
    join(BASE_DIR, 'static'),
)


# RabbitMQ Broker settings
# http://www.marinamele.com/2014/02/how-to-install-celery-on-django-and.html
BROKER_URL =  get_secret("CLOUDAMQP_URL")

CELERY_BACKEND = "amqp" 
CELERY_RESULT_DBURI = ""
