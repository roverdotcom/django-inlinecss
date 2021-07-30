from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage


class BaseCSSLoader:
    def __init__(self):
        pass

    def load(self, path):
        """
        Retrieves the contents of the static asset specified
        :param path: path to the desired asset
        :return: contents of asset
        """
        raise NotImplementedError()


class StaticfilesFinderCSSLoader(BaseCSSLoader):
    def load(self, path):
        """
        Retrieve CSS contents from the local filesystem with static finders
        """
        expanded_path = finders.find(path)

        if expanded_path is None:
            raise OSError(f"{path} does not exist")

        with open(expanded_path, "rb") as css_file:
            return css_file.read().decode("utf-8")


class StaticfilesStorageCSSLoader(BaseCSSLoader):
    def load(self, path):
        """
        Retrieve CSS contents with staticfiles storage
        """
        return staticfiles_storage.open(path).read().decode("utf-8")
