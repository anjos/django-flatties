#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.dos.anjos@gmail.com>
# Mon 19 Apr 2010 05:10:51 PM CEST 

"""A few utility methods for pages.
"""

from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe

def raw(value):
  """Returns simple html and mark it safe."""
  return mark_safe(force_unicode(value))

def textile(value):
  """Converts the text data into html using textile"""
  try:
    import textile
  except ImportError:
    if django_settings.DEBUG: raise
    return simple_text('[warning: textile is *not* available]\n' + value) 
  else:
    return raw(textile.textile(smart_str(value), encoding='utf-8', output='utf-8'))

def restructuredtext(value):
  """Converts the text data into html using docutils"""
  try:
    from docutils.core import publish_parts
  except ImportError:
    if settings.DEBUG: raise
    return simple_text('[warning: docutils is *not* available]\n\n' + value) 
  else:
    docutils_settings = getattr(django_settings, 
        "RESTRUCTUREDTEXT_FILTER_SETTINGS", {})
    parts = publish_parts(source=smart_str(value), writer_name="html4css1", 
        settings_overrides=docutils_settings)
    return raw(parts["fragment"])



