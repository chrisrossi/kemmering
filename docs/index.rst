=========
Kemmering
=========

.. _overview:

Overview
========

`Kemmering` is a lightweight library for producing XML and HTML5 snippets in
Python code with a minimum of fuss and bother.   The snippets can be templated,
or not.  `Kemmering` is not an XML parser, doesn't know anything about SAX,
DOM, XPATH, or namespaces, and generally doesn't try to think too hard about
what an XML document is in the abstract.

`Kemmering` isn't intended as a wholesale replacement for template languages.
If you're editing a whole page of HTML, you may as well edit it as HTML, not
Python code.  `Kemmering` is intended to make it easy to produce little bits of
HTML or other XMLish markup and glue them together in convenient ways.  Imagine
you're writing a form library, for instance, that involves a lot of little 
snippets of HTML that get composed together to make a form.  You could have 
each widget in a separate template file, with dozens of files each containing
a few lines of markup.  Or you could put your widgets in a single Python file,
which may be more convenient.

One thing I recently used this for was producing SVG from a completely 
different drawing format.  This would have been a pain in the neck using a 
template language, but was pretty straightforward using `Kemmer` and a 
functional programming style.

Maybe you'll find this useful.  YMMV, y'all.

.. _installation:

Installation
============

Install using setuptools, e.g. (within a virtualenv)::

  $ $VENV/bin/pip install kemmering

Tags
====

The heart and soul of `Kemmering` is the :class:`tag <kemmering.tag>` class:

.. doctest:: hello-world

   >>> from kemmering import tag
   >>> hello_world = tag('hello', id='salutation')('world')
   >>> str(hello_world)
   '<hello id="salutation">world</hello>'

In a nutshell, the first and only positional argument is the name of the tag, 
any keyword arguments are attributes, and calling the result adds children, 
where children can be more tags or text elements.  Use `str` to realize a
snippet as a string.  

Appending a forward slash (`/`) character to the end of the tag name creates a
self-closing tag.

.. doctest:: hello

   >>> from kemmering import tag
   >>> str(tag('hello/'))
   '<hello/>'

If you are still using Python 2, you'll want to use `unicode` instead of `str`:

.. testsetup:: unicode

   # Run doctests in Python 3
   class unicode(str):
       def __repr__(self):
           return 'u' + super(unicode, self).__repr__()

.. doctest:: unicode

   >>> from kemmering import tag
   >>> hello_world = tag('hello', id='salutation')('world')
   >>> unicode(hello_world)
   u'<hello id="salutation">world</hello>'

A tag may be called more than once to add children to it:

.. doctest:: multiple-calls

   >>> from kemmering import tag
   >>> ul = tag('ul')
   >>> ul(tag('li')('one'))
   tag('ul')(tag('li')('one'))
   >>> ul(tag('li')('two'))
   tag('ul')(tag('li')('one'), tag('li')('two'))
   >>> str(ul)
   '<ul><li>one</li><li>two</li></ul>'

Partial Pattern
---------------

A pattern some might find useful is to use partials to create tag-specific 
callables. For example:

.. doctest:: partials

   >>> from functools import partial
   >>> from kemmering import tag
   >>> div = partial(tag, 'div')
   >>> str(div()('Hello World!'))
   '<div>Hello World!</div>'

HTML Tags
---------

The partial pattern is the basic strategy used by the vast majority of the
:mod:`kemmering.html` package, which contains all valid HTML5 tags.

.. doctest:: html

   >>> from kemmering import html as h
   >>> snippet = h.dl(class_='fruits')(
   ...     h.dt()('Pomegranate'),
   ...     h.dd()('It has ', h.em()('lots'), ' of seeds!'),
   ...     h.dt()('Kiwi'),
   ...     h.dd()('It tastes like strawberry.'),
   ... )
   >>> str(snippet)
   '<dl class="fruits"><dt>Pomegranate</dt><dd>It has <em>lots</em> of seeds!</dd><dt>Kiwi</dt><dd>It tastes like strawberry.</dd></dl>'

Two tags, :class:`doc <kemmering.html.doc>` and 
:class:`style <kemmering.html.style>`, have different behavior from the standard
`tag`.  See their respective API docs for more information.

Make it pretty
++++++++++++++

The :mod:`html <kemmering.html>` package also as a 
:func:`pretty <kemmering.html.pretty>` function that will render a snippet
with line breaks and indentation, which can be useful for debugging.

.. doctest:: pretty

   >>> from kemmering import html as h
   >>> print(h.pretty(
   ...     h.doc(h.html()(
   ...        h.head()(
   ...            h.title()('Hello World!')
   ...        ),
   ...        h.body()(
   ...            h.p(class_='salutation')('Hello World!')
   ...        )
   ...     ))
   ... ))
   <!DOCTYPE html>
   <html>
     <head>
       <title>Hello World!</title>
     </head>
     <body>
       <p class="salutation">Hello World!</p>
     </body>
   </html>
   <BLANKLINE>

