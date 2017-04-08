from django.conf.urls import url
from main_server import views

urlpatterns = [
    url(r'^main_server/$', views.account_registration),
    url(r'^main_server/account_authentication/$', views.account_authentication),
]
