from setuptools import setup, find_packages

setup(
    name='django-inlinecss',
    version="0.1.1",
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
        'Topic :: Communications :: Email',
        'Topic :: Text Processing :: Markup :: HTML',
        ],
    install_requires=[
        'Django',
        'cssutils',
        'BeautifulSoup',
        'mock'
    ]
)
