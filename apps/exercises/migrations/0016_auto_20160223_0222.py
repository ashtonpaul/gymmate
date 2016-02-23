# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-23 08:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0015_exerciseimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exerciseimage',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='exercises.Exercise'),
        ),
    ]
