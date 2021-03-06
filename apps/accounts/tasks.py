from django.conf import settings
from django.core.mail import send_mail

from celery import task
from easy_thumbnails.files import generate_all_aliases
from easy_thumbnails.files import get_thumbnailer
from sparkpost import SparkPost


@task()
def send_email(user_email, template_name, template_data):
    """
    Send transactional email for registration, password etc
    """
    sp = SparkPost(settings.SPARKPOST_API_KEY)
    template_data = {"substitution_data": template_data}
    template = sp.templates.preview(template_name, template_data)
    send_mail(
        subject=template["subject"],
        message=template["text"],
        from_email='{0} <{1}>'.format(template["from"]["name"], template["from"]["email"]),
        recipient_list=['{0}'.format(user_email)],
        html_message=template["html"],
    )


@task()
def generate_thumbnails(model, pk, field):
    """
    Async task to generate thumbnail from file
    """
    instance = model.__default_manager.get(pk=pk)
    filefield = getattr(instance, field)
    generate_all_aliases(filefield, include_global=True)


@task()
def generate_thumbnail(obj, relative_name=None):
    return get_thumbnailer(obj, relative_name)['avatar'].url
