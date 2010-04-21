#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Ter 17 Mar 2009 14:54:20 CET 

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.safestring import mark_safe
from django.conf import settings
import django.forms

from models import * 

class TranslateTextarea(django.forms.widgets.Textarea):
  def __init__(self, *args, **kwargs):
    super(TranslateTextarea, self).__init__(*args, **kwargs)

  def render(self, name, value, attrs=None):
    v = super(TranslateTextarea, self).render(name, value, attrs)
    v += u' <a href="#" onclick="translate_text(\'%s\');" title="%s"><img style="vertical-align:bottom;" src="http://www.google.com/options/icons/translate.gif" width="16" height="16"/></a>' % \
        (name, ugettext(u'Suggest a translation using Google!'))
    
    return mark_safe(v)

class TranslateTextInput(django.forms.widgets.TextInput):
  def __init__(self, *args, **kwargs):
    super(TranslateTextInput, self).__init__(*args, **kwargs)

  def render(self, name, value, attrs=None):
    v = super(TranslateTextInput, self).render(name, value, attrs)
    v += u' <a href="#" onclick="translate(\'%s\');" title="%s"><img src="http://www.google.com/options/icons/translate.gif" width="16" height="16"/></a>' % \
        (name, ugettext(u'Suggest a translation using Google!'))
    
    return mark_safe(v)

class PageTranslationForm(django.forms.ModelForm):
  title = django.forms.CharField(widget=TranslateTextInput(attrs={'size':40}))
  content = django.forms.CharField(widget=TranslateTextarea(
    attrs={'cols': '85', 'rows': 10}))

  class Meta:
    model = PageTranslation 

  class Media:
    js = ('http://www.google.com/jsapi', 'flatties/js/translate.js')

class PageTranslationAdmin(admin.StackedInline):
  model = PageTranslation
  formset = django.forms.models.inlineformset_factory(Page, PageTranslation)
  form = PageTranslationForm #do not forget that!
  max_num = len(settings.LANGUAGES) - 1
  extra = len(settings.LANGUAGES) - 1
  
def translations(obj):
  return obj.pagetranslation_set.count()
translations.short_description = _(u'Translations')

class PageForm(django.forms.ModelForm):
  url = django.forms.RegexField(label=_("URL"), max_length=100,
    regex=r'^\w[-\w/]+\w$',
    help_text = _("Example: 'about/contact'. Do not write leading and trailing slashes - they will be added automatically."),
    error_message = _("This value must start/end with a letter, digit or underscore. It must contain only letters, numbers, underscores, dashes or slashes."))

  class Meta:
    model = Page

class PageAdmin(admin.ModelAdmin):
  form = PageForm
  list_display = ('title', 'created', 'updated', 'url', 'language', 'user', translations)
  fieldsets = (
      (None, 
        {
          'fields': ('title', 'url', 'language', 'template_name', 'markup', 'content', 'sites'),
        }
      ),
      (_(u'Permissions'), 
        {
          'classes': ('collapse',),
          'fields': ('user', 'groups'), 
        }
      ),
    )
  list_filter = ('title', 'created', 'updated', 'language', 'template_name')
  inlines = [ PageTranslationAdmin, ]

# make it admin'able
admin.site.register(Page, PageAdmin)

