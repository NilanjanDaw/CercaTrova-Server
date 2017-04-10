from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from emergency_arbitration_center.models import emergency
from emergency_arbitration_center.serializer import EmergencySerializer
from login_server.models import User
from login_server.serializer import UserSerializer

@api_view(['POST'])
def notifications(request):
    if request.method == 'POST':
        user_adhaar_number = request.data['user_adhaar_number']
        profile_data = User.objects.filter(adhaar_number=user_adhaar_number)
        if len(profile_data) > 0:
            print(profile_data[0].adhaar_number)
            serializer = EmergencySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
