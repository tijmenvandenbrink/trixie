# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-29 20:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('components', '0001_initial'),
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.Device'),
        ),
        migrations.AddField(
            model_name='component',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
