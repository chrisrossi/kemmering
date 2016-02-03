
def test_style():
    from kemmering.html import style
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


def test_doc():
    from kemmering.html import doc, html, head, title
    assert str(doc(html()(head()(title()('foo'))))) == (
        "<!DOCTYPE html>\n\n"
        "<html><head><title>foo</title></head></html>"
    )


def test_a():
    from kemmering.html import a
    assert str(a(href='foo/bar')('Howdy!')) == '<a href="foo/bar">Howdy!</a>'


def test_abbr():
    from kemmering.html import abbr
    assert str(abbr(title='foo')('bar')) == '<abbr title="foo">bar</abbr>'


def test_addr():
    from kemmering.html import address
    assert str(address()('113 Huse St.')) == '<address>113 Huse St.</address>'


def test_area():
    from kemmering.html import area
    assert str(area(shape='circle')) == '<area shape="circle"/>'


def test_article():
    from kemmering.html import article
    assert str(article()('foo')) == '<article>foo</article>'


def test_aside():
    from kemmering.html import aside
    assert str(aside()('foo')) == '<aside>foo</aside>'


def test_audio():
    from kemmering.html import audio
    assert str(audio()('foo')) == '<audio>foo</audio>'


def test_b():
    from kemmering.html import b
    assert str(b()('foo')) == '<b>foo</b>'


def test_base():
    from kemmering.html import base
    assert str(base()) == '<base/>'


def test_bdi():
    from kemmering.html import bdi
    assert str(bdi()('foo')) == '<bdi>foo</bdi>'


def test_bdo():
    from kemmering.html import bdo
    assert str(bdo()('foo')) == '<bdo>foo</bdo>'


def test_blockquote():
    from kemmering.html import blockquote
    assert str(blockquote()('foo')) == '<blockquote>foo</blockquote>'


def test_body():
    from kemmering.html import body
    assert str(body()('foo')) == '<body>foo</body>'


def test_br():
    from kemmering.html import br
    assert str(br()) == '<br/>'


def test_button():
    from kemmering.html import button
    assert str(button()('foo')) == '<button>foo</button>'


def test_canvas():
    from kemmering.html import canvas
    assert str(canvas()('foo')) == '<canvas>foo</canvas>'


def test_caption():
    from kemmering.html import caption
    assert str(caption()('foo')) == '<caption>foo</caption>'


def test_cite():
    from kemmering.html import cite
    assert str(cite()('foo')) == '<cite>foo</cite>'


def test_code():
    from kemmering.html import code
    assert str(code()('foo')) == '<code>foo</code>'


def test_col():
    from kemmering.html import col
    assert str(col()) == '<col/>'


def test_colgroup():
    from kemmering.html import colgroup
    assert str(colgroup()('foo')) == '<colgroup>foo</colgroup>'


def test_datalist():
    from kemmering.html import datalist
    assert str(datalist()('foo')) == '<datalist>foo</datalist>'


def test_dd():
    from kemmering.html import dd
    assert str(dd()('foo')) == '<dd>foo</dd>'


def test_del():
    from kemmering.html import del_
    assert str(del_()('foo')) == '<del>foo</del>'


def test_details():
    from kemmering.html import details
    assert str(details()('foo')) == '<details>foo</details>'


def test_dfn():
    from kemmering.html import dfn
    assert str(dfn()('foo')) == '<dfn>foo</dfn>'


def test_div():
    from kemmering.html import div
    assert str(div()('foo')) == '<div>foo</div>'


def test_dl():
    from kemmering.html import dl
    assert str(dl()('foo')) == '<dl>foo</dl>'


def test_dt():
    from kemmering.html import dt
    assert str(dt()('foo')) == '<dt>foo</dt>'


def test_em():
    from kemmering.html import em
    assert str(em()('foo')) == '<em>foo</em>'


def test_embed():
    from kemmering.html import embed
    assert str(embed()) == '<embed/>'


def test_fieldset():
    from kemmering.html import fieldset
    assert str(fieldset()('foo')) == '<fieldset>foo</fieldset>'


