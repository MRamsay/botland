from django import template
from django.http.response import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.template import loader

from markdown import markdown

# Create your views here.

def index(request: WSGIRequest):

    with open('bots/content.md', 'r') as f:
        md = f.read()
        md = markdown(md) # conversion to HTML

    template = loader.get_template('bots/test.html')
    context = {
        'content': md,
    }
    
    return HttpResponse(template.render(context, request))
