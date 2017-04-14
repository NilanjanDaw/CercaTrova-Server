from rest_framework import serializers
from personnel_login_server.models import EmergencyPersonnel
class EmergencyPersonnelSerializer(serializers.ModelSerializer):
    """Serializer for EmergencyPersonnel model"""
    class Meta():
        model = EmergencyPersonnel
        fields = ('personnel_id', 'adhaar_number', 'first_name',
                'last_name', 'contact_number', 'car_number',
                'responder_type','password', 'location',)