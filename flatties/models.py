from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.template import Template
from utils import *

class Page(models.Model):
  """A flat page model."""

  login_choices = (
      ('X', _(u'Any user')),
      ('L', _(u'Authenticated')),
      ('N', _(u'Anonymous')),
      ('A', _(u'Administrator')),
      ('S', _(u'Staff')),
      ('G', _(u'Belonging to a group')),
      )

  markup_choices = (
      ('R', _(u'Raw HTML')),
      ('S', _(u'ReStructured Text')),
      ('T', _(u'Textile')),
      )

  url = models.CharField(_('URL'), max_length=100, db_index=True, blank=False,
      null=False)

  created = models.DateTimeField(_('Created'), null=False, blank=False,
    auto_now_add=True, editable=False)

  updated = models.DateTimeField(_('Updated'), null=False, blank=False,
    auto_now=True, editable=False)

  title = models.CharField(_('title'), max_length=200,
      help_text=_('The title of the page will be extracted from this variable. No markup or variable resolution is allowed.'))

  markup = models.CharField(_('Markup'), max_length=1,
    choices=markup_choices, default='R', null=False, blank=False,
    help_text=_('Choose here if you need some preprocessing of the contents based on a markup language. By default, we will display exactly what you write in the content field.'))

  content = models.TextField(_('content'), blank=True,
      help_text=_('These are the contents of the page. You can use templates and markup language if you decide to do so.'))

  template_name = models.CharField(_('template name'), max_length=70,
      blank=True, help_text=_("Example: 'flatties/about.html'. If this isn't provided, the system will use 'flatties/default.html'."))

  language = models.CharField(_('Language'), max_length=8, null=False, blank=False, help_text=_('Choose the language to which the name applies to.'), choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)

  user = models.CharField(_('User type'), default='X', max_length=1,
      choices=login_choices, help_text=_('Set this to determine if the page will be showed only to a subgroup of users.'))

  groups = models.ManyToManyField(Group, null=True, blank=True,
      help_text=_('If you have set "For users in a group" as the user type choice, select here the groups of users which will see this page. Otherwise, this parameter is ignored.'))

  sites = models.ManyToManyField(Site, null=True, blank=True,
      help_text=_('Select here the sites to which this page is effective.'))

  def is_allowed(self, user):
    """Tells if the given user/site is allowed to see this menu page."""
    if Site.objects.get_current() not in self.sites.all(): return False

    if self.user == 'X': return True
    elif self.user == 'L' and user.is_authenticated(): return True
    elif self.user == 'N' and not user.is_authenticated(): return True
    elif self.user == 'A' and user.is_superuser: return True
    elif self.user == 'S' and user.is_staff: return True
    elif self.user == 'G' and self.groups.all() and \
      [k for k in self.groups.all() if k in user.groups.all()]: return True

    # if you missed all other entries, you cannot see this one...
    return False

  def get_title(self, language):
    """Returns the title of this page (translated, if possible).""" 
    try: return self.pagetranslation_set.get(language=language).title
    except: return self.title

  def get_content(self, context, language):
    """Returns the contents of this page (translated, if possible) and filtered.""" 

    def filter(markup, content):
      if markup == 'R': return raw(content) 
      elif markup == 'S': return restructuredtext(content)
      elif markup == 'T': return textile(content)
      else: raise RuntimeError, 'Unknown markup (%s)' % markup

    try: filter(self.markup, Template(self.pagetranslation_set.get(language=language).content).render(context))
    except: filter(self.markup, Template(self.content).render(context))

  class Meta:
      verbose_name = _('page')
      verbose_name_plural = _('pages')
      ordering = ('url',)

  def __unicode__(self):
      return u"/%s/ -- %s (%s)" % (self.url, self.title, self.language)

class PageTranslation(models.Model):
  """A translation to the title and contents of the page."""

  page = models.ForeignKey(Page)

  language = models.CharField(_('Language'), max_length=8, null=False, blank=False, help_text=_('Choose the language to which this variant applies to.'), choices=settings.LANGUAGES)

  title = models.CharField(_('title'), max_length=200)

  content = models.TextField(_('content'), blank=True)

  class Meta:
    verbose_name = _('page translation')
    verbose_name_plural = _('page translations')

  def __unicode__(self):
    return u"/%s/ -- %s (%s)" % (self.page.url, self.title, self.language)
