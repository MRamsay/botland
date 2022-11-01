from typing import Pattern
from django.http.response import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.template import loader
from bots.helpers import RomanNumeral

from markdown import markdown
import re

# Create your views here.
NUMBER_OF_CANTOS: int = 34


def index(request: WSGIRequest):

    template = loader.get_template('main/index.html')

    return HttpResponse(template.render({}, request))