# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-11 01:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0007_auto_20160111_0151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routine',
            name='days',
            field=models.ManyToManyField(blank=True, to='workouts.DayOfWeek'),
        ),
    ]
