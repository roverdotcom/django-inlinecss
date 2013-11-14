#!/usr/bin/env python
import unittest
import warnings
import StringIO
import logging
import cssutils

from django_inlinecss import pynliner
from django_inlinecss.pynliner import Pynliner


class Basic(unittest.TestCase):
    def setUp(self):
        self.html = "<style>h1 { color:#ffcc00; }</style><h1>Hello World!</h1>"
        self.p = Pynliner().from_string(self.html)

    def test_01_fromString(self):
        """Test 'fromString' constructor"""
        self.assertEqual(self.p.source_string, self.html)

    def test_02_get_soup(self):
        """Test '_get_soup' method"""
        self.p._get_soup()
        self.assertEqual(unicode(self.p.soup), self.html)

    def test_03_get_styles(self):
        """Test '_get_styles' method"""
        self.p._get_soup()
        self.p._get_styles()
        self.assertEqual(self.p.style_string, u'h1 { color:#ffcc00; }\n')
        self.assertEqual(unicode(self.p.soup), u'<h1>Hello World!</h1>')

    def test_04_apply_styles(self):
        """Test '_apply_styles' method"""
        self.p._get_soup()
        self.p._get_styles()
        self.p._apply_styles()
        self.assertEqual(
            unicode(self.p.soup),
            u'<h1 style="color: #fc0">Hello World!</h1>')

    def test_05_run(self):
        """Test 'run' method"""
        output = self.p.run()
        self.assertEqual(output, u'<h1 style="color: #fc0">Hello World!</h1>')

    def test_06_with_cssString(self):
        """Test 'with_cssString' method"""
        cssString = 'h1 {font-size: 2em;}'
        self.p = Pynliner().from_string(self.html).with_cssString(cssString)
        self.assertEqual(self.p.style_string, cssString + '\n')

        output = self.p.run()
        self.assertEqual(
            output,
            u'<h1 style="font-size: 2em; color: #fc0">Hello World!</h1>')

    def test_07_fromString(self):
        """Test 'fromString' complete"""
        output = pynliner.fromString(self.html)
        desired = u'<h1 style="color: #fc0">Hello World!</h1>'
        self.assertEqual(output, desired)

    def test_08_fromURL(self):
        """Test 'fromURL' constructor"""
        if hasattr(unittest, 'SkipTest'):
            raise unittest.SkipTest()
        else:
            return
        url = 'http://media.tannern.com/pynliner/test.html'
        p = Pynliner()
        p.from_url(url)
        self.assertEqual(p.root_url, 'http://media.tannern.com')
        self.assertEqual(p.relative_url, 'http://media.tannern.com/pynliner/')

        p._get_soup()

        p._get_external_styles()
        self.assertEqual(p.style_string, "p {color: #999}")

        p._get_internal_styles()
        self.assertEqual(
            p.style_string,
            "p {color: #999}\nh1 {color: #ffcc00;}\n")

        p._get_styles()

        output = p.run()
        desired = u"""<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>test</title>


</head>
<body>
<h1 style="color: #fc0">Hello World!</h1>
<p style="color: #999">Possim tincidunt putamus iriure eu nulla. Facer qui volutpat ut aliquam sequitur. Mutationem legere feugiat autem clari notare. Nulla typi augue suscipit lectores in.</p>
<p style="color: #999">Facilisis claritatem eum decima dignissim legentis. Nulla per legentis odio molestie quarta. Et velit typi claritas ipsum ullamcorper.</p>
</body>
</html>"""
        self.assertEqual(output, desired)

    def test_09_overloadedStyles(self):
        html = ''.join((
            '<style>h1 { color: red; } #test { color: blue; }</style>',
            '<h1 id="test">Hello world!</h1>'))
        expected = '<h1 id="test" style="color: blue">Hello world!</h1>'
        output = Pynliner().from_string(html).run()
        self.assertEqual(expected, output)


