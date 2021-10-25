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
