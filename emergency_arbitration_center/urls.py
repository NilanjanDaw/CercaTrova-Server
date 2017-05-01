from django.conf.urls import url
from emergency_arbitration_center import views
""" End point URLs for the arbitration center """
urlpatterns = [
    url(r'^emergency/notify/$', views.getNotification),
    url(r'^emergency/accept/$', views.acceptEmergency),
]