class CommaSelector(unittest.TestCase):

    def setUp(self):
        self.html = ''.join((
            '<style>.b1,.b2 { font-weight:bold; } .c {color: red}</style>'
            '<span class="b1">Bold</span><span class="b2 c">Bold Red</span>'))
        self.p = Pynliner().from_string(self.html)

    def test_01_fromString(self):
        """Test 'fromString' constructor"""
        self.assertEqual(self.p.source_string, self.html)

    def test_02_get_soup(self):
        """Test '_get_soup' method"""
        self.p._get_soup()
        self.assertEqual(unicode(self.p.soup), self.html)

    def test_03_get_styles(self):
        """Test '_get_styles' method"""
        self.p._get_soup()
        self.p._get_styles()
        self.assertEqual(
            self.p.style_string,
            u'.b1,.b2 { font-weight:bold; } .c {color: red}\n')
        self.assertEqual(
            unicode(self.p.soup),
            u'<span class="b1">Bold</span><span class="b2 c">Bold Red</span>')

    def test_04_apply_styles(self):
        """Test '_apply_styles' method"""
        self.p._get_soup()
        self.p._get_styles()
        self.p._apply_styles()
        self.assertEqual(
            unicode(self.p.soup),
            unicode(''.join((
                '<span class="b1" style="font-weight: bold">Bold</span>',
                '<span class="b2 c" style="color: red; font-weight: bold">',
                'Bold Red</span>'))
            ))

    def test_05_run(self):
        """Test 'run' method"""
        output = self.p.run()
        self.assertEqual(output, u'<span class="b1" style="font-weight: bold">Bold</span><span class="b2 c" style="color: red; font-weight: bold">Bold Red</span>')

    def test_06_with_cssString(self):
        """Test 'with_cssString' method"""
        cssString = '.b1,.b2 {font-size: 2em;}'
        self.p = Pynliner().from_string(self.html).with_cssString(cssString)
        self.assertEqual(self.p.style_string, cssString + '\n')

        output = self.p.run()
        self.assertEqual(output, u'<span class="b1" style="font-size: 2em; font-weight: bold">Bold</span><span class="b2 c" style="color: red; font-size: 2em; font-weight: bold">Bold Red</span>')

    def test_07_fromString(self):
        """Test 'fromString' complete"""
        output = pynliner.fromString(self.html)
        desired = u'<span class="b1" style="font-weight: bold">Bold</span><span class="b2 c" style="color: red; font-weight: bold">Bold Red</span>'
        self.assertEqual(output, desired)

    def test_08_comma_whitespace(self):
        """Test excess whitespace in CSS"""
        html = '<style>h1,  h2   ,h3,\nh4{   color:    #000}  </style><h1>1</h1><h2>2</h2><h3>3</h3><h4>4</h4>'
        desired_output = '<h1 style="color: #000">1</h1><h2 style="color: #000">2</h2><h3 style="color: #000">3</h3><h4 style="color: #000">4</h4>'
        output = Pynliner().from_string(html).run()
        self.assertEqual(output, desired_output)

class Extended(unittest.TestCase):

    def test_overwrite(self):
        """Test overwrite inline styles"""
        html = '<style>h1 {color: #000;}</style><h1 style="color: #fff">Foo</h1>'
        desired_output = '<h1 style="color: #000; color: #fff">Foo</h1>'
        output = Pynliner().from_string(html).run()
        self.assertEqual(output, desired_output)

    def test_overwrite_comma(self):
        """Test overwrite inline styles"""
        html = '<style>h1,h2,h3 {color: #000;}</style><h1 style="color: #fff">Foo</h1><h3 style="color: #fff">Foo</h3>'
        desired_output = '<h1 style="color: #000; color: #fff">Foo</h1><h3 style="color: #000; color: #fff">Foo</h3>'
        output = Pynliner().from_string(html).run()
        self.assertEqual(output, desired_output)