Reserved Word Attributes
------------------------

You might have noticed in the example above that the `class` attribute for the 
`<p>` element is specified using `class_`.  Because `class` is a reserved word
in Python, you wouldn't be able to say `h.p(class='salutation')`.  For this 
reason, any attribute name can end with an underscore character, and the 
trailing underscore will be elided from the ultimate attribute name.

.. doctest:: reserved-words

   >>> from kemmering import html as h
   >>> snippet = h.label(for_='full_name')('Your full legal name')
   >>> str(snippet)
   '<label for="full_name">Your full legal name</label>'

Templates
=========

`defer` and `bind`
------------------

Using :class:`defer <kemmering.defer>` and :class:`bind <kemmering.bind>` you
can create and render templates.  `defer` allows you to create an element that
is realized at a later time with information not available when the snippet is
being created.  `bind` is used to realize the snippet later.  `defer` accepts a
single argument which is a function that is called at bind time.  The deferred
function accepts a single argument, `context`, which should contain any
information needed to realize the snippet at bind time.  In theory, the
`context` can be any object, but the standard set of template helpers provided
mostly assume the context is a dictionary or an object which provides a
dictionary interface.  The deferred function returns either a tag instance or a
string which replaces the deferred function in the bound snippet.

The signature of `defer` allows it to be used as a decorator, if you're into
that kind of thing:

.. doctest:: defer

   >>> from kemmering import bind, defer
   >>> from kemmering import html as h
   >>> @defer
   ... def things(context):
   ...     ul = h.ul()
   ...     for thing in context['things']:
   ...         ul(h.li()(thing))
   ...     return ul
   >>> snippet = h.div()(things)
   >>> bound = bind(snippet, {'things': ['bat', 'glove']})
   >>> str(bound)
   '<div><ul><li>bat</li><li>glove</li></ul></div>'

`notag`
-------

:class:`notag <kemmering.notag>` is useful if you'd like for a deferred to
provide more than one child at the level it is placed in the snippet:

.. doctest:: notag

   >>> from kemmering import bind, defer, notag
   >>> from kemmering import html as h
   >>> @defer
   ... def address(context):
   ...     return notag(
   ...         context['name'], h.br(),
   ...         context['address'], h.br(),
   ...         context['city'], ', ', 
   ...         context['state'], ' ',
   ...         context['zip'],
   ...     )
   >>> snippet = h.p()(address)
   >>> bound = bind(snippet, {'name': 'Joe Blow', 'address': '123 Main St.',
   ...                        'city': 'Minsk', 'state': 'MS', 'zip': '12345'})
   >>> str(bound)
   '<p>Joe Blow<br/>123 Main St.<br/>Minsk, MS 12345</p>'

Templating attributes
---------------------

Attributes can be templated as well as tag children. For obvious reasons, a 
deferred function being used for an attribute can't return a tag.  A deferred
function used for an attribute may return a string, or it may return `None`. If
an attribute is set to `None` that attribute is omitted from the final bound
snippet.

.. doctest:: defer-attributes

   >>> from kemmering import bind, defer
   >>> from kemmering import html as h
   >>> def selected(context):
   ...     if context['option'] == context['selected']:
   ...         return ''
   >>> snippet = h.option(selected=defer(selected))(
   ...     defer(lambda context: context['option']))
   >>> bound = bind(snippet, {'option': 'fish', 'selected': 'fish'})
   >>> str(bound)
   '<option selected="">fish</option>'
   >>> bound = bind(snippet, {'option': 'medicine', 'selected': 'fish'})
   >>> str(bound)
   '<option>medicine</option>'


Template Helpers
================

The examples above which use :class:`defer <kemmering.defer>` are a bit
contrived. In practice, it will probably be rare to use the general purpose
`defer`, although it is general enough it should cover any use case.  The most
common use cases for `defer` are covered by the helpers described below, which
should cover the vast majority of cases for `defer`.  

`from_context`
--------------

:class:`from_context <kemmering.from_context>` substitutes a value from the
context:

.. doctest:: from_context

   >>> from kemmering import bind, from_context
   >>> from kemmering import html as h
   >>> snippet = h.p()("Hello ", from_context('name'), '!')
   >>> bound = bind(snippet, {'name': 'Edgar'})
   >>> str(bound)
   '<p>Hello Edgar!</p>'

`from_context` accepts an optional default argument:

