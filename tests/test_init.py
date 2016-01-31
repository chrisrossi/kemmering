
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
