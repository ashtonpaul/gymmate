# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-07 16:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0005_auto_20160107_1649'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipment',
            options={'ordering': ['name'], 'verbose_name_plural': 'Equipment'},
        ),
    ]
