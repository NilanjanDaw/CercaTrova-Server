from django.conf.urls import url
from login_server import views
""" End point URLs for User Profile Login, Registration, and Updation"""
urlpatterns = [
    url(r'^login_server/user/$', views.account_registration, name='user_list'),
    url(r'^login_server/account_authentication/$', views.validate_client, name='authenticate'),
    url(r'^login_server/update/$', views.update_account_information, name='update'),
]
