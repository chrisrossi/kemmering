
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
    assert str(tag('a/', foo='bar', bar='baz')) == '<a foo="bar" bar="baz"/>'

def test_tag_with_attributes_repr():
    from kemmering import tag
    assert (repr(tag('a/', foo='bar', bar='baz')) ==
            "tag('a/', foo='bar', bar='baz')")

def test_style():
    from kemmering import style
    assert str(style(
        ('a', {'b': 'c'})
    )) == (
        "\n"
        "<style>\n"
        "  a {\n"
        "    b: c;\n"
        "  }\n"
        "</style>\n"
    )
