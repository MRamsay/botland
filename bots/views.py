from django.http.response import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

# Create your views here.

def index(request: WSGIRequest):
    return HttpResponse('Hello There')
