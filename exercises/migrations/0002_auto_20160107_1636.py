# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-07 16:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='muscle',
            name='name',
            field=models.CharField(help_text='Latin representation', max_length=50),
        ),
    ]
