from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


try:
    import importlib
except ImportError:
    from django.utils import importlib

DEFAULT_ENGINE = 'django_inlinecss.engines.PynlinerEngine'


def load_class_by_path(path):
    i = path.rfind('.')
    module_path, class_name = path[:i], path[i + 1:]
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def get_engine():
    from django.conf import settings
    engine_path = getattr(settings, 'INLINECSS_ENGINE', DEFAULT_ENGINE)
    return load_class_by_path(engine_path)


def get_css_loader():
    from django.conf import settings

    if settings.DEBUG:
        default_css_loader = 'django_inlinecss.css_loaders.StaticFinderCSSLoader'
    else:
        default_css_loader = 'django_inlinecss.css_loaders.StaticPathCSSLoader'

    engine_path = getattr(settings, 'INLINECSS_CSS_LOADER', default_css_loader)
    return load_class_by_path(engine_path)
