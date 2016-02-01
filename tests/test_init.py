import pytest


def test_tag():
    from kemmering import tag
    assert str(tag('hello')) == '<hello></hello>'


def test_tag_repr():
    from kemmering import tag
    assert repr(tag('hello')) == "tag('hello')"


def test_tag_with_text():
    from kemmering import tag
    assert str(tag('hello')('world')) == '<hello>world</hello>'


def test_tag_with_text_repr():
    from kemmering import tag
    assert repr(tag('hello')('world')) == "tag('hello')('world')"


def test_nested_tags():
    from kemmering import tag
    assert str(tag('a')(tag('b/'))) == '<a><b/></a>'


def test_nested_tags_repr():
    from kemmering import tag
    assert repr(tag('a')(tag('b/'))) == "tag('a')(tag('b/'))"


def test_tag_with_attributes():
    from kemmering import tag
    result = str(tag('a/', foo='bar', bar='baz'))
    assert (result == '<a foo="bar" bar="baz"/>' or
            result == '<a bar="baz" foo="bar"/>')


def test_tag_with_attributes_repr():
    from kemmering import tag
    result = repr(tag('a/', foo='bar', bar='baz'))
    assert (result == "tag('a/', foo='bar', bar='baz')" or
            result == "tag('a/', bar='baz', foo='bar')")


def test_tag_with_reserved_word_attributes():
    from kemmering import tag
    assert str(tag('a/', class_='foo')) == '<a class="foo"/>'


def test_tag_with_reserved_word_attributes_repr():
    from kemmering import tag
    assert repr(tag('a/', class_='foo')) == "tag('a/', class_='foo')"


def test_defer():
    from kemmering import bind, defer, tag

    @defer
    def deferred(context):
        return tag('p')('Hello {}!'.format(context['name']))
    doc = tag('doc')(deferred, 'foo')
    assert repr(doc) == "tag('doc')(defer(deferred), 'foo')"
    with pytest.raises(ValueError):
        str(doc)
    bound = bind(doc, {'name': 'Fred'})
    assert str(bound) == '<doc><p>Hello Fred!</p>foo</doc>'


def test_defer_attribute():
    from kemmering import bind, defer, tag

    @defer
    def deferred(context):
        return 'Hello {}!'.format(context['name'])
    doc = tag('doc', foo=deferred)('woot')
    assert repr(doc) == "tag('doc', foo=defer(deferred))('woot')"
    bound = bind(doc, {'name': 'Fred'})
    assert str(bound) == '<doc foo="Hello Fred!">woot</doc>'


def test_defer_remove_attribute():
    from kemmering import bind, defer, tag

    @defer
    def deferred(context):
        return None
    doc = tag('doc', foo=deferred)('woot')
    assert repr(doc) == "tag('doc', foo=defer(deferred))('woot')"
    bound = bind(doc, {'name': 'Fred'})
    assert str(bound) == '<doc>woot</doc>'


def test_defer_with_notag():
    from kemmering import bind, defer, notag, tag

    @defer
    def deferred(context):
        return notag(
            tag('p')('Hello {}!'.format(context['name'])),
            tag('p')('Nice to meet you!')
        )
    doc = tag('doc')(deferred, 'foo')
    assert repr(doc) == "tag('doc')(defer(deferred), 'foo')"
    with pytest.raises(ValueError):
        str(doc)
    bound = bind(doc, {'name': 'Fred'})
    assert str(bound) == ('<doc><p>Hello Fred!</p>'
                          '<p>Nice to meet you!</p>foo</doc>')
    assert repr(bound) == ("tag('doc')(notag(tag('p')('Hello Fred!'), "
                           "tag('p')('Nice to meet you!')), 'foo')")


