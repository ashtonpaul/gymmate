# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-28 02:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metric',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.AccountUser', to_field='username'),
        ),
    ]
