"""
Kemmering tag
"""


class tag(object):
    self_closing = False

    def __init__(self, tag, **attrs):
        if tag and tag.endswith('/'):
            self.self_closing = True
            tag = tag[:-1]
        self.tag = tag
        self.attrs = attrs
        self.children = ()

    def __call__(self, *children):
        def mkchild(x):
            if isinstance(x, str):
                x = text(x)
            x.parent = self
            return x
        self.children += tuple(mkchild(x) for x in children)
        return self

    def _bind(self, context):
        def bind(x):
            if hasattr(x, '_bind'):
                return x._bind(context)
            return x
        attrs = {k: bind(v) for k, v in self.attrs.items()}
        children = tuple(bind(child) for child in self.children)
        return type(self)(self.tag, **attrs)(*children)

    def __str__(self):
        return ''.join(self._stream())

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

    def __init__(self, *children):
        super(notag, self).__init__(None)
        self(*children)


class text(str):

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
