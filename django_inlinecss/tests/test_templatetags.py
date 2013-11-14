"""
Test the functioning of the templatetag itself.

The actual CSS inlining displayed here is extremely simple:
tests of the CSS selector functionality is independent.
"""
import os

from django.test import TestCase
from django.test.utils import override_settings
from django.conf import settings
from django.utils.safestring import mark_safe

from django.template import Context
from django.template.loader import get_template

from mock import patch

from django_inlinecss.tests.constants import TESTS_TEMPLATE_DIR
from django_inlinecss.tests.constants import TESTS_STATIC_DIR


templates_override = settings.TEMPLATE_DIRS + (TESTS_TEMPLATE_DIR,)


@override_settings(
    TEMPLATE_DIRS=templates_override,
    STATIC_ROOT=TESTS_STATIC_DIR)
class InlineCssTests(TestCase):
    def setUp(self):
        super(InlineCssTests, self).setUp()

    def assert_foo_and_bar_rendered(self, rendered):
        foo_div_regex = (
            r'<div class="foo" style="margin: 10px 15px 20px 25px">'
            '\s+This is the "foo" div.\s+'
            '<\/div>')
        self.assertRegexpMatches(
            rendered,
            foo_div_regex)

        bar_div_regex = (
            r'<div class="bar" style="padding: 10px 15px 20px 25px">'
            '\s+This is the "bar" div.\s+'
            '<\/div>')
        self.assertRegexpMatches(
            rendered,
            bar_div_regex)

    def test_single_staticfiles_css(self):
        """
        Test the basic inlining case of using the staticfiles loader
        to load a CSS file and inline it as part of a rendering step.
        """
        template = get_template('single_staticfiles_css.html')
        rendered = template.render(Context({}))
        self.assert_foo_and_bar_rendered(rendered)

    def test_multiple_staticfiles_css(self):
        """
        Test the multiple inlining case of using the staticfiles loader.

        This tests that passing two css files works.
        """
        template = get_template('multiple_staticfiles_css.html')
        rendered = template.render(Context({}))
        self.assert_foo_and_bar_rendered(rendered)

    def test_variable_defined_staticfiles_css(self):
        """
        Test that the staticfiles paths passed to the templatetag
        may be defined as variables instead of strings.
        """
        template = get_template('variable_defined_staticfiles_css.html')
        context = Context({'foo_css': 'foo.css', 'bar_css': 'bar.css'})

        rendered = template.render(context)
        self.assert_foo_and_bar_rendered(rendered)

    def test_variable_and_string_defined_staticfiles_css(self):
        """
        Test that we can mix and match variable-defined CSS files &
        those defined quoted in the templatetag.
        """
        template = get_template(
            'variable_and_string_defined_staticfiles_css.html')
        context = Context({'foo_css': 'foo.css'})
        rendered = template.render(context)
        self.assert_foo_and_bar_rendered(rendered)

    def test_inline_css(self):
        """
        Test that <style> tags are pulled out and used to render the
        content wrapped in the inlinecss block.
        """
        template = get_template('inline_css.html')
        rendered = template.render(Context({}))
        self.assert_foo_and_bar_rendered(rendered)

    def test_context_vars_render_first(self):
        """
        Test that context variables are fully rendered before
        the inline css step is undertaken.
        """
        template = get_template('context_vars_render_first.html')
        context = Context({
            'foo_div_open_tag': mark_safe('<div class="foo">'),
            'bar_div_open_tag': mark_safe('<div class="bar">')})
        rendered = template.render(context)
        self.assert_foo_and_bar_rendered(rendered)

    def test_template_inheritance(self):
        """
        Test the inlining CSS works through template inheritance
        structures.
        """
        template = get_template('template_inheritance.html')
        rendered = template.render(Context({}))
        self.assert_foo_and_bar_rendered(rendered)

    def test_unicode_context_variables(self):
        """
        Test unicode values in the template do not break
        template rendering.
        """
        template = get_template('unicode_context_variables.html')

        rendered = template.render(Context({
            'unicode_string': u'I love playing with my pi\xf1ata'}))
        self.assertRegexpMatches(
            rendered,
            '<div class="bar" style="padding: 10px 15px 20px 25px">')
        self.assertRegexpMatches(
            rendered,
            u'I love playing with my pi\xf1ata')

    def test_comments_are_ignored(self):
        """
        Test that comments are ignored in the templatetag rendering
        step.

        With older BeautifulSoup the comments can be double escaped
        leading to something like:
            <!--<!-- Comment -->-->
        """
        template = get_template('comments_are_ignored.html')

        rendered = template.render(Context({}))
        self.assertRegexpMatches(
            rendered,
            '<body>\s+<!-- Here is comment one -->\s+<div')
        self.assertRegexpMatches(
            rendered,
            'This is the "foo" div.\s+<!-- comment two -->\s+')
        self.assertRegexpMatches(
            rendered,
            'This is the "bar" div.\s+<!-- comment three -->\s+')


@override_settings(
    TEMPLATE_DIRS=templates_override,
    STATIC_ROOT=TESTS_STATIC_DIR)
class DebugModeStaticfilesTests(TestCase):
    @override_settings(DEBUG=True)
    @patch('django.contrib.staticfiles.finders.find')
    def test_debug_mode_uses_staticfiles_finder(self, find):
        full_path = os.path.join(TESTS_STATIC_DIR, "foobar.css")
        find.return_value = full_path
        template = get_template('single_staticfiles_css.html')
        template.render(Context({}))
        find.assert_called_once_with("foobar.css")

    @patch('django.contrib.staticfiles.storage.staticfiles_storage.path')
    def test_non_debug_mode_uses_staticfiles_storage(self, path):
        full_path = os.path.join(TESTS_STATIC_DIR, "foobar.css")
        path.return_value = full_path
        template = get_template('single_staticfiles_css.html')
        template.render(Context({}))
        path.assert_called_once_with("foobar.css")
