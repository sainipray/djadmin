#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.urls import NoReverseMatch, reverse
from django.utils.text import capfirst


def build_app_dict(request, label=None, name=None):
    app_dict = {}
    models = admin.site._registry

    for model, model_admin in models.items():
        app_label = model._meta.app_label

        has_module_perms = model_admin.has_module_permission(request)
        if not has_module_perms:
            if label:
                raise PermissionDenied
            continue

        perms = model_admin.get_model_perms(request)
        if True not in perms.values():
            continue

        info = (app_label, model._meta.model_name)
        model_dict = {
            'name': capfirst(model._meta.verbose_name_plural),
            'object_name': model._meta.object_name,
            'perms': perms,
        }
        if perms.get('change'):
            try:
                model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info, current_app=name)
            except NoReverseMatch:
                pass
        if perms.get('add'):
            try:
                model_dict['add_url'] = reverse('admin:%s_%s_add' % info, current_app=name)
            except NoReverseMatch:
                pass

        if app_label in app_dict:
            app_dict[app_label]['models'].append(model_dict)
        else:
            app_dict[app_label] = {
                'name': apps.get_app_config(app_label).verbose_name,
                'app_label': app_label,
                'app_url': reverse(
                    'admin:app_list',
                    kwargs={'app_label': app_label},
                    current_app=name,
                ),
                'has_module_perms': has_module_perms,
                'models': [model_dict],
            }

    if label:
        return app_dict.get(label)
    app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
    return app_list
