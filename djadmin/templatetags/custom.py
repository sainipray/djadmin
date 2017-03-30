# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import re

from django import template
from django.apps import apps
from django.conf import settings, global_settings
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import translate_url
from django.db.models import Q
from django.template import TemplateSyntaxError
from django.templatetags.i18n import GetAvailableLanguagesNode

from ..models import Visitor, DjadminModelSetting
from ..util import get_admin_color_theme

register = template.Library()

CL_VALUE_RE = re.compile('value="(.*)\"')


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
    Mobile = visit.filter(device_type="Mobile").count()
    Tablet = visit.filter(device_type="Tablet").count()
    Unknown = visit.filter(device_type="Touch").count()
    Unknown += visit.filter(device_type="Bot").count()
    Unknown += visit.filter(device_type="Unknown").count()
    return {'pc': pc, 'mobile': Mobile, 'tablet': Tablet, 'unknown': Unknown}


@register.assignment_tag
def next_prev(Model):
    Next = None
    Prev = None
    if Model._meta.pk.__class__.__name__ == "AutoField":
        Next_Queryset = Model.__class__.objects.filter(id__gt=Model.id).order_by('id')
        Prev_Queryset = Model.__class__.objects.filter(id__lt=Model.id).order_by('id')
        if Next_Queryset:
            Next = Next_Queryset[0].id
        if Prev_Queryset:
            Prev = Prev_Queryset[Prev_Queryset.count() - 1].id
    return {'next': Next, 'prev': Prev}


@register.assignment_tag
def admin_color_theme():
    admin_color_theme = getattr(settings, 'ADMIN_COLOR_THEME', 'cyan')
    ADMIN_COLOR_THEME = get_admin_color_theme(admin_color_theme)
    return ADMIN_COLOR_THEME


@register.assignment_tag
def history_of_app(app_label, user):
    models = ContentType.objects.filter(app_label=app_label).select_related()
    q = Q()
    for model in models:
        q |= Q(content_type=model.pk)
    log_list = LogEntry.objects.filter(q).filter(user=user.pk).select_related().order_by('-action_time')[:10]
    return log_list


@register.assignment_tag
def get_site_header():
    get_site_title = "Django administrator"
    if hasattr(settings, 'ADMIN_HEADER_TITLE'):
        get_site_title = settings.ADMIN_HEADER_TITLE
    return get_site_title


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
    except:
        pass
    return pk


@register.simple_tag(takes_context=True)
def change_language(context, lang=None, *args, **kwargs):
    path = context['request'].path
    return translate_url(path, lang)
