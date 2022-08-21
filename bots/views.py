from typing import Pattern
from django.http.response import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.template import loader
from bots.helpers import RomanNumeral

from markdown import markdown
import re

# Create your views here.
NUMBER_OF_CANTOS: int = 34


def canto_index(request: WSGIRequest):

    cantos = range(1, NUMBER_OF_CANTOS + 1)

    template = loader.get_template('bots/canto_index.html')
    context = {
        'title': 'DANTE\'S INFERNO',
        'number_list': zip(list(cantos), [RomanNumeral(c) for c in cantos]),
    }

    return HttpResponse(template.render(context, request))


def dantebot(request: WSGIRequest, canto: int = 1):

    # --- Content load

    path = 'bots/content/dantebot'
    english_file = f'{path}/canto_{canto}_en.md'
    italian_file = f'{path}/canto_{canto}_it.md'
    footnotes_file = f'{path}/canto_{canto}_en_footnotes.md'

    with open(english_file, 'r') as f:
        english: str = f.read()

    with open(italian_file, 'r') as f:
        italian: str = f.read()

    with open(footnotes_file, 'r') as f:
        footnotes: str = f.read()

    # --- Preprocessing to get text display ready

    # Original Italian is easy to preprocess.
    italian = markdown(italian)
    # italian = re.sub('\n', '</br>', italian)

    # English translation w/ footnotes needs more work

    # Transform footnote style given into the markdown extension for footnotes style.
    # https://www.markdownguide.org/extended-syntax/#footnotes

    english_footnote_re: Pattern = re.compile(r'\[(\d*)\]')
    english_footnote_post_re = r'[^\g<1>]:'
    english = re.sub(english_footnote_re, english_footnote_post_re, english)
    footnotes = re.sub(english_footnote_re, english_footnote_post_re,
                       footnotes)

    # Add a newline to each verse triplet
    # NOTE: Every verse triplet starts without indenting
    # start_of_english_triplet_re: Pattern = re.compile(r'\n\s\s(\S)')
    # an_extra_newline_re = r'\n\n\g<1>'
    # english = re.sub(start_of_english_triplet_re, an_extra_newline_re, english)

    line_number_marker_re: Pattern = re.compile('\s*\d{2,3}(\n|$)')
    english = re.sub(line_number_marker_re, r'\n', english)

    marked_up_footnotes: str = f'{english}\n{footnotes}'

    # Links footnotes to English as well
    marked_up_footnotes = markdown(marked_up_footnotes,
                                   extensions=['footnotes'])

    english_footnote_splitpoint: Pattern = re.compile(
        r'(?=<div class="footnote")')
    splits = re.split(english_footnote_splitpoint, marked_up_footnotes)
    english, footnotes = splits

    # english = re.sub('\n', '</br>', english)
    # english = re.sub('</br>\n</br>', '</br>', english)

    if canto == 0:
        template = loader.get_template('bots/canto_intro.html')
        context = {
            'title': 'INTRODUCTION',
            'text': english,
            'footnotes': footnotes,
            'preceding': canto - 1,  # canto 0 is the intro
            'preceding_roman': RomanNumeral(canto - 1) if canto >= 2 else '',
            'proceeding':
            canto + 1 if canto + 1 <= NUMBER_OF_CANTOS else False,
            'proceeding_roman': RomanNumeral(canto + 1),
        }
    else:
        template = loader.get_template('bots/canto.html')

        lines = zip(italian.split('\n'), english.split('\n'))
        lines = [{
            'italian': line[0],
            'english': line[1],
        } for line in zip(italian.split('\n'), english.split('\n'))]

        context = {
            'title':
            f'CANTO {RomanNumeral(canto)}' if canto != 0 else 'INTRODUCTION',
            'lines': lines,
            'footnotes': footnotes,
            'preceding': canto - 1,  # canto 0 is the intro
            'preceding_roman': RomanNumeral(canto - 1) if canto >= 2 else '',
            'proceeding':
            canto + 1 if canto + 1 <= NUMBER_OF_CANTOS else False,
            'proceeding_roman': RomanNumeral(canto + 1),
        }

    return HttpResponse(template.render(context, request))
