from collections import OrderedDict


class tag(object):
    self_closing = False

    def __init__(self, tag, **attrs):
        if tag.endswith('/'):
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

    def __iter__(self):
        return iter(self.children)

    def render(self):
        return self.__str__()

    def __str__(self):
        return ''.join(self._stream())

    def __repr__(self):
        if self.self_closing and not self.children:
            return 'tag(%s)' % repr(self.tag + '/')

        if self.attrs:
            attrs = ', ' + ', '.join(
                ('%s=%s' % (k, repr(v)) for k, v in self.attrs.items())
            )
        else:
            attrs = ''

        children = ('(%s)' % ', '.join(map(repr, self.children))
                    if self.children else '')
        return 'tag(%s%s)%s' % (repr(self.tag), attrs, children)

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

        yield '<%s%s>' % (self.tag, attrs)
        for child in self.children:
            for x in child._stream():
                yield x
        yield '</%s>' % self.tag


class text(str):

    def _stream(self):
        yield self


class style(object):

    def __init__(self, *args):
        self.styles = OrderedDict()
        self(*args)

    def _stream(self):
        yield '\n<style>\n'
        for selector, style in self.styles.items():
            yield '{} {{\n'.format(selector)
            for k, v in style.items():
                yield '    {}: {};\n'.format(k, v)
            yield '}\n'
        yield '\n</style>\n'

    def __call__(self, *args):
        for selector, style in args:
            self.styles[selector] = style
