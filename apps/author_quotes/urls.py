from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^quotes$', views.quotes),
    url(r'^logout$', views.logout),
    url(r'^myaccount/(?P<id>\d+)$', views.myaccount),
    url(r'^myaccount_errors$', views.myaccount_errors),
    url(r'^edit/(?P<id>\d+)$' , views.edit),
    url(r'^create/(?P<id>\d+)$', views.create),
    url(r'^show/(?P<id>\d+)$', views.show),
    url(r'^delete_quote/(?P<id>\d+)$', views.delete_quote),
    url(r'^like/(?P<id>\d+)$', views.like)
]