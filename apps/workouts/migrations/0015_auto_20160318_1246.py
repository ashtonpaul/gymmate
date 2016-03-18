# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-18 17:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0014_auto_20160229_2349'),
    ]

    operations = [
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.IntegerField(null=True)),
                ('reps', models.IntegerField(null=True)),
                ('weight', models.IntegerField(null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='progress',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='progress',
            name='reps',
        ),
        migrations.RemoveField(
            model_name='progress',
            name='sets',
        ),
        migrations.RemoveField(
            model_name='progress',
            name='weight',
        ),
        migrations.AddField(
            model_name='set',
            name='progress',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workouts.Progress'),
        ),
    ]
