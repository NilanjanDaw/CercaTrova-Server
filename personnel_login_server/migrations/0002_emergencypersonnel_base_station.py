# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-13 16:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel_login_server', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emergencypersonnel',
            name='base_station',
            field=models.CharField(default='', max_length=255),
        ),
    ]
