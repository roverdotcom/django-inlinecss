"""
Test CSS loaders
"""
from django.test import TestCase
from django_inlinecss.css_loaders import StaticFinderCSSLoader, StaticPathCSSLoader


class StaticFinderCSSLoaderTestCase(TestCase):
    def setUp(self):
        self.loader = StaticFinderCSSLoader()
        super(StaticFinderCSSLoaderTestCase, self).setUp()

    def test_debug_mode_uses_staticfiles_finder(self):
        css = self.loader.load('bar.css')
        self.assertIn('div.bar {', css)

    def test_load_file_does_not_exists(self):
        with self.assertRaises(IOError) as e:
            self.loader.load('missing.css')

        self.assertEqual(e.exception.strerror, 'No such file or directory')


class StaticPathCSSLoaderTestCase(TestCase):
    def setUp(self):
        self.loader = StaticPathCSSLoader()
        super(StaticPathCSSLoaderTestCase, self).setUp()

    def test_load_existing_css_file(self):
        css = self.loader.load('bar.css')
        self.assertIn('div.bar {', css)

    def test_load_file_does_not_exists(self):
        with self.assertRaises(IOError) as e:
            self.loader.load('missing.css')

        self.assertEqual(e.exception.strerror, 'No such file or directory')
