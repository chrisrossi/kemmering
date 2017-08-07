import sys
from xml.sax.saxutils import escape


PY2 = sys.version_info[0] == 2
strbase = basestring if PY2 else str  # nopep8
strclass = unicode if PY2 else str    # nopep8


class tag(object):
    """
    An XML tag.

    `tag` is the name of the tag.  Add a trailing forward slash (`/`) character
    to create a self-closing tag.  `attrs` are the attributes for tag.  The tag
    itself is callable.  Call the tag to add children.

    .. doctest:: api-tag

       >>> from kemmering import tag
       >>> str(tag('a', b='c')('d'))
       '<a b="c">d</a>'
       >>> str(tag('e/'))
       '<e/>'

    """
    self_closing = False

    def __init__(self, tag, **attrs):
        self._init(tag, attrs, ())

    def _init(self, tag, attrs, children):
        if tag and tag.endswith('/'):
            self.self_closing = True
            tag = tag[:-1]
        self.tag = tag
        self.attrs = {k: v for k, v in attrs.items()
                      if v is not None}
        self.children = ()
        self._extend(*children)

    def _extend(self, *children):
        def mkchild(x):
            if isinstance(x, strbase):
                x = text(x)
            x.parent = self
            return x
        self.children += tuple(mkchild(x) for x in children)
        return self

    __call__ = _extend

    def _bind(self, context):
        attrs = {k: bind(v, context) for k, v in self.attrs.items()}
        children = tuple(bind(child, context) for child in self.children)
        return self._copy(attrs, children)

    def _copy(self, attrs, children):
        cls = type(self)
        obj = cls.__new__(cls)
        obj._init(self.tag, attrs, children)
        obj.self_closing = self.self_closing
        return obj

    def __str__(self):
        return ''.join(self._stream())

    __unicode__ = __str__

    def __repr__(self):
        if self.attrs:
            attrs = ', ' + ', '.join(
                ('%s=%s' % (k, repr(v)) for k, v in self.attrs.items())
            )
        else:
            attrs = ''

        if self.self_closing and not self.children:
            return 'tag({}{})'.format(repr(self.tag + '/'), attrs)

        children = ('(%s)' % ', '.join(map(repr, self.children))
                    if self.children else '')
        if self.tag:
            return 'tag(%s%s)%s' % (repr(self.tag), attrs, children)
        else:
            return 'notag{}'.format(children)

    def _stream(self):
        attrs = {k: v for k, v in self.attrs.items()}
        if attrs:
            attrs = ' ' + ' '.join(
                ('%s="%s"' % (k.rstrip('_'), v) for k, v in attrs.items())
            )
        else:
            attrs = ''

        if self.self_closing and not self.children:
            yield '<%s%s/>' % (self.tag, attrs)
            return

        if self.tag:
            yield '<%s%s>' % (self.tag, attrs)
        for child in self.children:
            for x in child._stream():
                yield x
        if self.tag:
            yield '</%s>' % self.tag


class notag(tag):
    """
    Used to represent a set of sibling elements with no enclosing parent tag.

    `children` is a sequence of elements.

    `notag` is particularly useful with `defer` and any of the template
    helpers which are based on `defer`.

    .. doctest:: api-notag

       >>> from kemmering import notag, tag
       >>> str(tag('a')(
       ...   tag('b/'),
       ...   notag(
       ...      tag('c/'),
       ...      tag('d/')
       ...   )
       ... ))
       '<a><b/><c/><d/></a>'

    """

    def __init__(self, *children):
        super(notag, self).__init__(None)
        self(*children)


_nothing = notag()


class text(strclass):

    def _stream(self):
        yield escape(self)


def bind(template, context):
    """
    Realize a template by binding it to a context.

    `template` is a `tag` instance which should contain some instances of
    `defer` in its structure.  `context` is the context object that is passed
    to deferred functions in the template.  Most template helpers assume the
    context is a dictionary.

    Returns new `tag` instance that is a copy of the template with any
    deferred elements replaced by the return values of their deferred
    functions.
    """
    if hasattr(template, '_bind'):
        template = template._bind(context)
    return template


