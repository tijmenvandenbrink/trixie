# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_auto_20150320_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='category',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='device_type',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='hostname',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='ip',
            field=models.IPAddressField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='location',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='manufacturer',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='organization',
            field=models.ForeignKey(related_name='devices', to='organizations.Organization'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='serial',
            field=models.CharField(max_length=250, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='software_version',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
