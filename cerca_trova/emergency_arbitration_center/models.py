from __future__ import unicode_literals

from django.contrib.gis.db import models

class emergency(models.Model):
    """Database to store emergency notifications"""
    timestamp = models.DateTimeField(auto_now_add=True)
    user_adhaar_number = models.CharField(max_length=12, primary_key=True, unique=True)
    emergency_responder_id = models.CharField(max_length=255, blank=True)
    emergency_type = models.IntegerField()
    status = models.IntegerField(default=0)
