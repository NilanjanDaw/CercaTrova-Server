from rest_framework import serializers
from personnel_login_server.models import EmergencyPersonnel
class EmergencyPersonnelSerializer(serializers.ModelSerializer):
    """Serializer for EmergencyPersonnel model"""
    class Meta():
        model = EmergencyPersonnel
        fields = ('last_update', 'personnel_id', 'adhaar_number', 'first_name',
                'last_name', 'contact_number', 'car_number','device_id',
                'status', 'responder_type','password', 'base_station', 'location',)
