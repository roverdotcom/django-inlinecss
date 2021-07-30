import os
import sys
from shutil import rmtree

from setuptools import Command
from setuptools import find_packages
from setuptools import setup

# Package meta-data.
NAME = 'django-inlinecss'
SRC_DIR = 'django_inlinecss'
DESCRIPTION = 'A Django app useful for inlining CSS (primarily for e-mails)'
URL = 'https://github.com/roverdotcom/django-inlinecss'
EMAIL = 'philip@rover.com'
AUTHOR = 'Philip Kimmey'
REQUIRES_PYTHON = '>=3.8'
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = [
    'Django>=3.2',
    'pynliner',
    'future>=0.16.0',
]

# What packages are required only for tests?
TESTS = [
    'mock==5.1.0',
    'pytest==8.0.1',
    'pytest-django==4.8.0',
]

# What packages are optional?
EXTRAS = {
    'flake8': [
        'flake8==7.0.0',
        'flake8-isort==6.1.1',
        'isort==5.13.2',
        'testfixtures==8.0.0',
    ],
    "tests": TESTS,
}

here = os.path.abspath(os.path.dirname(__file__))


# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!

try:
    with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, SRC_DIR, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print(f"\033[1m{s}\033[0m")

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system(f"{sys.executable} setup.py sdist bdist_wheel --universal")

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    license="MIT",
    url=URL,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    keywords=["html", "css", "inline", "style", "email"],
    classifiers=[
        "Environment :: Other Environment",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Communications :: Email",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    install_requires=REQUIRED,
    tests_require=TESTS,
    extras_require=EXTRAS,
    # $ setup.py upload support.
    cmdclass={
        "upload": UploadCommand,
    },
)
