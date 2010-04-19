#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Mon 20 Oct 11:19:56 2008 

"""Context processors for standard things on every template rendering
"""

from django.contrib.sites.models import Site

def current_site(request):
  return {'site': Site.objects.get_current()}
