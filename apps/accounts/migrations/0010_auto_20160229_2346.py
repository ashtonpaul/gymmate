# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-01 05:46
from __future__ import unicode_literals

import apps.accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20160228_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountuser',
            name='avatar',
            field=models.ImageField(blank=True, default='', upload_to=apps.accounts.models.upload_to),
            preserve_default=False,
        ),
    ]
