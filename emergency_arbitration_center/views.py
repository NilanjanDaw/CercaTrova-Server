import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.gis.measure import D
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from emergency_arbitration_center.models import emergency
from emergency_arbitration_center.serializer import EmergencySerializer
from login_server.models import User
from login_server.serializer import UserSerializer
from personnel_login_server.models import EmergencyPersonnel
from personnel_login_server.serializer import EmergencyPersonnelSerializer
from django.conf import settings
from rest_framework.renderers import JSONRenderer


@api_view(['GET', 'POST'])
def notifications(request):

    if request.method == 'GET':
        data = emergency.objects.all()
        serializer = EmergencySerializer(data, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        user_adhaar_number = request.data['user_adhaar_number']
        profile_data = User.objects.filter(adhaar_number=user_adhaar_number)
        if len(profile_data) > 0:
            emergency_location = GEOSGeometry(request.data['location'])
            emergency_type = request.data['emergency_type']
            assignment_list = EmergencyPersonnel.objects.filter(location__distance_lte=(emergency_location, D(m=2000)), \
                status=1, responder_type=emergency_type) \
                .annotate(distance=Distance('location', emergency_location)) \
                .order_by('distance')
            if len(assignment_list) > 0:
                assignment_serialized = EmergencyPersonnelSerializer(assignment_list[0])
                sendMessageToPersonnel(assignment_list[0], profile_data[0])
                serializer = EmergencySerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(assignment_serialized.data, status=status.HTTP_201_CREATED)
                else:
                    print(serializer.errors)
    return Response(status=status.HTTP_400_BAD_REQUEST)

def sendMessageToPersonnel(personnel, user):
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
    print(response.text)
