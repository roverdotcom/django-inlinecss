from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from setuptools import find_packages
from setuptools import setup


# What packages are required for this module to be executed?
REQUIRED = [
    'Django>=1.11',
    'pynliner',
    'future>=0.16.0',
]

# What packages are required only for tests?
TESTS = [
    'mock==2.0.0',
    'pytest==4.3.1',
    'pytest-django==3.4.8',
]

# What packages are optional?
EXTRAS = {
    'flake8': [
        'flake8==3.6.0',
        'flake8-isort==2.6.0',
        'isort==4.3.4',
        'testfixtures==6.3.0',
    ],
}


setup(
    name='django-inlinecss',
    version="0.1.2",
    description='A Django app useful for inlining CSS (primarily for e-mails)',
    long_description=open('README.md').read(),
    author='Philip Kimmey',
    author_email='philip@rover.com',
    maintainer='Philip Kimmey',
    maintainer_email='philip@rover.com',
    license='BSD',
    url='https://github.com/roverdotcom/django-inlinecss',
    download_url='https://github.com/roverdotcom/django-inlinecss/releases',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    keywords=['html', 'css', 'inline', 'style', 'email'],
    classifiers=[
        'Environment :: Other Environment',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications :: Email',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
    install_requires=REQUIRED,
    tests_require=TESTS,
    extras_require=EXTRAS,
)
