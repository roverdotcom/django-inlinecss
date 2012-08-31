from django.utils import importlib


DEFAULT_ENGINE = 'django_inlinecss.engines.PynlinerEngine'


def get_engine():
    from django.conf import settings
    engine_path = getattr(settings, 'INLINECSS_ENGINE', DEFAULT_ENGINE)
    i = engine_path.rfind('.')
    module_path, class_name = engine_path[:i], engine_path[i + 1:]
    module = importlib.import_module(module_path)
    return getattr(module, class_name)
