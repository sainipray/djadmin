import re
from importlib import import_module

from django.conf import settings
from django.contrib.admin.templatetags.admin_list import (result_headers,
                                                          result_hidden_fields,
                                                          results)
from django.urls import reverse
from django.template import Library

from .base import AdminReadonlyField, Inline
from .base import Layout, Fieldset, Row
from .compat import simple_tag

register = Library()

CL_VALUE_RE = re.compile('value="(.*)\"')


def get_admin_site():
    site_module = getattr(
        settings,
        'DJADMIN_SITE',
        'django.contrib.admin.site'
    )
    mod, inst = site_module.rsplit('.', 1)
    mod = import_module(mod)
    return getattr(mod, inst)


site = get_admin_site()


@register.simple_tag
def fieldset_layout(adminform, inline_admin_formsets):
    layout = getattr(adminform.model_admin, 'layout', None)
    if layout is not None:
        for element in layout.elements:
            # TODO Ugly hack to substitute inline classes to instances
            if isinstance(element, Inline) and isinstance(element.inline, type):
                for inline in inline_admin_formsets:
                    if inline.formset.model == element.inline.model:
                        element.inline = inline
        return layout

    sets = []

    for fieldset in adminform:
        fields = []

        for line in fieldset:
            line_fields = []

            for fieldset_field in line:
                field = None

                if getattr(fieldset_field, 'is_readonly', False):
                    field = AdminReadonlyField(fieldset_field)
                else:
                    field = fieldset_field.field.name

                line_fields.append(field)

            if len(line_fields) == 1:
                fields.append(line_fields[0])
            else:
                fields.append(Row(*line_fields))

        if fieldset.name:
            sets.append(Fieldset(fieldset.name, *fields))
        else:
            sets += fields

    for inline in inline_admin_formsets:
        sets.append(Inline(inline))

    return Layout(*sets)


def admin_related_field_urls(bound_field):
    from django.contrib.admin.views.main import IS_POPUP_VAR, TO_FIELD_VAR

    rel_widget = bound_field.field.widget
    rel_opts = rel_widget.rel.model._meta
    info = (rel_opts.app_label, rel_opts.model_name)
    rel_widget.widget.choices = rel_widget.choices
    url_params = '&'.join("%s=%s" % param for param in [
        (TO_FIELD_VAR, rel_widget.rel.get_related_field().name),
        (IS_POPUP_VAR, 1),
    ])

    context = {
        'widget': rel_widget.widget.render(bound_field.name, bound_field.value()),
        'name': bound_field.name,
        'url_params': url_params,
        'model': rel_opts.verbose_name,
    }
    if rel_widget.can_change_related:
        change_related_template_url = rel_widget.get_related_url(info, 'change', '__fk__')
        context.update(
            can_change_related=True,
            change_related_template_url=change_related_template_url,
        )
    if rel_widget.can_add_related:
        add_related_url = rel_widget.get_related_url(info, 'add')
        context.update(
            can_add_related=True,
            add_related_url=add_related_url,
        )
    if rel_widget.can_delete_related:
        delete_related_template_url = rel_widget.get_related_url(info, 'delete', '__fk__')
        context.update(
            can_delete_related=True,
            delete_related_template_url=delete_related_template_url,
        )

    return context


simple_tag(register, admin_related_field_urls)


def admin_select_related_link(bound_field):
    """
    {% admin_select_related_link bound_field as rel_field_urls %}
    """
    rel_widget = bound_field.field.widget
    rel_to = rel_widget.rel.model
    if rel_to in rel_widget.admin_site._registry:
        related_url = reverse(
            'admin:%s_%s_changelist' % (
                rel_to._meta.app_label,
                rel_to._meta.model_name,
            ),
            current_app=rel_widget.admin_site.name,
        )
        params = rel_widget.url_parameters()
        if params:
            related_url += '?' + '&amp;'.join('%s=%s' % (k, v) for k, v in params.items())
        return {'related_url': related_url}
    return {}


simple_tag(register, admin_select_related_link)


@register.inclusion_tag("admin/change_list_results.html")
def result_sortable_list(cl):
    """
    Displays the headers and data list together
    """
    if not cl.params.get('o',None):
        # Disable sortable when admin filter data from result table according to fields
        from ..models import Sortable
        cl.result_list = Sortable.get_sortable_row(cl.opts.model_name, cl.result_list)
    headers = list(result_headers(cl))
    num_sorted_fields = 0
    for h in headers:
        if h['sortable'] and h['sorted']:
            num_sorted_fields += 1
    return {'cl': cl,
            'result_hidden_fields': list(result_hidden_fields(cl)),
            'result_headers': headers,
            'num_sorted_fields': num_sorted_fields,
            'results': list(results(cl))}

@register.simple_tag
def list_count(app_label, model_name):
    from django.apps import apps
    Model = apps.get_model(app_label=app_label, model_name=model_name)
    return Model.objects.count()

@register.simple_tag
def dashboard_icon(model_name):
    if hasattr(settings, 'DASHBOARD_ICONS'):
        icon =  settings.DASHBOARD_ICONS.get(model_name)
        if icon:
            return icon
    return "mdi-format-align-center"
