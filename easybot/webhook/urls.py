
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^webhook', views.webhook),
    url(r'^manifest.json', views.manifest),
    url(r'^firebase-messaging-sw.js', views.fms),
]