def test_figcaption():
    from kemmering.html import figcaption
    assert str(figcaption()('foo')) == '<figcaption>foo</figcaption>'


def test_figure():
    from kemmering.html import figure
    assert str(figure()('foo')) == '<figure>foo</figure>'


def test_footer():
    from kemmering.html import footer
    assert str(footer()('foo')) == '<footer>foo</footer>'


def test_form():
    from kemmering.html import form
    assert str(form()('foo')) == '<form>foo</form>'


def test_h1():
    from kemmering.html import h1
    assert str(h1()('foo')) == '<h1>foo</h1>'


def test_h2():
    from kemmering.html import h2
    assert str(h2()('foo')) == '<h2>foo</h2>'


def test_h3():
    from kemmering.html import h3
    assert str(h3()('foo')) == '<h3>foo</h3>'


def test_h4():
    from kemmering.html import h4
    assert str(h4()('foo')) == '<h4>foo</h4>'


def test_h5():
    from kemmering.html import h5
    assert str(h5()('foo')) == '<h5>foo</h5>'


def test_h6():
    from kemmering.html import h6
    assert str(h6()('foo')) == '<h6>foo</h6>'


def test_head():
    from kemmering.html import head
    assert str(head()('foo')) == '<head>foo</head>'


def test_header():
    from kemmering.html import header
    assert str(header()('foo')) == '<header>foo</header>'


def test_hgroup():
    from kemmering.html import hgroup
    assert str(hgroup()('foo')) == '<hgroup>foo</hgroup>'


def test_hr():
    from kemmering.html import hr
    assert str(hr()) == '<hr/>'


def test_html():
    from kemmering.html import html
    assert str(html()('foo')) == '<html>foo</html>'


def test_i():
    from kemmering.html import i
    assert str(i()('foo')) == '<i>foo</i>'


def test_iframe():
    from kemmering.html import iframe
    assert str(iframe()('foo')) == '<iframe>foo</iframe>'


def test_img():
    from kemmering.html import img
    assert str(img()) == '<img/>'


def test_input():
    from kemmering.html import input
    assert str(input()) == '<input/>'


def test_kbd():
    from kemmering.html import kbd
    assert str(kbd()('foo')) == '<kbd>foo</kbd>'


def test_keygen():
    from kemmering.html import keygen
    assert str(keygen()('foo')) == '<keygen>foo</keygen>'


def test_label():
    from kemmering.html import label
    assert str(label()('foo')) == '<label>foo</label>'


def test_legend():
    from kemmering.html import legend
    assert str(legend()('foo')) == '<legend>foo</legend>'


def test_li():
    from kemmering.html import li
    assert str(li()('foo')) == '<li>foo</li>'


def test_link():
    from kemmering.html import link
    assert str(link()) == '<link/>'


def test_map():
    from kemmering.html import map
    assert str(map()('foo')) == '<map>foo</map>'


def test_mark():
    from kemmering.html import mark
    assert str(mark()('foo')) == '<mark>foo</mark>'


def test_menu():
    from kemmering.html import menu
    assert str(menu()('foo')) == '<menu>foo</menu>'


def test_meta():
    from kemmering.html import meta
    assert str(meta()) == '<meta/>'


def test_meter():
    from kemmering.html import meter
    assert str(meter()('foo')) == '<meter>foo</meter>'


def test_nav():
    from kemmering.html import nav
    assert str(nav()('foo')) == '<nav>foo</nav>'


def test_noscript():
    from kemmering.html import noscript
    assert str(noscript()('foo')) == '<noscript>foo</noscript>'


def test_object():
    from kemmering.html import object
    assert str(object()('foo')) == '<object>foo</object>'


def test_ol():
    from kemmering.html import ol
    assert str(ol()('foo')) == '<ol>foo</ol>'


def test_optgroup():
    from kemmering.html import optgroup
    assert str(optgroup()('foo')) == '<optgroup>foo</optgroup>'


def test_option():
    from kemmering.html import option
    assert str(option()('foo')) == '<option>foo</option>'


