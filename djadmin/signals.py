# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

import geocoder
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.db.models import ForeignKey

from djadmin import settings
from .mixins import DjadminMixin
from .models import DjadminField, DjadminModelSetting
from .models import Visitor
from .util import calculate_action_field_list, get_session

User = get_user_model()


def add_visitor(request, user=None):
    if request.user_agent.is_mobile:
        device_type = "Mobile"
    elif request.user_agent.is_tablet:
        device_type = "Tablet"
    elif request.user_agent.is_touch_capable:
        device_type = "Touch"
    elif request.user_agent.is_pc:
        device_type = "PC"
    elif request.user_agent.is_bot:
        device_type = "Bot"
    else:
        device_type = "Unknown"
    browser = request.user_agent.browser.family
    browser_version = request.user_agent.browser.version_string
    os_info = request.user_agent.os.family
    os_info_version = request.user_agent.os.version_string
    device_name = request.user_agent.device.family
    device_name_brand = request.user_agent.device.brand
    device_name_model = request.user_agent.device.model
    ipaddress = request.META.get("HTTP_X_FORWARDED_FOR", None)
    http_referer = request.META.get("HTTP_REFERER", None)
    request_url = request.build_absolute_uri()
    if ipaddress:
        ipaddress = ipaddress.split(", ")[0]
    else:
        ipaddress = request.META.get("REMOTE_ADDR", "")
    session = get_session(request)
    city = None
    state = None
    country = None
    latitude = None
    longitude = None
    if request.method == 'POST':
        try:
            if not request.POST.get('latitude', '') == '':
                latitude = request.POST.get('latitude', None)
                longitude = request.POST.get('longitude', None)
                g = geocoder.google([latitude, longitude], method='reverse')
                city = g.city
                state = g.state_long
                country = g.country_long
        except Exception as e:
            pass
    unique_computer = request.META.get("PROCESSOR_IDENTIFIER", None)
    Visitor.objects.create(device_type=device_type, name=user, ipaddress=ipaddress, browser=browser,
                           browser_version=browser_version, os_info_version=os_info_version,
                           os_info=os_info, http_referer=http_referer, request_url=request_url,
                           device_name=device_name, city=city, state=state, country=country,
                           device_name_brand=device_name_brand, device_name_model=device_name_model,
                           unique_computer_processor=unique_computer,session=session, latitude=latitude, longitude=longitude)


def visitor(sender, user, request, **kwargs):
    if hasattr(request, 'user') and (not request.user.is_superuser or settings.ALLOW_STAFF_USER_AS_VISITOR):
        add_visitor(request, user)


user_logged_in.connect(visitor, sender=User, dispatch_uid="visitor")


def get_register_model_with_mixin():
    djadmin_mixin_inherit_classes = DjadminMixin.__subclasses__()
    djadmin_mixin_model = []
    for model, model_admin in admin.site._registry.items():
        if model_admin.__class__ in djadmin_mixin_inherit_classes or model_admin.__class__.__name__ == DjadminMixin.__name__:
            djadmin_mixin_model.append(model)
    return djadmin_mixin_model


def create_inner_field(main_field, depth, root_model, extra='', previous_model=None):
    if hasattr(main_field.related_model,
               '_meta') and main_field.related_model != root_model and main_field.related_model != previous_model:
        fields = main_field.related_model._meta.fields
        DjadminField.objects.create(name='{0}{1}'.format(extra, main_field.name),
                                    model=root_model.__name__,
                                    type=main_field.__class__.__name__,
                                    depth=depth,
                                    foreignkey_model=main_field.rel.to.__name__)
        if depth < settings.DJADMIN_FIELD_DEPTH:
            depth += 1
            for field in fields:
                if isinstance(field, ForeignKey):
                    create_inner_field(field, depth, root_model,
                                       extra="{0}{1}__".format(extra, main_field.name),
                                       previous_model=main_field.related_model)
                else:
                    field_name = extra + main_field.name + "__{0}".format(field.name)
                    DjadminField.objects.create(name=field_name,
                                                model=root_model.__name__,
                                                type=field.__class__.__name__,
                                                depth=depth,
                                                foreignkey_model=main_field.rel.to.__name__)

    else:
        foreignkey_model = None
        if isinstance(main_field, ForeignKey):
            foreignkey_model = main_field.rel.to.__name__
        DjadminField.objects.create(name='{0}{1}'.format(extra, main_field.name),
                                    model=root_model.__name__,
                                    type=main_field.__class__.__name__,
                                    depth=depth,
                                    foreignkey_model=foreignkey_model)


def handle_djadmin_field_data(djadmin_mixin_model, action):
    models = []
    for model in djadmin_mixin_model:
        if action:
            sys.stdout.write("  Applying {0} model".format(model.__name__))
            exist_fields = DjadminField.objects.filter(model=model.__name__)
            define_fields = model._meta.fields  # + model._meta.many_to_many
            delete_fields = calculate_action_field_list(exist_fields, define_fields, True)
            for delete_field in delete_fields:
                sys.stdout.write(".")
                delete_field.delete()
            exist_fields = DjadminField.objects.filter(model=model.__name__)
            create_fields = calculate_action_field_list(define_fields, exist_fields, False)
            for create_field in create_fields:
                sys.stdout.write(".")
                depth = 0
                create_inner_field(create_field, depth, model)
            sys.stdout.write(" OK\n")
            DjadminModelSetting.objects.get_or_create(model=model.__name__, app_label=model._meta.app_label)
        else:
            models.append(model.__name__)
    if models:
        delete_models = DjadminModelSetting.objects.exclude(model__in=models)
        for model in delete_models:
            sys.stdout.write("  Deleting {0} model".format(model.model))
            exist_fields = DjadminField.objects.filter(model=model.model)
            exist_fields.delete()
            model.delete()
            sys.stdout.write(" OK\n")
