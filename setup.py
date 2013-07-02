from setuptools import setup, find_packages

setup(
    name='django-inlinecss',
    version="0.1.0",
    description='A Django app useful for inlining CSS (primarily for e-mails)',
    long_description=open('README.md').read(),
    author='Philip Kimmey',
    maintainer='Steve Jalim',
    maintainer_email='steve@somefantastic.co.uk',
    license='BSD',
    url='https://github.com/stevejalim/django-inlinecss',
    download_url='https://github.com/stevejalim/django-inlinecss/downloads',
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
        'Topic :: Communications :: Email',
        'Topic :: Text Processing :: Markup :: HTML',
        ],
    install_requires=[
        'cssutils',
        'BeautifulSoup'
    ]
)
