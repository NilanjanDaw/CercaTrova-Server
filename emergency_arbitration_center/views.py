import requests
import datetime

from django.shortcuts import render
from django.contrib.gis.measure import D
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.conf import settings
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from emergency_arbitration_center.models import emergency
from emergency_arbitration_center.serializer import EmergencySerializer
from login_server.models import User
from login_server.serializer import UserSerializer
from personnel_login_server.models import EmergencyPersonnel
from personnel_login_server.serializer import EmergencyPersonnelSerializer

"""
    The main notification arbitration service. Receives a POST request
    from a remote client. Finds the nearest probable responder unit
    and forwards a notification to it.
    @param request The payload body  contained within the API request
"""
@api_view(['GET', 'POST'])
def getNotification(request):
    """
        Receives a GET request of the form http://127.0.0.1:8000/emergency/notify/
        Returns the list of all archived historical Emergencies
        else
        Receives a POST request of the form http://127.0.0.1:8000/emergency/notify/
        Finds a responder unit and returns its details to the invoking client
        Also forwards a notification using FCM to the responder unit.
        Archives the new Emergency
    """
    if request.method == 'GET':
        data = emergency.objects.all()
        serializer = EmergencySerializer(data, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        user_adhaar_number = request.data['user_adhaar_number']
        # Retrieves profile details of the invoking remote client
        profile_data = User.objects.filter(adhaar_number=user_adhaar_number)
        if len(profile_data) > 0:
            # Sets a account inactivity threshold at 2 minutes
            time_threshold = timezone.now() - datetime.timedelta(minutes=2)
            emergency_location = GEOSGeometry(request.data['location'])
            emergency_type = request.data['emergency_type']

            """ finds the nearest active unit within 5km with a matching responder_type"""
            assignment_list = EmergencyPersonnel.objects.filter(last_update__gte=time_threshold, \
                location__distance_lte=(emergency_location, D(m=5000)), \
                status=1, responder_type=emergency_type) \
                .annotate(distance=Distance('location', emergency_location)) \
                .order_by('distance')
            if len(assignment_list) > 0:
                # if an unit is found it is inactivated and a notified
                assignment_list[0].status = 2
                assignment_list[0].save()
                assignment_serialized = EmergencyPersonnelSerializer(assignment_list[0])
                informationExchange(assignment_list[0], profile_data[0])
                serializer = EmergencySerializer(data=request.data)
                # The emergency is archived
                if serializer.is_valid():
                    serializer.save()
                    return Response(assignment_serialized.data, status=status.HTTP_201_CREATED)
                else:
                    print(serializer.errors)
    return Response(status=status.HTTP_400_BAD_REQUEST)
"""
    Receives a POST request from a remote Responder
    confirming willingness to investigate forwarded emergency
    @param request The payload body  contained within the API request
"""
@api_view(['POST'])
def acceptEmergency(request):
    user_adhaar_number = request.data["user_adhaar_number"]
    personnel_id = request.data["personnel_id"]
    emergencyData = emergency.objects.filter(user_adhaar_number=user_adhaar_number,\
                    status=0).order_by('-timestamp')
    personnel = EmergencyPersonnel.objects.filter(personnel_id=personnel_id)
    # Relevant tables are updated reflecting the confirmation
    if len(emergencyData) > 0 and len(personnel) > 0:
        emergencyData[0].emergency_responder_id = personnel[0].personnel_id
        emergencyData[0].status = 1
        emergencyData[0].save()
        personnel[0].status = 0
        personnel[0].save()
        return  Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)
"""
    Method to forward user details to Responder Unit
    via Firebase Cloud Messaging
    @param personnel EmergencyPersonnel object containing details of Responder Unit
    @param user User object containing details of the invoking Emergency User
"""
def informationExchange(personnel, user):
    # Adding authorization headers
    headers = {
    'authorization': "key=" + str(settings.FCM_APIKEY),
    'content-type': "application/json",
    'cache-control': "no-cache",
    }
    serializer = UserSerializer(user)
    to = str(personnel.device_id)
    json = JSONRenderer().render(serializer.data)
    # creating payload for transfer
    payload = "{ \"data\":" + str(json) + ",\"priority\" : \"high\",\"to\" : \"" + to + "\"}"
    # creating a POST request to FCM server
    response = requests.request("POST", settings.FCM_URL, data=payload, headers=headers)
