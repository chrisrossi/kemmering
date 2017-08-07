import pytest
import sys

PY2 = sys.version_info[0] == 2
STR = unicode if PY2 else str  # nopep8
if PY2:
    def REPR(o):
        return repr(o).replace('u"', '"').replace("u'", "'")
else:
    REPR = repr


def test_tag():
    from kemmering import tag
    assert STR(tag('hello')) == '<hello></hello>'


def test_tag_non_ascii():
    from kemmering import tag
    assert STR(tag(u'h\u03b5llo')) == u'<h\u03b5llo></h\u03b5llo>'


def test_tag_repr():
    from kemmering import tag
    assert REPR(tag('hello')) == "tag('hello')"


def test_tag_with_text():
    from kemmering import tag
    assert STR(tag('hello')('world')) == '<hello>world</hello>'


def test_tag_with_text_escape():
    from kemmering import tag
    assert STR(tag('hello')('kith & kin > 0')) == (
        '<hello>kith &amp; kin &gt; 0</hello>')


def test_tag_with_text_non_ascii():
    from kemmering import tag
    assert STR(tag('hello')(u'w\u03bfrld')) == u'<hello>w\u03bfrld</hello>'


def test_tag_with_text_repr():
    from kemmering import tag
    assert REPR(tag('hello')('world')) == "tag('hello')('world')"


def test_nested_tags():
    from kemmering import tag
    assert STR(tag('a')(tag('b/'))) == '<a><b/></a>'


def test_nested_tags_repr():
    from kemmering import tag
    assert REPR(tag('a')(tag('b/'))) == "tag('a')(tag('b/'))"


def test_tag_with_attributes():
    from kemmering import tag
    result = STR(tag('a/', foo='bar', bar='baz'))
    assert (result == '<a foo="bar" bar="baz"/>' or
            result == '<a bar="baz" foo="bar"/>')


def test_tag_with_attributes_non_ascii():
    from kemmering import tag
    result = STR(tag('a/', foo=u'b\u03b1r', bar='baz'))
    assert (result == u'<a foo="b\u03b1r" bar="baz"/>' or
            result == u'<a bar="baz" foo="b\u03b1r"/>')


def test_tag_with_attributes_repr():
    from kemmering import tag
    result = REPR(tag('a/', foo='bar', bar='baz'))
    assert (result == "tag('a/', foo='bar', bar='baz')" or
            result == "tag('a/', bar='baz', foo='bar')")


def test_tag_with_reserved_word_attributes():
    from kemmering import tag
    assert STR(tag('a/', class_='foo')) == '<a class="foo"/>'


def test_tag_with_reserved_word_attributes_repr():
    from kemmering import tag
    assert REPR(tag('a/', class_='foo')) == "tag('a/', class_='foo')"


def test_defer():
    from kemmering import bind, defer, tag

    @defer
    def deferred(context):
        return tag('p')('Hello {}!'.format(context['name']))
    doc = tag('doc')(deferred, 'foo')
    assert REPR(doc) == "tag('doc')(defer(deferred), 'foo')"
    with pytest.raises(ValueError):
        STR(doc)
    bound = bind(doc, {'name': 'Fred'})
    assert STR(bound) == '<doc><p>Hello Fred!</p>foo</doc>'


def test_defer_attribute():
    from kemmering import bind, defer, tag

    @defer
    def deferred(context):
        return 'Hello {}!'.format(context['name'])
    doc = tag('doc', foo=deferred)('woot')
    assert REPR(doc) == "tag('doc', foo=defer(deferred))('woot')"
    bound = bind(doc, {'name': 'Fred'})
    assert STR(bound) == '<doc foo="Hello Fred!">woot</doc>'


def test_defer_remove_attribute():
    from kemmering import bind, defer, tag

    @defer
    def deferred(context):
        return None
    doc = tag('doc', foo=deferred)('woot')
    assert REPR(doc) == "tag('doc', foo=defer(deferred))('woot')"
    bound = bind(doc, {'name': 'Fred'})
    assert STR(bound) == '<doc>woot</doc>'


def test_defer_with_notag():
    from kemmering import bind, defer, notag, tag

    @defer
    def deferred(context):
        return notag(
            tag('p')('Hello {}!'.format(context['name'])),
            tag('p')('Nice to meet you!'),
            tag('br/'),
        )
    doc = tag('doc')(deferred, 'foo')
    assert REPR(doc) == "tag('doc')(defer(deferred), 'foo')"
    with pytest.raises(ValueError):
        STR(doc)
    bound = bind(doc, {'name': 'Fred'})
    assert STR(bound) == ('<doc><p>Hello Fred!</p>'
                          '<p>Nice to meet you!</p><br/>foo</doc>')
    assert REPR(bound) == ("tag('doc')(notag(tag('p')('Hello Fred!'), "
                           "tag('p')('Nice to meet you!'), tag('br/')), "
                           "'foo')")


