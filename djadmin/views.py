import subprocess

import pip
from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import NoReverseMatch, reverse
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.text import capfirst

from .util import remaining_migrations


def _build_app_dict(request, label=None, name=None):
    """
    Builds the app dictionary. Takes an optional label parameters to filter
    models of a specific app.
    """
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

        # Check whether user has any perm for this module.
        # If so, add the module to the model_list.
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
    return app_dict


def about(request):
    site = AdminSite()
    # base_url = "https://pypi.python.org/pypi/"
    data = site.each_context(request)
    avai = _build_app_dict(request)
    app_list = sorted(avai.values(), key=lambda x: x['name'].lower())
    data['available_apps'] = app_list
    all_apps = []
    for pkg in pip.get_installed_distributions():
        # url = base_url + pkg.project_name + "/json"
        # req = requests.get(url)
        # pkg_data = json.loads(req.text)
        # latest_version = pkg_data['info']['version']
        all_apps.append({'key': pkg.project_name, 'version': pkg.version})
    data['title'] = 'About'
    data['all_apps'] = sorted(all_apps, key=lambda k: k['key'])
    data['migrations'] = remaining_migrations()
    return render(request, 'admin/about.html', context=data)


def InstallLibrary(request):
    if request.method == "POST":
        lib = request.POST.get("lib", None)
        version = request.POST.get("version", None)
        upgradeBool = int(request.POST.get("upgradeBool", None))
        if not getattr(__builtins__, "WindowsError", None):
            class WindowsError(OSError): pass
        try:
            if upgradeBool:
                # python - m pip install - -upgrade djadmin
                # subprocess.check_call([sys.executable, "-m","pip","install","--upgrade",lib])
                subprocess.check_call(["python", "-m", "pip", "install", lib + "==" + version])
                # pip.main(['install', '--upgrade', 'requests'])
                msg = "Successfully upgraded"
                notify = 1
            else:
                if version:
                    # subprocess.check_call([sys.executable, "-m","pip","install",lib+"=="+version])
                    subprocess.check_call(["python", "-m", "pip", "install", lib + "==" + version])
                    msg = "Succesfully installed version %s" % format(version)
                    notify = 1
                else:
                    msg = "Version not found"
                    notify = 0
        except OSError as e:
            msg = e
            notify = 0
    return JsonResponse({'msg': msg, 'notify': notify})
