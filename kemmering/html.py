"""
HTML tags

Reference: http://www.html-5-tutorial.com/all-html-tags.htm
"""
import sys

from collections import OrderedDict
from functools import partial
from xml.dom import minidom

from . import tag

PY2 = sys.version_info[0] == 2
strclass = unicode if PY2 else str    # nopep8


class style(object):

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


class doc(tag):

    def __init__(self, *children):
        super(doc, self).__init__(None)
        self(*children)

    def _stream(self):
        yield '<!DOCTYPE html>\n\n'
        for child in super(doc, self)._stream():
            yield child


def pretty(doc):
    xml = minidom.parseString(strclass(doc))
    return xml.toprettyxml(indent="  ").split('\n', 1)[1]


a = partial(tag, 'a')
abbr = partial(tag, 'abbr')
address = partial(tag, 'address')
area = partial(tag, 'area/')
article = partial(tag, 'article')
aside = partial(tag, 'aside')
audio = partial(tag, 'audio')
b = partial(tag, 'b')
base = partial(tag, 'base/')
bdi = partial(tag, 'bdi')
bdo = partial(tag, 'bdo')
blockquote = partial(tag, 'blockquote')
body = partial(tag, 'body')
br = partial(tag, 'br/')
button = partial(tag, 'button')
canvas = partial(tag, 'canvas')
caption = partial(tag, 'caption')
cite = partial(tag, 'cite')
code = partial(tag, 'code')
col = partial(tag, 'col/')
colgroup = partial(tag, 'colgroup')
datalist = partial(tag, 'datalist')
dd = partial(tag, 'dd')
del_ = partial(tag, 'del')
details = partial(tag, 'details')
dfn = partial(tag, 'dfn')
div = partial(tag, 'div')
dl = partial(tag, 'dl')
dt = partial(tag, 'dt')
em = partial(tag, 'em')
embed = partial(tag, 'embed/')
fieldset = partial(tag, 'fieldset')
figcaption = partial(tag, 'figcaption')
figure = partial(tag, 'figure')
footer = partial(tag, 'footer')
form = partial(tag, 'form')
h1 = partial(tag, 'h1')
h2 = partial(tag, 'h2')
h3 = partial(tag, 'h3')
h4 = partial(tag, 'h4')
h5 = partial(tag, 'h5')
h6 = partial(tag, 'h6')
head = partial(tag, 'head')
header = partial(tag, 'header')
hgroup = partial(tag, 'hgroup')
hr = partial(tag, 'hr/')
html = partial(tag, 'html')
i = partial(tag, 'i')
iframe = partial(tag, 'iframe')
img = partial(tag, 'img/')
input = partial(tag, 'input/')
ins = partial(tag, 'ins')
kbd = partial(tag, 'kbd')
keygen = partial(tag, 'keygen')
label = partial(tag, 'label')
legend = partial(tag, 'legend')
li = partial(tag, 'li')
link = partial(tag, 'link/')
map = partial(tag, 'map')
mark = partial(tag, 'mark')
menu = partial(tag, 'menu')
meta = partial(tag, 'meta/')
meter = partial(tag, 'meter')
nav = partial(tag, 'nav')
noscript = partial(tag, 'noscript')
object = partial(tag, 'object')
ol = partial(tag, 'ol')
optgroup = partial(tag, 'optgroup')
option = partial(tag, 'option')
output = partial(tag, 'output')
p = partial(tag, 'p')
param = partial(tag, 'param/')
pre = partial(tag, 'pre')
progress = partial(tag, 'progress')
q = partial(tag, 'q')
rp = partial(tag, 'rp')
rt = partial(tag, 'rt')
ruby = partial(tag, 'ruby')
s = partial(tag, 's')
samp = partial(tag, 'samp')
script = partial(tag, 'script')
section = partial(tag, 'section')
select = partial(tag, 'select')
small = partial(tag, 'small')
source = partial(tag, 'source/')
span = partial(tag, 'span')
strong = partial(tag, 'strong')
sub = partial(tag, 'sub')
summary = partial(tag, 'summary')
sup = partial(tag, 'sup')
table = partial(tag, 'table')
tbody = partial(tag, 'tbody')
td = partial(tag, 'td')
textarea = partial(tag, 'textarea')
tfoot = partial(tag, 'tfoot')
th = partial(tag, 'th')
thead = partial(tag, 'thead')
time = partial(tag, 'time')
title = partial(tag, 'title')
tr = partial(tag, 'tr')
track = partial(tag, 'track/')
u = partial(tag, 'u')
ul = partial(tag, 'ul')
var = partial(tag, 'var')
video = partial(tag, 'video')
wbr = partial(tag, 'wbr')
