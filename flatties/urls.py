#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.dos.anjos@gmail.com>
# Mon 19 Apr 2010 05:57:29 PM CEST

"""URLs for flat pages
"""

from django.conf.urls import patterns, url
from flatties.views import *

urlpatterns = patterns('',

  url(r'^(?P<url>\w[-\w/]+\w)/$', view_page, name='view'),

)

namespaced = (urlpatterns, 'flatties', 'flatties')