def test_from_context():
    from kemmering import bind, from_context, tag

    doc = tag('doc')(
        tag('p')('Hello ', from_context('name'), '!'), 'foo')
    assert repr(doc) == ("tag('doc')(tag('p')"
                         "('Hello ', from_context('name'), '!'), 'foo')")
    with pytest.raises(ValueError):
        str(doc)
    bound = bind(doc, {'name': 'Fred'})
    assert str(bound) == '<doc><p>Hello Fred!</p>foo</doc>'


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
    assert repr(doc) == ("tag('doc')(tag('p')"
                         "('Hello ', from_context('name'), '!'), 'foo')")
    with pytest.raises(ValueError):
        str(doc)
    bound = bind(doc, {})
    assert str(bound) == '<doc><p>Hello World!</p>foo</doc>'


def test_in_context():
    from kemmering import bind, in_context, tag

    doc = tag('doc')(
        tag('p')('Hello ', in_context(['user', 'name']), '!'), 'foo')
    assert repr(doc) == ("tag('doc')(tag('p')"
                         "('Hello ', in_context(['user', 'name']), '!'),"
                         " 'foo')")
    with pytest.raises(ValueError):
        str(doc)
    bound = bind(doc, {'user': {'name': 'Fred'}})
    assert str(bound) == '<doc><p>Hello Fred!</p>foo</doc>'


def test_in_context_key_error():
    from kemmering import bind, in_context, tag

    doc = tag('doc')(
        tag('p')('Hello ', in_context(['user', 'name']), '!'), 'foo')
    assert repr(doc) == ("tag('doc')(tag('p')"
                         "('Hello ', in_context(['user', 'name']), '!'),"
                         " 'foo')")
    with pytest.raises(ValueError):
        str(doc)
    with pytest.raises(KeyError):
        bind(doc, {'user': {}})


def test_in_context_use_default():
    from kemmering import bind, in_context, tag

    doc = tag('doc')(
        tag('p')('Hello ', in_context(['user', 'name'], 'World'), '!'), 'foo')
    assert repr(doc) == ("tag('doc')(tag('p')"
                         "('Hello ', in_context(['user', 'name']), '!'),"
                         " 'foo')")
    with pytest.raises(ValueError):
        str(doc)
    bound = bind(doc, {})
    assert str(bound) == '<doc><p>Hello World!</p>foo</doc>'


def test_format_context():
    from kemmering import bind, format_context, tag

    doc = tag('doc')(tag('p')(format_context('Hello {name}!')), 'foo')
    assert repr(doc) == ("tag('doc')(tag('p')"
                         "(format_context('Hello {name}!')), 'foo')")
    with pytest.raises(ValueError):
        str(doc)
    bound = bind(doc, {'name': 'Fred'})
    assert str(bound) == '<doc><p>Hello Fred!</p>foo</doc>'


def test_cond():
    from kemmering import bind, cond, tag

    def is_admin(context):
        return context['user'] == 'admin'
    doc = tag('doc')(cond(is_admin,
                          tag('p')('At your service!'),
                          tag('p')('Go away!')))
    assert repr(doc) == (
        "tag('doc')(cond(is_admin, "
        "tag('p')('At your service!'), "
        "tag('p')('Go away!')))")
    with pytest.raises(ValueError):
        str(doc)
    bound = bind(doc, {'user': 'admin'})
    assert str(bound) == '<doc><p>At your service!</p></doc>'
    bound = bind(doc, {'user': 'grunt'})
    assert str(bound) == '<doc><p>Go away!</p></doc>'


def test_cond_no_negative():
    from kemmering import bind, cond, tag

    def is_admin(context):
        return context['user'] == 'admin'
    doc = tag('doc')(tag('p')('Hi there.', cond(
        is_admin, ' How do you do?')))
    assert repr(doc) == (
        "tag('doc')(tag('p')('Hi there.', cond("
        "is_admin, ' How do you do?')))")
    with pytest.raises(ValueError):
        str(doc)
    bound = bind(doc, {'user': 'admin'})
    assert str(bound) == '<doc><p>Hi there. How do you do?</p></doc>'
    bound = bind(doc, {'user': 'grunt'})
    assert str(bound) == '<doc><p>Hi there.</p></doc>'
