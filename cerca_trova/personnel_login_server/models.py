from __future__ import unicode_literals

from django.contrib.gis.db import models

class EmergencyPersonnel(models.Model):
    """Database for emergency personnel"""
    personnel_id = models.CharField(max_length=255, primary_key=True, unique=True)
    adhaar_number = models.CharField(max_length=12, unique=True)
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    contact_number = models.BigIntegerField(blank=False)
    car_number = models.CharField(max_length=255, blank=False)
    responder_type = models.IntegerField(blank=False)
    base_station = models.CharField(max_length=255, blank=False, default="")
    password = models.CharField(max_length=255, blank=False)
    location = models.PointField(blank=True, null=True)
