from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from personnel_login_server.models import EmergencyPersonnel
from personnel_login_server.serializer import EmergencyPersonnelSerializer

@api_view(['GET', 'POST'])
def account_registration(request):
    if request.method == 'GET':
        data = EmergencyPersonnel.objects.all()
        serializer = EmergencyPersonnelSerializer(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmergencyPersonnelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def account_authentication(request):
    personnel_id = request.data['personnel_id']
    password = request.data['password']
    print(personnel_id)
    profile_data = EmergencyPersonnel.objects.filter(personnel_id=personnel_id, password=password)
    if len(profile_data) > 0:
        serializer = EmergencyPersonnelSerializer(profile_data[0])
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(None, status=status.HTTP_404_NOT_FOUND)
