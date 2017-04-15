from __future__ import unicode_literals

from django.contrib.gis.db import models

class EmergencyPersonnel(models.Model):
    """Database for emergency personnel"""
    personnel_id = models.CharField(max_length=255, primary_key=True, unique=True)
    adhaar_number = models.CharField(max_length=12, unique=True)
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    contact_number = models.CharField(max_length=10, blank=False)
    car_number = models.CharField(max_length=255, blank=False)
    responder_type = models.IntegerField(blank=False)
    base_station = models.CharField(max_length=255, blank=False, default="")
    password = models.CharField(max_length=255, blank=False)
    status = models.IntegerField(default=0)
    device_id = models.CharField(max_length=1024, blank=True)
    location = models.PointField(blank=True, null=True)
