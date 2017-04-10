from rest_framework import serializers
from login_server.models import User
from emergency_arbitration_center.models import emergency

class EmergencySerializer(serializers.ModelSerializer):
    """Serializer for Emergency Model"""
    class Meta :
        model = emergency
        fields = ('timestamp', 'user_adhaar_number', 'emergency_responder_id','emergency_type', 'status')
