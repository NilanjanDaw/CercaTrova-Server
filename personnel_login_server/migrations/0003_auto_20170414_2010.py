# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-14 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel_login_server', '0002_emergencypersonnel_base_station'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emergencypersonnel',
            name='contact_number',
            field=models.CharField(max_length=10),
        ),
    ]