def test_from_context():
    from kemmering import bind, from_context, tag

    doc = tag('doc')(
        tag('p')('Hello ', from_context('name'), '!'), 'foo')
    assert REPR(doc) == ("tag('doc')(tag('p')"
                         "('Hello ', from_context('name'), '!'), 'foo')")
    with pytest.raises(ValueError):
        STR(doc)
    bound = bind(doc, {'name': 'Fred'})
    assert STR(bound) == '<doc><p>Hello Fred!</p>foo</doc>'


def test_from_context_key_error():
    from kemmering import bind, from_context, tag

    doc = tag('doc')(
        tag('p')('Hello ', from_context('name'), '!'), 'foo')
    with pytest.raises(KeyError):
        bind(doc, {})


def test_from_context_use_default():
    from kemmering import bind, from_context, tag

    doc = tag('doc')(
        tag('p')('Hello ', from_context('name', 'World'), '!'), 'foo')
    assert REPR(doc) == ("tag('doc')(tag('p')"
                         "('Hello ', from_context('name'), '!'), 'foo')")
    with pytest.raises(ValueError):
        STR(doc)
    bound = bind(doc, {})
    assert STR(bound) == '<doc><p>Hello World!</p>foo</doc>'


def test_in_context():
    from kemmering import bind, in_context, tag

    doc = tag('doc')(
        tag('p')('Hello ', in_context(['user', 'name']), '!'), 'foo')
    assert REPR(doc) == ("tag('doc')(tag('p')"
                         "('Hello ', in_context(['user', 'name']), '!'),"
                         " 'foo')")
    with pytest.raises(ValueError):
        STR(doc)
    bound = bind(doc, {'user': {'name': 'Fred'}})
    assert STR(bound) == '<doc><p>Hello Fred!</p>foo</doc>'


def test_in_context_key_error():
    from kemmering import bind, in_context, tag

    doc = tag('doc')(
        tag('p')('Hello ', in_context(['user', 'name']), '!'), 'foo')
    assert REPR(doc) == ("tag('doc')(tag('p')"
                         "('Hello ', in_context(['user', 'name']), '!'),"
                         " 'foo')")
    with pytest.raises(ValueError):
        STR(doc)
    with pytest.raises(KeyError):
        bind(doc, {'user': {}})


def test_in_context_use_default():
    from kemmering import bind, in_context, tag

    doc = tag('doc')(
        tag('p')('Hello ', in_context(['user', 'name'], 'World'), '!'), 'foo')
    assert REPR(doc) == ("tag('doc')(tag('p')"
                         "('Hello ', in_context(['user', 'name']), '!'),"
                         " 'foo')")
    with pytest.raises(ValueError):
        STR(doc)
    bound = bind(doc, {})
    assert STR(bound) == '<doc><p>Hello World!</p>foo</doc>'


def test_format_context():
    from kemmering import bind, format_context, tag

    doc = tag('doc')(tag('p')(format_context('Hello {name}!')), 'foo')
    assert REPR(doc) == ("tag('doc')(tag('p')"
                         "(format_context('Hello {name}!')), 'foo')")
    with pytest.raises(ValueError):
        STR(doc)
    bound = bind(doc, {'name': 'Fred'})
    assert STR(bound) == '<doc><p>Hello Fred!</p>foo</doc>'


def test_cond():
    from kemmering import bind, cond, tag

    def is_admin(context):
        return context['user'] == 'admin'
    doc = tag('doc')(cond(is_admin,
                          tag('p')('At your service!'),
                          tag('p')('Go away!')))
    assert REPR(doc) == (
        "tag('doc')(cond(is_admin, "
        "tag('p')('At your service!'), "
        "tag('p')('Go away!')))")
    with pytest.raises(ValueError):
        STR(doc)
    bound = bind(doc, {'user': 'admin'})
    assert STR(bound) == '<doc><p>At your service!</p></doc>'
    bound = bind(doc, {'user': 'grunt'})
    assert STR(bound) == '<doc><p>Go away!</p></doc>'


def test_cond_key_condition():
    from kemmering import bind, cond, tag

    doc = tag('doc')(cond('admin',
                          tag('p')('At your service!'),
                          tag('p')('Go away!')))
    assert REPR(doc) == (
        "tag('doc')(cond('admin', "
        "tag('p')('At your service!'), "
        "tag('p')('Go away!')))")
    with pytest.raises(ValueError):
        STR(doc)
    bound = bind(doc, {'admin': True})
    assert STR(bound) == '<doc><p>At your service!</p></doc>'
    bound = bind(doc, {'admin': False})
    assert STR(bound) == '<doc><p>Go away!</p></doc>'