.. doctest:: from_context_default

   >>> from kemmering import bind, from_context
   >>> from kemmering import html as h
   >>> snippet = h.p()("Hello ", from_context('name', 'World'), '!')
   >>> bound = bind(snippet, {'name': 'Edgar'})
   >>> str(bound)
   '<p>Hello Edgar!</p>'
   >>> bound = bind(snippet, {})
   >>> str(bound)
   '<p>Hello World!</p>'

`in_context`
------------

:class:`in_context <kemmering.in_context>` works very simlarly to
`from_context` but accepts a sequence of keys as an argument and can traverse a
seris of nested dictionaries to retrieve a value from the context:

.. doctest:: in_context

   >>> from kemmering import bind, in_context
   >>> from kemmering import html as h
   >>> snippet = h.p()("Hello ", in_context(['user', 'name']), '!')
   >>> bound = bind(snippet, {'user': {'name': 'Edgar'}})
   >>> str(bound)
   '<p>Hello Edgar!</p>'

`in_context` also accepts an optional default argument:

.. doctest:: in_context_default

   >>> from kemmering import bind, in_context
   >>> from kemmering import html as h
   >>> snippet = h.p()("Hello ", in_context(['user', 'name'], 'World'), '!')
   >>> bound = bind(snippet, {'user': {'name': 'Edgar'}})
   >>> str(bound)
   '<p>Hello Edgar!</p>'
   >>> bound = bind(snippet, {})
   >>> str(bound)
   '<p>Hello World!</p>'

`format_context`
----------------

:class:`format_context <kemmering.format_context>` is passed a format string,
`s`, and returns the equivalent of `s.format(**context)` when it is bound:

.. doctest:: format_context

   >>> from kemmering import bind, format_context
   >>> from kemmering import html as h
   >>> snippet = h.p()(format_context('Hello {name}!'))
   >>> bound = bind(snippet, {'name': 'Edgar'})
   >>> str(bound)
   '<p>Hello Edgar!</p>'

`cond`
------

:class:`cond <kemmering.cond>` includes a sub-snippet or not conditionally.
The first argument is a function, `condition`, which accepts a single argument,
`context`, and returns a boolean.  The second argument is the snippet to
include if `condition` returns `True`.

.. doctest:: cond

   >>> from kemmering import bind, cond, format_context
   >>> from kemmering import html as h
   >>> def logged_in(context):
   ...     return 'user' in context
   >>> snippet = h.div()(
   ...     'Welcome to Acme!',
   ...     cond(logged_in, format_context(' Hello {user[name]}!')))
   >>> bound = bind(snippet, {'user': {'name': 'Fred'}})
   >>> str(bound)
   '<div>Welcome to Acme! Hello Fred!</div>'
   >>> bound = bind(snippet, {})
   >>> str(bound)
   '<div>Welcome to Acme!</div>'

`cond` also accepts an optional third argument, which is a snippet to include 
if `condition` returns `False`.

.. doctest:: cond-else

   >>> from kemmering import bind, cond, format_context
   >>> from kemmering import html as h
   >>> def logged_in(context):
   ...     return 'user' in context
   >>> snippet = h.div()(
   ...     'Welcome to Acme!',
   ...     cond(logged_in, format_context(' Hello {user[name]}!'),
   ...          ' You are not logged in!'))
   >>> bound = bind(snippet, {'user': {'name': 'Fred'}})
   >>> str(bound)
   '<div>Welcome to Acme! Hello Fred!</div>'
   >>> bound = bind(snippet, {})
   >>> str(bound)
   '<div>Welcome to Acme! You are not logged in!</div>'

`loop`
------

:class:`loop <kemmering.loop>` allows for repeating of a sub-snippet inside of
another snippet by looping over items in a sequence.  The first argument to
`loop` is the name of a key to maintain in the `context` with the value of the
current item being iterated over.  This argument can optionally be a `list` or
`tuple` of key names, which will cause sequence values to be unpacked.  The
second argument is either a function, which accepts the `context` as an
argument and returns a sequence, or the name of a key inside of `context` whose
value is the sequence to iterate over.  The third argument is the snippet to be
repeated for each item in the sequence.

.. doctest:: loop

   >>> from kemmering import bind, from_context, loop
   >>> from kemmering import html as h
   >>> snippet = h.ul()(
   ...     loop('fruit', 'fruits', h.li()(from_context('fruit'))))
   >>> bound = bind(snippet, {'fruits': ['apple', 'pear', 'banana']})
   >>> str(bound)
   '<ul><li>apple</li><li>pear</li><li>banana</li></ul>'

More Information
================

.. toctree::
   :maxdepth: 1

   api.rst

Reporting Bugs / Development Versions
=====================================

Visit http://github.com/chrisrossi/kemmering to download development or tagged
versions.

Visit http://github.com/chrisrossi/kemmering/issues to report bugs.