class LogOptions(unittest.TestCase):
    def setUp(self):
        self.html = "<style>h1 { color:#ffcc00; }</style><h1>Hello World!</h1>"

    def test_no_log(self):
        self.p = Pynliner()
        self.assertEqual(self.p.log, None)
        self.assertEqual(cssutils.log.enabled, False)

    def test_custom_log(self):
        self.log = logging.getLogger('testlog')
        self.log.setLevel(logging.DEBUG)

        self.logstream = StringIO.StringIO()
        handler = logging.StreamHandler(self.logstream)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.log.addHandler(handler)

        self.p = Pynliner(self.log).from_string(self.html)

        self.p.run()
        log_contents = self.logstream.getvalue()
        self.assertTrue("DEBUG" in log_contents)


class BeautifulSoupBugs(unittest.TestCase):

    def test_double_doctype(self):
        self.html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">"""
        output = pynliner.fromString(self.html)
        self.assertFalse("<!<!" in output)

    def test_double_comment(self):
        self.html = """<!-- comment -->"""
        output = pynliner.fromString(self.html)
        self.assertFalse("<!--<!--" in output)


class ComplexSelectors(unittest.TestCase):

    def test_multiple_class_selector(self):
        html = """<h1 class="a b">Hello World!</h1>"""
        css = """h1.a.b { color: red; }"""
        expected = u"""<h1 class="a b" style="color: red">Hello World!</h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_combination_selector(self):
        html = """<h1 id="a" class="b">Hello World!</h1>"""
        css = """h1#a.b { color: red; }"""
        expected = u"""<h1 id="a" class="b" style="color: red">Hello World!</h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_descendant_selector(self):
        html = """<h1><span>Hello World!</span></h1>"""
        css = """h1 span { color: red; }"""
        expected = u"""<h1><span style="color: red">Hello World!</span></h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_child_selector(self):
        html = """<h1><span>Hello World!</span></h1>"""
        css = """h1 > span { color: red; }"""
        expected = u"""<h1><span style="color: red">Hello World!</span></h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_nested_child_selector(self):
        html = """<div><h1><span>Hello World!</span></h1></div>"""
        css = """div > h1 > span { color: red; }"""
        expected = u"""<div><h1><span style="color: red">Hello World!</span></h1></div>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_child_selector_complex_dom(self):
        html = """<h1><span>Hello World!</span><p>foo</p><div class="barclass"><span>baz</span>bar</div></h1>"""
        css = """h1 > span { color: red; }"""
        expected = u"""<h1><span style="color: red">Hello World!</span><p>foo</p><div class="barclass"><span>baz</span>bar</div></h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_child_all_selector_complex_dom(self):
        html = """<h1><span>Hello World!</span><p>foo</p><div class="barclass"><span>baz</span>bar</div></h1>"""
        css = """h1 > * { color: red; }"""
        expected = u"""<h1><span style="color: red">Hello World!</span><p style="color: red">foo</p><div class="barclass" style="color: red"><span>baz</span>bar</div></h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_adjacent_selector(self):
        html = """<h1>Hello World!</h1><h2>How are you?</h2>"""
        css = """h1 + h2 { color: red; }"""
        expected = u"""<h1>Hello World!</h1><h2 style="color: red">How are you?</h2>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_unknown_pseudo_selector(self):
        html = """<h1><span>Hello World!</span><p>foo</p><div class="barclass"><span>baz</span>bar</div></h1>"""
        css = """h1 > span:css4-selector { color: red; }"""
        expected = u"""<h1><span>Hello World!</span><p>foo</p><div class="barclass"><span>baz</span>bar</div></h1>"""
        pynliner_instance = Pynliner().from_string(html).with_cssString(css)
        with warnings.catch_warnings(record=True) as warning:
            output = pynliner_instance.run()
            self.assertEqual(
                warning[0].message.message,
                'Pseudoclass :css4-selector invalid or unsupported')
        self.assertEqual(
            output,
            expected)

    def test_child_follow_by_adjacent_selector_complex_dom(self):
        html = """<h1><span>Hello World!</span><p>foo</p><div class="barclass"><span>baz</span>bar</div></h1>"""
        css = """h1 > span + p { color: red; }"""
        expected = u"""<h1><span>Hello World!</span><p style="color: red">foo</p><div class="barclass"><span>baz</span>bar</div></h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_child_follow_by_first_child_selector_with_white_spaces(self):
        html = """<h1> <span>Hello World!</span><p>foo</p><div class="barclass"><span>baz</span>bar</div></h1>"""
        css = """h1 > :first-child { color: red; }"""
        expected = u"""<h1> <span style="color: red">Hello World!</span><p>foo</p><div class="barclass"><span>baz</span>bar</div></h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_child_follow_by_first_child_selector_with_comments(self):
        html = """<h1> <!-- enough said --><span>Hello World!</span><p>foo</p><div class="barclass"><span>baz</span>bar</div></h1>"""
        css = """h1 > :first-child { color: red; }"""
        expected = u"""<h1> <!-- enough said --><span style="color: red">Hello World!</span><p>foo</p><div class="barclass"><span>baz</span>bar</div></h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_child_follow_by_first_child_selector_complex_dom(self):
        html = """<h1><span>Hello World!</span><p>foo</p><div class="barclass"><span>baz</span>bar</div></h1>"""
        css = """h1 > :first-child { color: red; }"""
        expected = u"""<h1><span style="color: red">Hello World!</span><p>foo</p><div class="barclass"><span>baz</span>bar</div></h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_last_child_selector(self):
        html = """<h1><span>Hello World!</span></h1>"""
        css = """h1 > :last-child { color: red; }"""
        expected = u"""<h1><span style="color: red">Hello World!</span></h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_child_follow_by_last_child_selector_complex_dom(self):
        html = """<h1><span>Hello World!</span><p>foo</p><div class="barclass"><span>baz</span>bar</div></h1>"""
        css = """h1 > :last-child { color: red; }"""
        expected = u"""<h1><span>Hello World!</span><p>foo</p><div class="barclass" style="color: red"><span>baz</span>bar</div></h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_child_with_first_child_override_selector_complex_dom(self):
        html = """<div><span>Hello World!</span><p>foo</p><div class="barclass"><span>baz</span>bar</div></div>"""
        css = """div > * { color: green; } div > :first-child { color: red; }"""
        expected = u"""<div><span style="color: red">Hello World!</span><p style="color: green">foo</p><div class="barclass" style="color: green"><span style="color: red">baz</span>bar</div></div>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_id_el_child_with_first_child_override_selector_complex_dom(self):
        html = """<div id="abc"><span class="cde">Hello World!</span><p>foo</p><div class="barclass"><span>baz</span>bar</div></div>"""
        css = """#abc > * { color: green; } #abc > :first-child { color: red; }"""
        expected = u"""<div id="abc"><span class="cde" style="color: red">Hello World!</span><p style="color: green">foo</p><div class="barclass" style="color: green"><span>baz</span>bar</div></div>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_child_with_first_and_last_child_override_selector(self):
        html = """<p><span>Hello World!</span></p>"""
        css = """p > * { color: green; } p > :first-child:last-child { color: red; }"""
        expected = u"""<p><span style="color: red">Hello World!</span></p>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_nested_child_with_first_child_override_selector_complex_dom(self):
        self.maxDiff = None

        html = """<div><div><span>Hello World!</span><p>foo</p><div class="barclass"><span>baz</span>bar</div></div></div>"""
        css = """div > div > * { color: green; } div > div > :first-child { color: red; }"""
        expected = u"""<div><div><span style="color: red">Hello World!</span><p style="color: green">foo</p><div class="barclass" style="color: green"><span style="color: red">baz</span>bar</div></div></div>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_child_with_first_child_and_class_selector_complex_dom(self):
        html = """<h1><span class="hello">Hello World!</span><p>foo</p><div class="barclass"><span>baz</span>bar</div></h1>"""
        css = """h1 > .hello:first-child { color: green; }"""
        expected = u"""<h1><span class="hello" style="color: green">Hello World!</span><p>foo</p><div class="barclass"><span>baz</span>bar</div></h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_child_with_first_child_and_unmatched_class_selector_complex_dom(self):
        html = """<h1><span>Hello World!</span><p>foo</p><div class="barclass"><span>baz</span>bar</div></h1>"""
        css = """h1 > .hello:first-child { color: green; }"""
        expected = u"""<h1><span>Hello World!</span><p>foo</p><div class="barclass"><span>baz</span>bar</div></h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_first_child_descendant_selector(self):
        html = """<h1><div><span>Hello World!</span></div></h1>"""
        css = """h1 :first-child { color: red; }"""
        expected = u"""<h1><div style="color: red"><span style="color: red">Hello World!</span></div></h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_last_child_descendant_selector(self):
        html = """<h1><div><span>Hello World!</span></div></h1>"""
        css = """h1 :last-child { color: red; }"""
        expected = u"""<h1><div style="color: red"><span style="color: red">Hello World!</span></div></h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_first_child_descendant_selector_complex_dom(self):
        html = """<h1><div><span>Hello World!</span></div><p>foo</p><div class="barclass"><span>baz</span>bar</div></h1>"""
        css = """h1 :first-child { color: red; }"""
        expected = u"""<h1><div style="color: red"><span style="color: red">Hello World!</span></div><p>foo</p><div class="barclass"><span style="color: red">baz</span>bar</div></h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_hover_pseudo_selector(self):
        """
        :hover pseudo-selector isn't valid in the context of inline CSS
        so we can't possible support it. However we can raise a
        RuntimeWarning.

        (In the scenario where the CSS is shared between normal pages &
        CSS inlined pages, it may make sense to have things that can't
        actually be used in the inlining step.)
        """
        html = """<h1><a href="/some-url/">Click here</a></h1>"""
        css = """a:hover { color: red; }"""
        expected = """<h1><a href="/some-url/">Click here</a></h1>"""
        with warnings.catch_warnings(record=True) as warning:
            output = Pynliner().from_string(html).with_cssString(css).run()
            self.assertEqual(
                warning[0].message.message,
                'Pseudoclass :hover invalid or unsupported')
        self.assertEqual(output, expected)

    def test_attribute_selector_match(self):
        html = """<h1 title="foo">Hello World!</h1>"""
        css = """h1[title="foo"] { color: red; }"""
        expected = u"""<h1 title="foo" style="color: red">Hello World!</h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_attribute_selector_no_match(self):
        html = """<h1 title="bar">Hello World!</h1>"""
        css = """h1[title="foo"] { color: red; }"""
        expected = u"""<h1 title="bar">Hello World!</h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_comma_separated_selectors(self):
        html = """<a href="#">Click Here</a><p>Or here</p>"""
        css = """a, p { color: red; }"""
        expected = u"""<a href="#" style="color: red">Click Here</a><p style="color: red">Or here</p>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_complex_comma_separated_selectors(self):
        html = """<div><a class="hi" href="#">Hi</a></div><div><p class="hi">Hi</p></div>"""
        css = """div > a.hi, div > p.hi { color: red; }"""
        expected = u"""<div><a class="hi" href="#" style="color: red">Hi</a></div><div><p class="hi" style="color: red">Hi</p></div>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_immediate_child_with_additional_child_selector(self):
        if hasattr(unittest, 'SkipTest'):
            raise unittest.SkipTest("No support yet for immediate child")
        else:
            return
        return
        html = """<div class="wrapper"><div class="header"><input type="text" /></div></div>"""
        css = """.wrapper > .header input { color: red; }"""
        expected = u"""<div class="wrapper"><div class="header"><input type="text" style="color: red" /></div></div>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_html_comment_ignored(self):
        html = """<div class="hi">Hello<!-- A comment --></div>"""
        css = """div.hi { color: red; }"""
        expected = """<div class="hi" style="color: red">Hello<!-- A comment --></div>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
