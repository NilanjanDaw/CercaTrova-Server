from django.conf.urls import url
from login_server import views

urlpatterns = [
    url(r'^login_server/user/$', views.account_registration),
    url(r'^login_server/account_authentication/$', views.account_authentication),
]
