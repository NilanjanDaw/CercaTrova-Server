from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from login_server.models import User
from login_server.serializer import UserSerializer

"""
    API endpoint to create and list new user accounts
    @param request The payload body contained within the API request
    @return User details with HTTP status 201 if valid request is made else
            HTTP status 400 is returned
"""
@api_view(['GET', 'POST'])
def account_registration(request):
    """
        Receives a GET request of the form http://127.0.0.1:8000/login_server/user/
        Returns the list of all registered Users
        Else
        Receives a POST request of the form http://127.0.0.1:8000/login_server/user/
        Creates a new instance User profile data if entered credentials are valid
    """
    if request.method == 'GET':
        data = User.objects.all()
        serializer = UserSerializer(data, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
    Method to validate a Client and send back necessary details
    according to incoming payload
    Invoking POST URL: http://127.0.0.1:8000/login_server/account_authentication/
    @param request The payload body contained within the API request
    @return User details with HTTP status 202 if valid credentials are given else
            HTTP status 404 is returned
"""
@api_view(['POST'])
def validate_client(request):
    user_id = request.data['user_id']
    password = request.data['password']
    profile_data = User.objects.filter(email_id=user_id, password=password)
    if len(profile_data) > 0:
        serializer = UserSerializer(profile_data[0])
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(None, status=status.HTTP_404_NOT_FOUND)

"""
    Method to update a client's location or FCM device ID
    Invoking POST URL: http://127.0.0.1:8000/login_server/update/
    @param request The payload body contained within the API request
    @return User details with HTTP status 201 if valid data is provided else
            HTTP status 404 is returned
"""
@api_view(['POST'])
def update_account_information(request):
    user_id = request.data['user_id']
    try:
        profile_data = User.objects.get(email_id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # checks if location is to be updated
    if 'location' in request.data:
        profile_data.location = request.data['location']
    # checks if FCM device_id is to be updated
    if 'device_id' in request.data:
        profile_data.device_id = request.data['device_id']
    profile_data.save()
    serializer = UserSerializer(profile_data)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
