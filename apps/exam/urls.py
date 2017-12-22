from django.conf.urls import url
from . import views        
urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.index),
    url(r'^regis$', views.regis),
    url(r'^login$', views.login),
    url(r'^travels$', views.travels),
    url(r'^logout$', views.logout),
    url(r'^add$', views.add),
    url(r'^createplans$', views.createplans),
    url(r'^travels/join/(?P<planid>\d+)$', views.join),
    url(r'^travels/destination/(?P<planid>\d+)$', views.showuser),

    ]
