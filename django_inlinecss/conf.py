try:
    import importlib
except ImportError:
    from django.utils import importlib

DEFAULT_ENGINE = "django_inlinecss.engines.PynlinerEngine"
DEFAULT_CSS_LOADER = "django_inlinecss.css_loaders.StaticfilesStorageCSSLoader"


def load_class_by_path(path):
    i = path.rfind(".")
    module_path, class_name = path[:i], path[i + 1 :]
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def get_engine():
    from django.conf import settings

    engine_path = getattr(settings, "INLINECSS_ENGINE", DEFAULT_ENGINE)
    return load_class_by_path(engine_path)


def get_css_loader():
    from django.conf import settings

    engine_path = getattr(settings, "INLINECSS_CSS_LOADER", DEFAULT_CSS_LOADER)
    return load_class_by_path(engine_path)
