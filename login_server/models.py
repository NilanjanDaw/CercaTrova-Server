from __future__ import unicode_literals

# from django.db import models
from django.contrib.gis.db import models

class User(models.Model):
    """Database Model for User"""
    adhaar_number = models.CharField(max_length=12, primary_key=True, unique=True)
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    email_id = models.CharField(max_length=255, blank=False, unique=True)
    device_id = models.CharField(max_length=1024, blank=True)
    contact_number = models.CharField(max_length=10, blank=False)
    address = models.CharField(max_length=512, blank=False)
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    blood_group = models.CharField(max_length=255)
    password = models.CharField(max_length=255, blank=False)
    location = models.PointField(blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True)
    emergency_contact_number = models.CharField(max_length=10, blank=True)
# TODO emergency contact
