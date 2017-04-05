# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import subprocess

import pip
from django.contrib.admin.sites import AdminSite
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_http_methods

from djadmin import settings
from djadmin.models import Sortable
from .sidebar import build_app_dict
from .util import get_all_migrations_status, user_is_authenticated


def configuration(request):
    if user_is_authenticated(request.user):
        site = AdminSite()
        data = site.each_context(request)
        data['available_apps'] = build_app_dict(request)
        all_apps = []
        for pkg in pip.get_installed_distributions():
            all_apps.append({'key': pkg.project_name, 'version': pkg.version})
        data['title'] = _('Configuration')
        data['all_apps'] = sorted(all_apps, key=lambda k: k['key'])
        data['migrations'] = get_all_migrations_status()
        return render(request, 'admin/config.html', context=data)
    return redirect(reverse('admin:login'))


@require_http_methods(["POST"])
def install_library(request):
    ajax_type = request.POST.get("ajax_type", None)
    if not getattr(__builtins__, "WindowsError", None):
        class WindowsError(OSError): pass
    try:
        command = None
        if ajax_type == 'library':
            lib = request.POST.get("lib", None)
            command = 'pip install {0}'.format(lib)
            version = request.POST.get("version", None)
            if version:
                command = '{0}=={1}'.format(command, version)

        elif ajax_type == 'app':
            app_label = request.POST.get('app', None)
            command = 'python {0} migrate'.format(settings.DJADMIN_MANAGE_FILE_NAME)
            if app_label:
                command = '{0} {1}'.format(command, app_label)
        if command:
            proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            stdout, stderr = proc.communicate(command)
            msg = stdout.replace('\n', '<br/>').replace(' ', '&nbsp;')
    except OSError as e:
        msg = e
    return JsonResponse({'msg': msg})


@require_http_methods(["POST"])
def model_sortable(request, model_name, type):
    sort_array = request.POST.get('sortable')
    model = ContentType.objects.get(model=model_name)

    if type == "update":
        model_id_list = []
        for model_id in json.loads(sort_array):
            model_id_list.append(int(model_id))
        Sortable.objects.update_or_create(
            model=model,
            defaults={'sort_array': model_id_list},
        )
    elif type == 'reset':
        try:
            obj = Sortable.objects.get(model=model)
            obj.delete()
        except Sortable.DoesNotExist:
            pass
    return JsonResponse({'status': 200, 'message': _('Successfully updated')})
