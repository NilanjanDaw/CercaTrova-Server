# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-13 15:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_server', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='contact_number',
            field=models.BigIntegerField(),
        ),
    ]
