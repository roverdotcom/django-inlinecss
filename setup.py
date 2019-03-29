from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals
from setuptools import setup, find_packages

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
        'Programming Language :: Python :: 3.7',
        'Topic :: Communications :: Email',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
    install_requires=[
        'Django>=1.11',
        'pynliner',
        'mock',
        'future>=0.16.0',
    ],
)
