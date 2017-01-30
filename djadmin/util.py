import sys
from hashlib import md5

from django.core.cache import cache
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.executor import MigrationExecutor
from django.db.models import ForeignKey
from django.db.models import Q
from user_agents import parse

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


def remaining_migrations():
    connection = connections[DEFAULT_DB_ALIAS]
    connection.prepare_database()
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    return executor.migration_plan(targets)


def calculate_action_field_list(first_list, second_list, Order_Type):
    field_name = None
    field_type = None
    data = []
    for first_field in first_list:
        for second_field in second_list:
            if first_field.name == second_field.name:
                field_name = True
                if Order_Type:
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
            if Order_Type:
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
            if Order_Type:
                DjadminField.objects.filter(
                    Q(name__endswith="__{0}".format(first_field.name), foreignkey_model__exact=first_field.model) |
                    Q(name__exact=first_field.name, model__exact=first_field.model)).update(
                    type=second_field.__class__.__name__)
    return data
