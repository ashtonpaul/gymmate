# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-24 22:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0017_auto_20160224_1513'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exerciseimage',
            options={'ordering': ['exercise', '-is_main'], 'verbose_name_plural': 'Exercise Images'},
        ),
    ]
