from django.conf.urls import url
from personnel_login_server import views
""" End point URLs for Personnel Profile Login, Registration, and Updation"""
urlpatterns = [
    url(r'^personnel_login_server/user/$', views.account_registration, name="create"),
    url(r'^personnel_login_server/account_authentication/$', views.account_authentication, name="authenticate"),
    url(r'^personnel_login_server/update/$', views.update_account_information, name="update"),
]
