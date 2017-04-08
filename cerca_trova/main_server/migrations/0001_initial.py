# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-07 11:01
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adhaar_number', models.CharField(max_length=12)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email_id', models.CharField(max_length=255, unique=True)),
                ('contact_number', models.IntegerField()),
                ('address', models.CharField(max_length=512)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=1)),
                ('blood_group', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
    ]