import re
from markdown import Markdown
from io import StringIO
from typing import Text, Pattern


# Like all good work, lifted wholesale from https://stackoverflow.com/a/54923798
def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


# patching Markdown
Markdown.output_formats["plain"] = unmark_element
__md = Markdown(output_format="plain")
__md.stripTopLevelTags = False


def unmark(text):
    return __md.convert(text)


# Wholesale lifting ends


def readfile(path) -> Text:
    with open(path, 'r') as f:
        contents: Text = f.read()

    return contents


def strip_footnotes(text: Text) -> Text:
    english_footnote_re: Pattern = re.compile(r'\[(\d*)\]')
    text = re.sub(english_footnote_re, '', text)
    return text


def format_english_canto_for_twitter(content) -> Text:

    # Add a newline to each verse triplet
    # NOTE: Every verse triplet starts without indenting
    start_of_english_triplet_re: Pattern = re.compile(r'\n\s\s(\S)')
    an_extra_newline_re = r'\n\n\g<1>'
    content = re.sub(start_of_english_triplet_re, an_extra_newline_re, content)

    line_number_marker_re: Pattern = re.compile('\d{2,3}(\n|$)')
    content = re.sub(line_number_marker_re, '\n', content)

    content = unmark(strip_footnotes(content))
    content = re.sub('   ', '', content)
    content = re.sub('\n ', '\n', content)

    return content


ROMAN = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
]


def int_to_roman(number):
    result = []
    for (arabic, roman) in ROMAN:
        (factor, number) = divmod(number, arabic)
        result.append(roman * factor)
        if number == 0:
            break
    return "".join(result)


class RomanNumeral(int):

    def __str__(self) -> str:
        return int_to_roman(self)