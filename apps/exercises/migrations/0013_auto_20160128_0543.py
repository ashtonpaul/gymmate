# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-28 05:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0012_auto_20160111_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='muscle',
            name='name',
            field=models.CharField(help_text=b'Muscle name e.g biceps', max_length=50),
        ),
    ]