class defer(object):
    """
    Defer the realization of a part of a template until a later time.

    Use of a deferred function in a snippet comprised of `tag` objects, turns
    that snippet into a template.  That template is said to be realized when
    `bind` is called on the snippet, which generates a concrete snippet based
    on the template and a context passed in via `bind`.

    `f` is a function with the signature:

    .. code-block:: python

       def deferred(context):
           "Return a `tag`, `notag`, or string."

    The function will be called at realization time when `bind` is called on
    the containing snippet and passed the context object.  Most template
    helpers assume the context is a dictionary.

    Instances of `defer` may be used as children of `tag` objects or as values
    of tag atrributes.  When used as a child of a tag, the return value should
    be either another `tag` instance or a string for a text element.  When used
    as an attribute value, the return value should be a string or `None`.
    Setting an attribute to `None` causes it to be omitted from the realized
    template.

    Most use cases for `defer` are actually covered by more specific helpers
    based on `defer`, described below.
    """

    def __init__(self, f):
        self.f = f

    def _bind(self, context):
        return bind(self.f(context), context)

    def _stream(self):
        raise ValueError("Unbound defer, unable to stream.")

    def __repr__(self):
        return '{}({})'.format(
            type(self).__name__,
            getattr(self.f, '__name__', repr(self.f)))


class from_context(defer):
    """
    This specialization of `defer` simply returns a value from the bind
    context.

    `key` is the name to look up in the bind context dictionary.  Whatever is
    the value in the bind context is returned.  If `default` is specified and
    `key` is not found in the bind context, `default` is returned instead.

    .. doctest:: api-from_context

       >>> from kemmering import bind, from_context, tag
       >>> template = tag('a')(from_context('b', 'c'))
       >>> str(bind(template, {'b': 'd'}))
       '<a>d</a>'
       >>> str(bind(template, {}))
       '<a>c</a>'
    """

    def __init__(self, key, default=_nothing):
        self.key = key
        self.default = default

    def _bind(self, context):
        value = context.get(self.key, self.default)
        if value is _nothing:
            raise KeyError(self.key)
        return bind(value, context)

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, repr(self.key))


class in_context(defer):
    """
    This specialization of `defer` looks up a value in the bind context by
    traversing the context using a sequence of keys where the bind context is
    presumed to be a structure of nested dictionaries.

    `keys` is a sequence of names to look up, in order, in the bind context.
    If `default` is specified and a value is not found in the bind context for
    the given keys, `default` is returned instead.

    .. doctest:: api-in_context

       >>> from kemmering import bind, in_context, tag
       >>> template = tag('a')(in_context(['b', 'c'], 'd'))
       >>> str(bind(template, {'b': {'c': 'e'}}))
       '<a>e</a>'
       >>> str(bind(template, {}))
       '<a>d</a>'
    """

    def __init__(self, keys, default=_nothing):
        self.keys = keys
        self.default = default

    def _bind(self, context):
        value = context
        keys = self.keys
        while keys:
            key = keys[0]
            keys = keys[1:]
            value = value.get(key, _nothing)
            if value is _nothing:
                if self.default is _nothing:
                    raise KeyError(self.keys)
                return self.default
        return bind(value, context)

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, repr(self.keys))


class format_context(defer):
    """
    This specialization of `defer` uses the bind context to perform Python
    string formatting on a format string.

    `s` is the format string.  The return value is the equivalent of
    `s.format(**context)`.

    .. doctest:: api-format_context

       >>> from kemmering import bind, format_context, tag
       >>> template = tag('a')(format_context('{b} {c}'))
       >>> str(bind(template, {'b': 'd', 'c': 'e'}))
       '<a>d e</a>'
    """

    def __init__(self, s):
        self.s = s

    def _bind(self, context):
        return self.s.format(**context)

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, repr(self.s))


