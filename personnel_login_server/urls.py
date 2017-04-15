from django.conf.urls import url
from personnel_login_server import views

urlpatterns = [
    url(r'^personnel_login_server/user/$', views.account_registration),
    url(r'^personnel_login_server/account_authentication/$', views.account_authentication),
    url(r'^personnel_login_server/update/$', views.update_account_information),
]
