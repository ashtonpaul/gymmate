# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-11 21:25
from __future__ import unicode_literals

import apps.accounts.models
from django.db import migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20160229_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountuser',
            name='avatar',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, upload_to=apps.accounts.models.upload_to),
        ),
    ]
