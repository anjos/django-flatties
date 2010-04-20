#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.dos.anjos@gmail.com>
# Mon 19 Apr 2010 06:03:59 PM CEST 

"""Views for flatties.
"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist

from models import Page

def view_page(request, url):
  obj = Page.objects.get(url=url)
  if not obj.is_allowed(request.user): raise ObjectDoesNotExist 
  template = obj.template_name
  if not template: template = "flatties/default.html"
  return render_to_response(template, { 'object': obj, }, 
                            context_instance=RequestContext(request))
