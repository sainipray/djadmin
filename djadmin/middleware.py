# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django
from django.contrib.admin.sites import AdminSite
from django.utils.functional import SimpleLazyObject

from djadmin import settings
from .models import DjadminModelSetting
from .signals import get_register_model_with_mixin, handle_djadmin_field_data
from .util import get_user_agent, get_admin_color_theme, get_admin_color_theme_hex_code

if django.VERSION >= (1, 10):
    from django.utils.deprecation import MiddlewareMixin
else:
    MiddlewareMixin = object


class DJMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user_agent = SimpleLazyObject(lambda: get_user_agent(request))
        admin_color_theme = settings.ADMIN_COLOR_THEME
        ADMIN_COLOR_THEME = get_admin_color_theme(admin_color_theme)
        ADMIN_COLOR_THEME_CODE = get_admin_color_theme_hex_code(admin_color_theme)
        ALLOW_FORGET_PASSWORD_ADMIN = settings.ALLOW_FORGET_PASSWORD_ADMIN
        AdminSite.site_header = settings.ADMIN_HEADER_TITLE
        request.ADMIN_COLOR_THEME = ADMIN_COLOR_THEME
        request.ALLOW_FORGET_PASSWORD_ADMIN = ALLOW_FORGET_PASSWORD_ADMIN
        request.ADMIN_COLOR_THEME_CODE = ADMIN_COLOR_THEME_CODE
        if request.user.is_superuser and settings.DJADMIN_DYNAMIC_FIELD_DISPLAY:
            register_model_object_list = get_register_model_with_mixin()
            exist_model_object_list = DjadminModelSetting.objects.all()
            register_model_list = [model.__name__ for model in register_model_object_list]
            exist_model_list = [str(model.model) for model in exist_model_object_list]
            create_model_name = [model for model in register_model_list if model not in exist_model_list]
            delete_model_name = [model for model in exist_model_list if model not in register_model_list]
            if len(create_model_name):
                handle_djadmin_field_data(register_model_object_list, True)
            if len(delete_model_name):
                if settings.DJADMIN_DYNAMIC_DELETE_UNREGISTER_FIELD:
                    handle_djadmin_field_data(register_model_object_list, False)
