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


@api_view(['GET', 'POST'])
def getNotification(request):

    if request.method == 'GET':
        data = emergency.objects.all()
        serializer = EmergencySerializer(data, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        user_adhaar_number = request.data['user_adhaar_number']
        profile_data = User.objects.filter(adhaar_number=user_adhaar_number)
        if len(profile_data) > 0:
            time_threshold = timezone.now() - datetime.timedelta(minutes=10)
            emergency_location = GEOSGeometry(request.data['location'])
            emergency_type = request.data['emergency_type']
            assignment_list = EmergencyPersonnel.objects.filter(last_update__gte=time_threshold, location__distance_lte=(emergency_location, D(m=5000)), \
                status=1, responder_type=emergency_type) \
                .annotate(distance=Distance('location', emergency_location)) \
                .order_by('distance')
            if len(assignment_list) > 0:
                assignment_list[0].status = 2
                assignment_list[0].save()
                assignment_serialized = EmergencyPersonnelSerializer(assignment_list[0])
                informationExchange(assignment_list[0], profile_data[0])
                serializer = EmergencySerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(assignment_serialized.data, status=status.HTTP_201_CREATED)
                else:
                    print(serializer.errors)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def acceptEmergency(request):
    user_adhaar_number = request.data["user_adhaar_number"]
    personnel_id = request.data["personnel_id"]
    emergencyData = emergency.objects.filter(user_adhaar_number=user_adhaar_number,\
                    status=0).order_by('-timestamp')
    personnel = EmergencyPersonnel.objects.filter(personnel_id=personnel_id)
    if len(emergencyData) > 0 and len(personnel) > 0:
        emergencyData[0].emergency_responder_id = personnel[0].personnel_id
        emergencyData[0].status = 1
        emergencyData[0].save()
        personnel[0].status = 0
        personnel[0].save()
        return  Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

def informationExchange(personnel, user):
    headers = {
    'authorization': "key=" + str(settings.FCM_APIKEY),
    'content-type': "application/json",
    'cache-control': "no-cache",
    }
    serializer = UserSerializer(user)
    to = str(personnel.device_id)
    json = JSONRenderer().render(serializer.data)
    payload = "{ \"data\":" + str(json) + ",\"priority\" : \"high\",\"to\" : \"" + to + "\"}"
    response = requests.request("POST", settings.FCM_URL, data=payload, headers=headers)
