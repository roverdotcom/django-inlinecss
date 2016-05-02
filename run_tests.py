#!/usr/bin/env python

# Short way to bootstrap Django test runner:
# taken from django-extensions (which also has
# a comment suggesting it was taken originally from
# from http://www.travisswicegood.com/2010/01/17/
#           django-virtualenv-pip-and-fabric/
import os
import sys

import django
import django.conf

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)


def main():
    django.conf.settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django_inlinecss'
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
        }],
        STATIC_URL='/static/',
        DEBUG=True
    )
    django.setup()

    django.core.management.call_command('test', 'django_inlinecss')

if __name__ == '__main__':
    main()
