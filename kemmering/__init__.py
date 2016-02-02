"""
Kemmering tag
"""
import sys

PY2 = sys.version_info[0] == 2
strbase = basestring if PY2 else str  # nopep8
strclass = unicode if PY2 else str    # nopep8


class tag(object):
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
        def bind(x):
            if hasattr(x, '_bind'):
                return x._bind(context)
            return x
        attrs = {k: bind(v) for k, v in self.attrs.items()}
        children = tuple(bind(child) for child in self.children)
        return self._copy(attrs, children)

    def _copy(self, attrs, children):
        cls = type(self)
        obj = cls.__new__(cls)
        obj._init(self.tag, attrs, children)
        return obj

    def __str__(self):
        return u''.join(self._stream())

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
            attrs = u' ' + u' '.join(
                (u'%s="%s"' % (k.rstrip(u'_'), v) for k, v in attrs.items())
            )
        else:
            attrs = u''

        if self.self_closing and not self.children:
            yield u'<%s%s/>' % (self.tag, attrs)
            return

        if self.tag:
            yield u'<%s%s>' % (self.tag, attrs)
        for child in self.children:
            for x in child._stream():
                yield x
        if self.tag:
            yield u'</%s>' % self.tag


class notag(tag):

    def __init__(self, *children):
        super(notag, self).__init__(None)
        self(*children)


_nothing = notag()


class text(strclass):

    def _stream(self):
        yield self


def bind(doc, context):
    return doc._bind(context)


class defer(object):

    def __init__(self, f):
        self.f = f

    def _bind(self, context):
        return self.f(context)

    def _stream(self):
        raise ValueError("Unbound defer, unable to stream.")

    def __repr__(self):
        return '{}({})'.format(
            type(self).__name__,
            getattr(self.f, '__name__', repr(self.f)))


class from_context(defer):

    def __init__(self, key, default=_nothing):
        self.key = key
        self.default = default

    def _bind(self, context):
        value = context.get(self.key, self.default)
        if value is _nothing:
            raise KeyError(self.key)
        return value

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, repr(self.key))


class in_context(defer):

    def __init__(self, keys, default=_nothing):
        self.keys = keys
        self.default = default

    def _bind(self, context):
        keys = self.keys
        while keys:
            key = keys[0]
            keys = keys[1:]
            context = context.get(key, _nothing)
            if context is _nothing:
                if self.default is _nothing:
                    raise KeyError(self.keys)
                return self.default
        return context

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, repr(self.keys))


class format_context(defer):

    def __init__(self, s):
        self.s = s

    def _bind(self, context):
        return self.s.format(**context)

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, repr(self.s))


class cond(defer):

    def __init__(self, condition, affirmative, negative=_nothing):
        self.condition = condition
        self.affirmative = affirmative
        self.negative = negative

    def _bind(self, context):
        if self.condition(context):
            return self.affirmative
        else:
            return self.negative

    def __repr__(self):
        return '{}({}, {}{})'.format(
            type(self).__name__,
            getattr(self.condition, '__name__', repr(self.condition)),
            repr(self.affirmative),
            '' if self.negative is _nothing else
            ', {}'.format(repr(self.negative))
        )


class loop(defer):

    def __init__(self, key, seq, template):
        self.key = key
        self.seq = seq
        self.template = template

    def _bind(self, context):
        seq = self.seq(context) if callable(self.seq) else context[self.seq]
        return notag(*(
            self.template._bind(assoc(context, self.key, value))
            for value in seq
        ))


def assoc(d, k, v):
    d = d.copy()
    d[k] = v
    return d
