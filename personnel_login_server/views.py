from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from personnel_login_server.models import EmergencyPersonnel
from personnel_login_server.serializer import EmergencyPersonnelSerializer
from cerca_trova import Encryption
"""
    API endpoint to create and list new EmergencyPersonnel accounts
    @param request The payload body contained within the API request
    @return Personnel details with HTTP status 201 if valid request is made else
            HTTP status 400 is returned
"""
@api_view(['GET', 'POST'])
def account_registration(request):
    """
        Receives a GET request of the form http://127.0.0.1:8000/personnel_login_server/user/
        Returns the list of all registered Users
        else
        Receives a POST request of the form http://127.0.0.1:8000/personnel_login_server/user/
        Creates a new instance User profile data if entered credentials are valid
    """
    if request.method == 'GET':
        data = EmergencyPersonnel.objects.all()
        serializer = EmergencyPersonnelSerializer(data, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.data['password'] = Encryption.decrypt(request.data['password'])
        request.POST._mutable = mutable
        serializer = EmergencyPersonnelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
    Method to validate an Emergency Personnel and send back necessary details
    according to incoming payload
    Invoking POST URL: http://127.0.0.1:8000/personnel_login_server/account_authentication/
    @param request The payload body contained within the API request
    @return Personnel details with HTTP status 202 if valid credentials are given else
            HTTP status 404 is returned
"""
@api_view(['POST'])
def account_authentication(request):
    mutable = request.POST._mutable
    request.POST._mutable = True
    request.data['password'] = Encryption.decrypt(request.data['password'])
    request.POST._mutable = mutable
    
    personnel_id = request.data['personnel_id']
    password = request.data['password']
    print(personnel_id)
    profile_data = EmergencyPersonnel.objects.filter(personnel_id=personnel_id, password=password)
    if len(profile_data) > 0:
        serializer = EmergencyPersonnelSerializer(profile_data[0])
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(None, status=status.HTTP_404_NOT_FOUND)
"""
    Method to update a Personnel's location, status or FCM device ID
    Invoking POST URL: http://127.0.0.1:8000/personnel_login_server/update/
    @param request The payload body contained within the API request
    @return Personnel details with HTTP status 201 if valid data is provided else
            HTTP status 404 is returned
"""
@api_view(['POST'])
def update_account_information(request):
    personnel_id = request.data['personnel_id']
    print(request.data['personnel_id'])
    try:
        profile_data = EmergencyPersonnel.objects.get(personnel_id=personnel_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # checks if location is to be updated
    if 'location' in request.data:
        profile_data.location = request.data['location']
    # checks if FCM device_id is to be updated
    if 'device_id' in request.data:
        profile_data.device_id = request.data['device_id']
    # checks if status is to be updated
    if 'status' in request.data:
        profile_data.status = request.data['status']
    profile_data.save()
    serializer = EmergencyPersonnelSerializer(profile_data)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
