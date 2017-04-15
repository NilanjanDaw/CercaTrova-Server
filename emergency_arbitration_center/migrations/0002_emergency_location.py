# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-15 14:23
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emergency_arbitration_center', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emergency',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
