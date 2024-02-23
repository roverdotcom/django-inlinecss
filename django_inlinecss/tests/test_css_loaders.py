"""
Test CSS loaders
"""

from django.conf import settings
from django.test import TestCase
from django.test import override_settings

from django_inlinecss.css_loaders import StaticfilesFinderCSSLoader
from django_inlinecss.css_loaders import StaticfilesStorageCSSLoader


@override_settings(STATICFILES_DIRS=[settings.STATIC_ROOT], STATIC_ROOT="")
class StaticfilesFinderCSSLoaderTestCase(TestCase):
    def setUp(self):
        self.loader = StaticfilesFinderCSSLoader()
        super().setUp()

    def test_loads_existing_css_file(self):
        css = self.loader.load("bar.css")
        self.assertIn("div.bar {", css)

    def test_load_file_does_not_exist(self):
        with self.assertRaises(IOError) as e:
            self.loader.load("missing.css")

        self.assertEqual(str(e.exception), "missing.css does not exist")


class StaticfilesStorageCSSLoaderTestCase(TestCase):
    def setUp(self):
        self.loader = StaticfilesStorageCSSLoader()
        super().setUp()

    def test_loads_existing_css_file(self):
        css = self.loader.load("bar.css")
        self.assertIn("div.bar {", css)

    def test_load_file_does_not_exist(self):
        with self.assertRaises(IOError) as e:
            self.loader.load("missing.css")

        self.assertEqual(e.exception.strerror, "No such file or directory")
