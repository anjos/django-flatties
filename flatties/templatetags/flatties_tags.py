#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.dos.anjos@gmail.com>
# Tue 20 Apr 2010 11:09:06 AM CEST 

"""Tags for flatties.
"""

import re
from django import template
from flatties.models import * 

register = template.Library()

@register.simple_tag
def get_title(page, language): 
  return page.get_title(language)

class PageContentNode(template.Node):
  def __init__(self, page, lang):
    self.page = template.Variable(page)
    self.lang = template.Variable(lang)

  def render(self, context):
    try:
      page = self.page.resolve(context)
      if not isinstance(page, Page): raise template.VariableDoesNotExist
    except template.VariableDoesNotExist:
      raise template.TemplateSyntaxError, '"%s" is not a valid flatties.Page' % self.page
    try:
      lang = self.lang.resolve(context)
    except template.VariableDoesNotExist:
      raise template.TemplateSyntaxError, \
          '"%s" is not a valid language code' % self.lang
    return page.get_content(context, lang) 

@register.tag(name='get_content')
def get_page_content(parser, token):
  # This version uses a regular expression to parse tag contents.
  try:
    # Splitting by None == splitting by spaces.
    tag_name, arg = token.contents.split(None, 1)
  except ValueError:
    raise template.TemplateSyntaxError, \
        "%r tag requires arguments (page, lang)" % token.contents.split()[0]
  m = re.search(r'^([\w\.]+) ([\w\.]+)$', arg.strip())
  if not m:
    raise template.TemplateSyntaxError, \
        "%r tag has invalid arguments - review your code." % tag_name
  page, lang = m.groups()
  return PageContentNode(page, lang)