def test_cond_no_negative():
    from kemmering import bind, cond, tag

    def is_admin(context):
        return context['user'] == 'admin'
    doc = tag('doc')(tag('p')('Hi there.', cond(
        is_admin, ' How do you do?')))
    assert REPR(doc) == (
        "tag('doc')(tag('p')('Hi there.', cond("
        "is_admin, ' How do you do?')))")
    with pytest.raises(ValueError):
        STR(doc)
    bound = bind(doc, {'user': 'admin'})
    assert STR(bound) == '<doc><p>Hi there. How do you do?</p></doc>'
    bound = bind(doc, {'user': 'grunt'})
    assert STR(bound) == '<doc><p>Hi there.</p></doc>'


def test_cond_deferred_children():
    from kemmering import bind, cond, tag, format_context

    def is_admin(context):
        return context['user'] == 'admin'
    doc = tag('doc')(tag('p')('Hi there.', cond(
        is_admin, format_context(' Hi {user}!'))))
    assert REPR(doc) == (
        "tag('doc')(tag('p')('Hi there.', cond("
        "is_admin, format_context(' Hi {user}!'))))")
    with pytest.raises(ValueError):
        STR(doc)
    bound = bind(doc, {'user': 'admin'})
    assert STR(bound) == '<doc><p>Hi there. Hi admin!</p></doc>'
    bound = bind(doc, {'user': 'grunt'})
    assert STR(bound) == '<doc><p>Hi there.</p></doc>'


def test_loop():
    from kemmering import bind, from_context, loop, tag

    doc = tag('doc', foo=from_context('foo'))(
        tag('ul')(
            loop('foo', 'animals',
                 tag('li')(from_context('foo')))),
        'foo is ', from_context('foo'),
    )
    with pytest.raises(ValueError):
        STR(doc)
    bound = bind(doc, {'animals': ['kitty', 'puppy', 'bunny'],
                       'foo': 'bar'})
    assert STR(bound) == (
        '<doc foo="bar"><ul>'
        '<li>kitty</li><li>puppy</li><li>bunny</li>'
        '</ul>foo is bar</doc>')


def test_loop_seq_callable():
    from kemmering import bind, from_context, loop, tag

    def animals(context):
        yield 'kitty'
        yield 'puppy'
        yield 'bunny'

    doc = tag('doc', foo=from_context('foo'))(
        tag('ul')(
            loop('foo', animals,
                 tag('li')(from_context('foo')))),
        'foo is ', from_context('foo'),
    )
    with pytest.raises(ValueError):
        STR(doc)
    bound = bind(doc, {'foo': 'bar'})
    assert STR(bound) == (
        '<doc foo="bar"><ul>'
        '<li>kitty</li><li>puppy</li><li>bunny</li>'
        '</ul>foo is bar</doc>')


def test_loop_unpack():
    from kemmering import bind, cond, from_context, loop, tag

    def animals(context):
        return enumerate(('kitty', 'puppy', 'bunny'))

    def is_even(context):
        return context['i'] % 2 == 0

    doc = tag('doc', foo=from_context('foo'))(
        tag('ul')(
            loop(('i', 'foo'), animals,
                 tag('li', class_=cond(is_even, 'even', 'odd'))(
                     from_context('foo')))),
        'foo is ', from_context('foo'),
    )
    with pytest.raises(ValueError):
        STR(doc)
    bound = bind(doc, {'foo': 'bar'})
    assert STR(bound) == (
        '<doc foo="bar"><ul>'
        '<li class="even">kitty</li>'
        '<li class="odd">puppy</li>'
        '<li class="even">bunny</li>'
        '</ul>foo is bar</doc>')


def test_loop_unpack_too_many():
    from kemmering import bind, cond, from_context, loop, tag

    def animals(context):
        return enumerate(('kitty', 'puppy', 'bunny'))

    def is_even(context):
        return context['i'] % 2 == 0

    doc = tag('doc', foo=from_context('foo'))(
        tag('ul')(
            loop(('i',), animals,
                 tag('li', class_=cond(is_even, 'even', 'odd'))(
                     from_context('foo')))),
        'foo is ', from_context('foo'),
    )
    with pytest.raises(ValueError):
        STR(doc)
    with pytest.raises(ValueError):
        bind(doc, {'foo': 'bar'})


def test_loop_unpack_not_enough():
    from kemmering import bind, cond, from_context, loop, tag

    def animals(context):
        return enumerate(('kitty', 'puppy', 'bunny'))

    def is_even(context):
        return context['i'] % 2 == 0

    doc = tag('doc', foo=from_context('foo'))(
        tag('ul')(
            loop(('i', 'foo', 'bar'), animals,
                 tag('li', class_=cond(is_even, 'even', 'odd'))(
                     from_context('foo')))),
        'foo is ', from_context('foo'),
    )
    with pytest.raises(ValueError):
        STR(doc)
    with pytest.raises(ValueError):
        bind(doc, {'foo': 'bar'})
