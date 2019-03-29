#!/usr/bin/env python

# Short way to bootstrap Django test runner:
# taken from django-extensions (which also has
# a comment suggesting it was taken originally from
# from http://www.travisswicegood.com/2010/01/17/
#           django-virtualenv-pip-and-fabric/
import os
import sys

import django
from django.conf import settings
from django.core.management import call_command

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)


def main():
    settings.configure(
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
        TEMPLATES = [{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(PROJECT_ROOT,"django_inlinecss","tests","templates"),],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        }],
        STATIC_URL='/static/',
        DEBUG=True
    )

    django.setup()
    call_command('test', 'django_inlinecss')

if __name__ == '__main__':
    main()
