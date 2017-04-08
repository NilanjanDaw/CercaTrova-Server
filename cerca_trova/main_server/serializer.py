from rest_framework import serializers
from main_server.models import User

class UserSerializer(serializers.ModelSerializer):
    """serializer for user table"""
    class Meta():
        model = User
        fields = ('adhaar_number','first_name','last_name',
            'email_id', 'contact_number', 'address', 'age', 'gender',
            'blood_group', 'password', 'location')
