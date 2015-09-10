# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=200)),
                ('hostname', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('category', models.CharField(max_length=200)),
                ('device_type', models.CharField(max_length=200)),
                ('manufacturer', models.CharField(max_length=200)),
                ('serial', models.CharField(max_length=250)),
                ('location', models.TextField()),
                ('ip', models.IPAddressField()),
                ('software_version', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeviceStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('conversion', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Device statuses',
            },
            bases=(models.Model,),
        ),
    ]
