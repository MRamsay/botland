from django import template
from django.http.response import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.template import loader

from markdown import markdown
import re

# Create your views here.

def canto_index(request: WSGIRequest):
    template = loader.get_template('bots/canto_index.html')
    context = {
        'title': 'INFERNO',
        'number_list': range(1,33+1),
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

    marked_up_footnotes = f'''{english}
{footnotes}    
'''

    marked_up_footnotes = markdown(marked_up_footnotes, extensions=['footnotes'])

    splits = re.split(r'(<div class="footnote")', marked_up_footnotes)
    english = splits[0]
    footnotes = ''.join(splits[1:3])

    italian = markdown(italian)
    italian = re.sub('\n', '</br>', italian)
    english = re.sub('\n', '</br>', english)

    md_template = f'''
<table>
<tr>
<td>
{english}
</td>
<td>
{italian}
</td>
</table>

{footnotes}
'''

    # md_template = markdown(md_template, extensions=['footnotes', 'md_in_html']) # conversion to HTML

    template = loader.get_template('bots/test.html')
    context = {
        'title': 'CANTO 1',
        'content': md_template,
    }

    return HttpResponse(template.render(context, request))