class cond(defer):
    """
    This specialization of `defer` conditionally includes an element based
    on the bind context.

    `condition` is a function which accepts a single argument, `context` and
    returns a boolean.  `condition` may optionally be a string, in which case
    it is used as a key for performing a dictionary lookup in the bind context,
    the value of which will be treated as a boolean.

    `affirmative` is the return value if the condition is `True`.  `negative`
    is the return value of the condition is `False`.  If the condition is
    `False` and no `negative` value is given, this element is elided from the
    realized snippet.

    .. doctest:: api-cond

       >>> from kemmering import bind, cond, tag
       >>> def has_b(context):
       ...     return 'b' in context
       >>> template = tag('a')(cond(has_b, 'b'))
       >>> str(bind(template, {'b': ''}))
       '<a>b</a>'
       >>> str(bind(template, {}))
       '<a></a>'
       >>> template = tag('a')(cond('b', 'c', 'd'))
       >>> str(bind(template, {'b': True}))
       '<a>c</a>'
       >>> str(bind(template, {}))
       '<a>d</a>'
    """

    def __init__(self, condition, affirmative, negative=_nothing):
        self.cond = condition
        self.yes = affirmative
        self.no = negative

    def _bind(self, context):
        cond = self.cond
        cond = cond(context) if callable(cond) else context.get(cond, False)
        return bind(self.yes, context) if cond else bind(self.no, context)

    def __repr__(self):
        return '{}({}, {}{})'.format(
            type(self).__name__,
            getattr(self.cond, '__name__', repr(self.cond)),
            repr(self.yes),
            '' if self.no is _nothing else
            ', {}'.format(repr(self.no))
        )


class loop(defer):
    """
    This specialization of `defer` repeats a snippet while iterating over a
    sequence.

    `key` is the name of a key that will be added to the context on each
    iteration whose value is the current item in the sequence. This makes the
    current item available to deferred functions in the repeated snippet. `key`
    may optionally be a `list` or `tuple` of string key names, in which case
    the sequence values, which should be sequences of equal length, will be
    unpacked into those keys.

    `seq` is a function which accepts a single argument, `context`, and returns
    an iterable sequence.  Alternatively, `seq` can be the name of a key in the
    current context whose value is an iterable sequence.

    `template` is the snippet to be repeated.

    .. doctest:: api-loop

       >>> from kemmering import bind, from_context, loop, tag
       >>> def fruits(context):
       ...     return ['apple', 'pear', 'banana']
       >>> template = tag('ul')(
       ...     loop('fruit', fruits, tag('li')(from_context('fruit'))))
       >>> str(bind(template, {'fruit': 'hamburger'}))
       '<ul><li>apple</li><li>pear</li><li>banana</li></ul>'
       >>> template = tag('ul')(
       ...     loop('fruit', 'fruits', tag('li')(from_context('fruit'))))
       >>> str(bind(template, {'fruits': ['apple', 'pear', 'banana']}))
       '<ul><li>apple</li><li>pear</li><li>banana</li></ul>'

    And an example which uses unpacking:

    .. doctest:: api-loop

       >>> from kemmering import cond
       >>> from kemmering.html import pretty
       >>> def fruits(context):
       ...     return enumerate(['apple', 'pear', 'banana'])
       >>> def is_even(context):
       ...     return context['i'] % 2 == 0
       >>> template = tag('ul')(
       ...     loop(('i', 'fruit'), fruits,
       ...         tag('li', class_=cond(is_even, 'even', 'odd'))(
       ...             from_context('fruit'))))
       >>> print(pretty(bind(template, {})))
       <ul>
         <li class="even">apple</li>
         <li class="odd">pear</li>
         <li class="even">banana</li>
       </ul>
       <BLANKLINE>
    """

    def __init__(self, key, seq, template):
        self.key = key
        self.seq = seq
        self.template = template

    def _bind(self, context):
        def subcontext(value):
            sub = context.copy()
            if isinstance(self.key, (list, tuple)):
                _check_unpack(len(self.key), len(value))
                sub.update({k: v for k, v in zip(self.key, value)})
            else:
                sub[self.key] = value
            return sub

        seq = self.seq(context) if callable(self.seq) else context[self.seq]
        return notag(*(
            bind(self.template, subcontext(value))
            for value in seq
        ))


def _check_unpack(expected, got):
    if got < expected:
        raise ValueError(
            'not enough values to unpack (expected {},  got {}'.format(
                expected, got))
    elif got > expected:
        raise ValueError(
            'too many values to unpack (expected {})'.format(
                expected))
