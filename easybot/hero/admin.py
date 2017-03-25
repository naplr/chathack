import datetime

from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from .models import *
# We don't want other app that use this as reusable app to have these admin views (These view requires AdminPlus)

admin.site.register([Intent, Response, Entity])
