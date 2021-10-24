from django import template
from django.http.response import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.template import loader

from markdown import markdown
import re

# Create your views here.
NUMBER_OF_CANTOS: int = 34

def canto_index(request: WSGIRequest):

    template = loader.get_template('bots/canto_index.html')
    context = {
        'title': 'DANTE\'S INFERNO',
        'number_list': range(1,NUMBER_OF_CANTOS+1),
    }

    return HttpResponse(template.render(context, request))

def dantebot(request: WSGIRequest, canto: int = 1):

    path = 'bots/content/dantebot'
    english_file = f'{path}/canto_{canto}_en.md'
    italian_file = f'{path}/canto_{canto}_it.md'
    footnotes_file = f'{path}/canto_{canto}_en_footnotes.md'

    with open(english_file, 'r') as f:
        english = f.read()

    with open(italian_file, 'r') as f:
        italian = f.read()

    with open(footnotes_file, 'r') as f:
        footnotes = f.read()

    # Preprocessing
    english = re.sub('\[(\d*)\]', '[^\g<1>]', english)
    english = re.sub('\n\s\s(\S)', r'\n\n\g<1>', english) # Every triplet starts without indenting, use this to add whitespace
    footnotes = re.sub('\[(\d*)\]', '[^\g<1>]:', footnotes)

    marked_up_footnotes = f'{english}\n{footnotes}'

    # Link footnotes to English
    marked_up_footnotes = markdown(marked_up_footnotes, extensions=['footnotes'])
    splits = re.split(r'(?=<div class="footnote")', marked_up_footnotes)
    english = splits[0]
    footnotes = ''.join(splits[1])

    italian = markdown(italian)
    italian = re.sub('\n', '</br>', italian)
    english = re.sub('\n', '</br>', english)

    template = loader.get_template('bots/canto.html')
    context = {
        'title': f'CANTO {canto}' if canto != 0 else 'INTRODUCTION',
        'english': english,
        'italian': italian,
        'footnotes': footnotes,
        'preceding': canto - 1, # canto 0 is the intro
        'proceeding': canto + 1 if canto + 1 <= NUMBER_OF_CANTOS else False,
    }

    return HttpResponse(template.render(context, request))
