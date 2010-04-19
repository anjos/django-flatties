#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Seg 14 Set 2009 14:42:06 CEST 

"""Installation instructions for django-ordered-model
"""

from setuptools import setup, find_packages

setup(

    name = 'django-flatties',
    version = '0.1',
    packages = find_packages(),

    # we also need all translation files and templates
    package_data = {
      'flatties': [
        'locale/*/LC_MESSAGES/django.po',
        'locale/*/LC_MESSAGES/django.mo',
        'media/js/*.js',
        ],
      },

    entry_points = {
      },

    zip_safe=False,

    install_requires = [
      'Django>=1.1',
      'docutils',
      'textile',
      ],

    # metadata for upload to PyPI
    author = 'André Anjos',
    author_email = "andre.dos.anjos@gmail.com",
    description = 'A django application that provides translatable flat pages',
    license = "GPL v2 or superior",
    keywords = "django flatpage i18n translatable",
    url = 'http://andreanjos.org/project/django-flatties/',
)
