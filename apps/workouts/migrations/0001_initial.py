# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-10 09:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_auto_20151228_0046'),
        ('exercises', '0008_auto_20160108_1811'),
    ]

    operations = [
        migrations.CreateModel(
            name='Routine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('exercises', models.ManyToManyField(to='exercises.Exercise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.AccountUser')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
