"""
Test CSS loaders
"""
import os

from django.test import TestCase
from django.test.utils import override_settings

from mock import patch

from django_inlinecss.tests.constants import TESTS_STATIC_DIR
from django_inlinecss.css_loaders import StaticFinderCSSLoader, StaticPathCSSLoader


@override_settings(STATIC_ROOT=TESTS_STATIC_DIR)
class StaticFinderCSSLoaderTestCase(TestCase):
    def setUp(self):
        self.loader = StaticFinderCSSLoader()
        super(StaticFinderCSSLoaderTestCase, self).setUp()

    @patch('django.contrib.staticfiles.finders.find')
    def test_debug_mode_uses_staticfiles_finder(self, find):
        full_path = os.path.join(TESTS_STATIC_DIR, 'bar.css')
        find.return_value = full_path
        css = self.loader.load(full_path)
        self.assertIn('div.bar {', css)

    @patch('django.contrib.staticfiles.finders.find')
    def test_load_file_does_not_exists(self, find):
        full_path = os.path.join(TESTS_STATIC_DIR, 'missing.css')
        find.return_value = full_path
        with self.assertRaises(IOError) as e:
            self.loader.load('missing.css')

        self.assertEqual(e.exception.strerror, 'No such file or directory')


@override_settings(STATIC_ROOT=TESTS_STATIC_DIR)
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