def test_output():
    from kemmering.html import output
    assert str(output()('foo')) == '<output>foo</output>'


def test_p():
    from kemmering.html import p
    assert str(p()('foo')) == '<p>foo</p>'


def test_param():
    from kemmering.html import param
    assert str(param()) == '<param/>'


def test_pre():
    from kemmering.html import pre
    assert str(pre()('foo')) == '<pre>foo</pre>'


def test_progress():
    from kemmering.html import progress
    assert str(progress()('foo')) == '<progress>foo</progress>'


def test_q():
    from kemmering.html import q
    assert str(q()('foo')) == '<q>foo</q>'


def test_rp():
    from kemmering.html import rp
    assert str(rp()('foo')) == '<rp>foo</rp>'


def test_rt():
    from kemmering.html import rt
    assert str(rt()('foo')) == '<rt>foo</rt>'


def test_ruby():
    from kemmering.html import ruby
    assert str(ruby()('foo')) == '<ruby>foo</ruby>'


def test_s():
    from kemmering.html import s
    assert str(s()('foo')) == '<s>foo</s>'


def test_samp():
    from kemmering.html import samp
    assert str(samp()('foo')) == '<samp>foo</samp>'


def test_script():
    from kemmering.html import script
    assert str(script()('foo')) == '<script>foo</script>'


def test_section():
    from kemmering.html import section
    assert str(section()('foo')) == '<section>foo</section>'


def test_select():
    from kemmering.html import select
    assert str(select()('foo')) == '<select>foo</select>'


def test_small():
    from kemmering.html import small
    assert str(small()('foo')) == '<small>foo</small>'


def test_source():
    from kemmering.html import source
    assert str(source()) == '<source/>'


def test_span():
    from kemmering.html import span
    assert str(span()('foo')) == '<span>foo</span>'


def test_strong():
    from kemmering.html import strong
    assert str(strong()('foo')) == '<strong>foo</strong>'


def test_sub():
    from kemmering.html import sub
    assert str(sub()('foo')) == '<sub>foo</sub>'


def test_summary():
    from kemmering.html import summary
    assert str(summary()('foo')) == '<summary>foo</summary>'


def test_sup():
    from kemmering.html import sup
    assert str(sup()('foo')) == '<sup>foo</sup>'


def test_table():
    from kemmering.html import table
    assert str(table()('foo')) == '<table>foo</table>'


def test_tbody():
    from kemmering.html import tbody
    assert str(tbody()('foo')) == '<tbody>foo</tbody>'


def test_td():
    from kemmering.html import td
    assert str(td()('foo')) == '<td>foo</td>'


def test_textarea():
    from kemmering.html import textarea
    assert str(textarea()('foo')) == '<textarea>foo</textarea>'


def test_tfoot():
    from kemmering.html import tfoot
    assert str(tfoot()('foo')) == '<tfoot>foo</tfoot>'


def test_th():
    from kemmering.html import th
    assert str(th()('foo')) == '<th>foo</th>'


def test_thead():
    from kemmering.html import thead
    assert str(thead()('foo')) == '<thead>foo</thead>'


def test_time():
    from kemmering.html import time
    assert str(time()('foo')) == '<time>foo</time>'


def test_title():
    from kemmering.html import title
    assert str(title()('foo')) == '<title>foo</title>'


def test_tr():
    from kemmering.html import tr
    assert str(tr()('foo')) == '<tr>foo</tr>'


def test_track():
    from kemmering.html import track
    assert str(track()) == '<track/>'


def test_u():
    from kemmering.html import u
    assert str(u()('foo')) == '<u>foo</u>'


def test_ul():
    from kemmering.html import ul
    assert str(ul()('foo')) == '<ul>foo</ul>'


def test_var():
    from kemmering.html import var
    assert str(var()('foo')) == '<var>foo</var>'


def test_video():
    from kemmering.html import video
    assert str(video()('foo')) == '<video>foo</video>'


def test_wbr():
    from kemmering.html import wbr
    assert str(wbr()('foo')) == '<wbr>foo</wbr>'
