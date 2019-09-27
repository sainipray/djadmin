# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
from hashlib import md5

import django
from django.contrib.sessions.models import Session
from django.core.cache import cache
from django.urls import Resolver404, resolve
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.loader import MigrationLoader
from django.db.models import ForeignKey
from django.db.models import Q
from user_agents import parse

from djadmin.colors import colors
from .models import DjadminField

if sys.version_info[0] == 3:
    text_type = str
else:
    text_type = unicode


def get_cache_key(ua_string):
    if isinstance(ua_string, text_type):
        ua_string = ua_string.encode('utf-8')
    return ''.join(['django_user_agents.', md5(ua_string).hexdigest()])


def get_user_agent(request):
    ua_string = request.META.get('HTTP_USER_AGENT', '')
    key = get_cache_key(ua_string)
    user_agent = cache.get(key)
    if user_agent is None:
        user_agent = parse(ua_string)
        cache.set(key, user_agent)
    return user_agent


def get_and_set_user_agent(request):
    if hasattr(request, 'user_agent'):
        return request.user_agent

    request.user_agent = get_user_agent(request)
    return request.user_agent


def get_all_migrations_status():
    list_data = {'migrated_apps': '', 'unmigrated_apps': ''}
    connection = connections[DEFAULT_DB_ALIAS]
    connection.prepare_database()
    self = MigrationLoader(connection)
    self.load_disk()
    list_data['migrated_apps'] = self.migrated_apps
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    list_data['unmigrated_apps'] = set([app[0].app_label for app in executor.migration_plan(targets)])
    return list_data
    # executor.migrate(targets) for migrate model


def get_admin_color_theme(color_theme):
    try:
        admin_color_theme = color_theme.strip().lower().split(' ')
        return admin_color_theme[0] if len(admin_color_theme) < 2 else '{0} {1}'.format(
            admin_color_theme[1], admin_color_theme[0])
    except KeyError:
        sys.stdout.write('Please use correct color combination like: "purple" or "purple darken-1"\n')
        raise


def get_admin_color_theme_hex_code(color_theme):
    admin_color_theme = color_theme.strip().lower().split(' ')
    return colors[admin_color_theme[0]][
        admin_color_theme[1] if len(admin_color_theme) > 1 else 'base']


def calculate_action_field_list(first_list, second_list, order_type):
    field_name = None
    field_type = None
    data = []
    second_field = None
    for first_field in first_list:
        for second_field in second_list:
            if first_field.name == second_field.name:
                field_name = True
                if order_type:
                    field_type = True if first_field.type == second_field.__class__.__name__ else False
                else:
                    field_type = True if first_field.__class__.__name__ == second_field.type else False
                break
            else:
                field_name = False
        if not field_name:
            if '__' in first_field.name:
                if first_field.name.split('__')[0] in data:
                    data.append(first_field)
                else:
                    continue
            if order_type:
                DjadminField.objects.filter(
                    Q(name__endswith="__{0}".format(first_field.name),
                      foreignkey_model__exact=first_field.model)).delete()
            elif second_list:
                foreign_key_models = DjadminField.objects.filter(foreignkey_model__exact=first_field.model.__name__,
                                                                 type=ForeignKey.__name__)
                for models in foreign_key_models:
                    field_name = models.name + "__{0}".format(first_field.name)
                    DjadminField.objects.create(name=field_name, model=models.model,
                                                type=first_field.__class__.__name__, depth=9,
                                                foreignkey_model=first_field.model.__name__)
            data.append(first_field)
        elif not field_type:
            if order_type:
                DjadminField.objects.filter(
                    Q(name__endswith="__{0}".format(first_field.name), foreignkey_model__exact=first_field.model) |
                    Q(name__exact=first_field.name, model__exact=first_field.model)).update(
                    type=second_field.__class__.__name__)
    return data


def user_is_authenticated(user):
    if django.VERSION >= (1, 10):
        return user.is_authenticated
    else:
        return user.is_authenticated()


def is_session_exist(request):
    if request.session.session_key and request.session.exists(request.session.session_key):
        return True
    return False


def get_session(request):
    if is_session_exist(request):
        return Session.objects.get(session_key=request.session.session_key)
    return create_new_session(request)


def create_new_session(request):
    request.session.create()
    return get_session(request)


def is_admin_url(request):
    try:
        result = resolve(request.path)
        if result.namespace == 'admin':
            return True
    except Resolver404:
        pass
    return False
