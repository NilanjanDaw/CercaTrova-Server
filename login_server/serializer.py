from rest_framework import serializers
from login_server.models import User

class UserSerializer(serializers.ModelSerializer):
    """serializer for user table"""
    class Meta():
        model = User
        fields = ('adhaar_number','first_name','last_name',
            'email_id', 'contact_number', 'address', 'age', 'gender','device_id',
            'blood_group', 'password', 'location', 'emergency_contact_name', 'emergency_contact_number')
