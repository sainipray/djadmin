# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import re

import django
from django import template
from django.apps import apps
from django.conf import settings, global_settings
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import Resolver404, resolve, reverse, NoReverseMatch
from django.db.models import Q
from django.template import TemplateSyntaxError
from django.templatetags.i18n import GetAvailableLanguagesNode
from django.utils.translation import override

from djadmin import settings as djadmin_settings
from ..models import Visitor, DjadminModelSetting
from ..util import get_admin_color_theme

register = template.Library()

CL_VALUE_RE = re.compile('value="([\\d-]+)"')

if django.VERSION >= (1, 9):
    from django.core.urlresolvers import translate_url
else:
    from django.utils.six.moves.urllib.parse import urlsplit, urlunsplit


    def translate_url(url, lang_code):
        parsed = urlsplit(url)
        try:
            match = resolve(parsed.path)
        except Resolver404:
            pass
        else:
            to_be_reversed = "%s:%s" % (match.namespace, match.url_name) if match.namespace else match.url_name
            with override(lang_code):
                try:
                    url = reverse(to_be_reversed, args=match.args, kwargs=match.kwargs)
                except NoReverseMatch:
                    pass
                else:
                    url = urlunsplit((parsed.scheme, parsed.netloc, url, parsed.query, parsed.fragment))
        return url


@register.filter
def admin_change_list_value(result_checkbox_html):
    value = CL_VALUE_RE.findall(result_checkbox_html)
    return value[0] if value else None


@register.filter
def cal_total(app_label, model_name):
    data = apps.get_model(app_label=app_label, model_name=model_name)
    return data.objects.all().count()


@register.assignment_tag
def visitors():
    visitor = Visitor.objects.all().order_by('-visit_datetime')[:10]
    return visitor


@register.assignment_tag
def calc_visitors():
    visit = Visitor.objects.all()
    pc = visit.filter(device_type="PC").count()
    mobile = visit.filter(device_type="Mobile").count()
    tablet = visit.filter(device_type="Tablet").count()
    unknown = visit.filter(device_type="Touch").count()
    unknown += visit.filter(device_type="Bot").count()
    unknown += visit.filter(device_type="Unknown").count()
    return {'pc': pc, 'mobile': mobile, 'tablet': tablet, 'unknown': unknown}


@register.assignment_tag
def next_prev(model):
    next = None
    prev = None
    if model._meta.pk.__class__.__name__ == "AutoField":
        next_queryset = model.__class__.objects.filter(id__gt=model.id).order_by('id')
        prev_queryset = model.__class__.objects.filter(id__lt=model.id).order_by('id')
        if next_queryset:
            next = next_queryset[0].id
        if prev_queryset:
            prev = prev_queryset[prev_queryset.count() - 1].id
    return {'next': next, 'prev': prev}


@register.assignment_tag
def admin_color_theme():
    return get_admin_color_theme(djadmin_settings.ADMIN_COLOR_THEME)


@register.assignment_tag
def history_of_app(app_label, user):
    models = ContentType.objects.filter(app_label=app_label).select_related()
    q = Q()
    log_list = None
    for model in models:
        q |= Q(content_type=model.pk)
    if hasattr(user, 'pk'):
        log_list = LogEntry.objects.filter(q).filter(user=user.pk).select_related().order_by('-action_time')[:10]
    return log_list


@register.assignment_tag
def get_site_header():
    return djadmin_settings.ADMIN_HEADER_TITLE


@register.assignment_tag
def get_file_detail(adminform, field):
    field_data = adminform.form.initial[field]
    field_name = type(field_data).__name__
    try:
        if field_name == 'ImageFieldFile':
            filename, file_extension = os.path.splitext(field_data.url)
            return {'type': 'image', 'width': field_data.width, 'height': field_data.height, 'url': field_data.url,
                    'size': field_data.size, 'extension': file_extension}
        if field_name == 'FieldFile':
            filename, file_extension = os.path.splitext(field_data.url)
            return {'type': 'file', 'url': field_data.url, 'size': field_data.size, 'extension': file_extension}
        return field
    except IOError:
        pass


class EmptyNode(template.Node):
    def render(self, context):
        return ''


@register.tag("get_user_define_available_languages")
def get_user_define_available_languages(parser, token):
    if len(settings.LANGUAGES) != len(global_settings.LANGUAGES) and len(settings.LANGUAGES) > 1:
        args = token.contents.split()
        if len(args) != 3 or args[1] != 'as':
            raise TemplateSyntaxError("'get_user_define_available_languages' requires 'as variable' (got %r)" % args)
        return GetAvailableLanguagesNode(args[2])
    return EmptyNode()


@register.assignment_tag
def get_pk(model, app_label):
    pk = 0
    try:
        obj = DjadminModelSetting.objects.get(model=model, app_label=app_label)
        pk = obj.pk
    except DjadminModelSetting.DoesNotExist:
        pass
    return pk


@register.simple_tag(takes_context=True)
def change_language(context, lang=None):
    path = context['request'].path
    return translate_url(path, lang)
