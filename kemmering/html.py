"""
HTML tags

Reference: http://www.html-5-tutorial.com/all-html-tags.htm
"""
import sys

from collections import OrderedDict
from xml.dom import minidom

from . import tag

PY2 = sys.version_info[0] == 2
strclass = unicode if PY2 else str    # nopep8

__all__ = ['doc', 'style', 'pretty']


class doc(tag):
    """
    Top level HTML5 document, includes doctype declaration.

    .. doctest:: api-doc

       >>> from kemmering.html import doc, html
       >>> print(doc(html()))
       <!DOCTYPE html>
       <BLANKLINE>
       <html></html>
    """

    def __init__(self, *children):
        super(doc, self).__init__(None)
        self(*children)

    def _stream(self):
        yield '<!DOCTYPE html>\n\n'
        for child in super(doc, self)._stream():
            yield child


class style(object):
    """
    HTML tag <style></style>.

    Each positional argument should be a tuple of `(selector, style)` where
    `selector` is the CSS selector and `style` is a dictionary containing the
    CSS styles for that selector.  Calling the resulting object uses the same
    signature and adds those styles to this tag.

    .. doctest:: api-style

       >>> from kemmering.html import style
       >>> print(style(
       ...     ('a', {'b': 'c', }),
       ...     ('d', {'e': 'f'})))
       <BLANKLINE>
       <style>
         a {
           b: c;
         }
         d {
           e: f;
         }
       </style>
       <BLANKLINE>
    """

    def __init__(self, *args):
        self.styles = OrderedDict()
        self(*args)

    def _stream(self):
        yield '\n<style>\n'
        for selector, style in self.styles.items():
            yield '  {} {{\n'.format(selector)
            for k, v in style.items():
                yield '    {}: {};\n'.format(k, v)
            yield '  }\n'
        yield '</style>\n'

    def __call__(self, *args):
        for selector, style in args:
            self.styles[selector] = style

    def __str__(self):
        return ''.join(self._stream())

    __unicode__ = __str__


def pretty(snippet):
    """
    Render a snippet of HTML as a string with line breaks and indentation.
    This is not necessarily a particularly fast implementation, but it can be
    useful for debugging.

    .. doctest:: api-pretty

       >>> from kemmering import tag
       >>> from kemmering.html import pretty
       >>> print(pretty(tag('a')(tag('b')(tag('c/')))))
       <a>
         <b>
           <c/>
         </b>
       </a>
       <BLANKLINE>
    """
    xml = minidom.parseString(strclass(snippet))
    return xml.toprettyxml(indent="  ").split('\n', 1)[1]


def _htmltag(_tag, name=None):
    def _inner(**attrs):
        return tag(_tag, **attrs)
    closing = _tag.endswith('/')
    __all__.append(name if name else _tag.rstrip('/'))
    _inner.__name__ = _tag
    _inner.__doc__ = (
        "HTML tag <{0}>".format(_tag)
        if closing else
        "HTML tag <{0}></{0}>".format(_tag))
    return _inner


a = _htmltag('a')
abbr = _htmltag('abbr')
address = _htmltag('address')
area = _htmltag('area/')
article = _htmltag('article')
aside = _htmltag('aside')
audio = _htmltag('audio')
b = _htmltag('b')
base = _htmltag('base/')
bdi = _htmltag('bdi')
bdo = _htmltag('bdo')
blockquote = _htmltag('blockquote')
body = _htmltag('body')
br = _htmltag('br/')
button = _htmltag('button')
canvas = _htmltag('canvas')
caption = _htmltag('caption')
cite = _htmltag('cite')
code = _htmltag('code')
col = _htmltag('col/')
colgroup = _htmltag('colgroup')
datalist = _htmltag('datalist')
dd = _htmltag('dd')
del_ = _htmltag('del', 'del_')
details = _htmltag('details')
dfn = _htmltag('dfn')
div = _htmltag('div')
dl = _htmltag('dl')
dt = _htmltag('dt')
em = _htmltag('em')
embed = _htmltag('embed/')
fieldset = _htmltag('fieldset')
figcaption = _htmltag('figcaption')
figure = _htmltag('figure')
footer = _htmltag('footer')
form = _htmltag('form')
h1 = _htmltag('h1')
h2 = _htmltag('h2')
h3 = _htmltag('h3')
h4 = _htmltag('h4')
h5 = _htmltag('h5')
h6 = _htmltag('h6')
head = _htmltag('head')
header = _htmltag('header')
hgroup = _htmltag('hgroup')
hr = _htmltag('hr/')
html = _htmltag('html')
i = _htmltag('i')
iframe = _htmltag('iframe')
img = _htmltag('img/')
input = _htmltag('input/')
ins = _htmltag('ins')
kbd = _htmltag('kbd')
keygen = _htmltag('keygen')
label = _htmltag('label')
legend = _htmltag('legend')
li = _htmltag('li')
link = _htmltag('link/')
map = _htmltag('map')
mark = _htmltag('mark')
menu = _htmltag('menu')
meta = _htmltag('meta/')
meter = _htmltag('meter')
nav = _htmltag('nav')
noscript = _htmltag('noscript')
object = _htmltag('object')
ol = _htmltag('ol')
optgroup = _htmltag('optgroup')
option = _htmltag('option')
output = _htmltag('output')
p = _htmltag('p')
param = _htmltag('param/')
pre = _htmltag('pre')
progress = _htmltag('progress')
q = _htmltag('q')
rp = _htmltag('rp')
rt = _htmltag('rt')
ruby = _htmltag('ruby')
s = _htmltag('s')
samp = _htmltag('samp')
script = _htmltag('script')
section = _htmltag('section')
select = _htmltag('select')
small = _htmltag('small')
source = _htmltag('source/')
span = _htmltag('span')
strong = _htmltag('strong')
sub = _htmltag('sub')
summary = _htmltag('summary')
sup = _htmltag('sup')
table = _htmltag('table')
tbody = _htmltag('tbody')
td = _htmltag('td')
textarea = _htmltag('textarea')
tfoot = _htmltag('tfoot')
th = _htmltag('th')
thead = _htmltag('thead')
time = _htmltag('time')
title = _htmltag('title')
tr = _htmltag('tr')
track = _htmltag('track/')
u = _htmltag('u')
ul = _htmltag('ul')
var = _htmltag('var')
video = _htmltag('video')
wbr = _htmltag('wbr')
