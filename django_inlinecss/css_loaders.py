from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage


def load_css_by_path(path):
    with open(path) as css_file:
        return css_file.read()


class BaseCSSLoader(object):
    def __init__(self):
        pass

    def load(self, path):
        """
        Retrieves the contents of the static asset specified
        :param path: path to the desired asset
        :return: contents of asset
        """
        raise NotImplementedError()


class StaticFinderCSSLoader(BaseCSSLoader):
    def load(self, path):
        """
        Retrieve CSS contents by static finders
        """
        expanded_path = finders.find(path)
        return load_css_by_path(expanded_path)


class StaticPathCSSLoader(BaseCSSLoader):
    def load(self, path):
        """
        Retrieve CSS contents by local file system
        """
        expanded_path = staticfiles_storage.path(path)
        return load_css_by_path(expanded_path)
