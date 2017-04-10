from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from login_server.models import User
from login_server.serializer import UserSerializer

@api_view(['GET', 'POST'])
def account_registration(request):
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

@api_view(['POST'])
def account_authentication(request):
    user_id = request.data['user_id']
    password = request.data['password']
    profile_data = User.objects.filter(email_id=user_id, password=password)
    if len(profile_data) > 0:
        serializer = UserSerializer(profile_data[0])
        print(type(serializer.data))
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(None, status=status.HTTP_404_NOT_FOUND)
