from distutils.version import StrictVersion as Version

import django
from django.conf import settings
from django.contrib.admin.sites import AdminSite
from django.utils.functional import SimpleLazyObject

from .colors import colors
from .models import DjadminModelSetting
from .signals import get_register_model_with_mixin, handle_djadmin_field_data
from .util import get_user_agent

if Version(django.get_version()) >= Version('1.10.0'):
    from django.utils.deprecation import MiddlewareMixin as object


class DJMiddleware(object):
    def process_request(self, request):
        request.user_agent = SimpleLazyObject(lambda: get_user_agent(request))

        ALLOW_FORGET_PASSWORD_ADMIN = getattr(settings, 'ALLOW_FORGET_PASSWORD_ADMIN', False)
        ADMIN_COLOR_THEME = getattr(settings, 'ADMIN_COLOR_THEME', 'cyan').lower()
        ADMIN_HEADER_TITLE = getattr(settings, 'ADMIN_HEADER_TITLE', 'Django administrator')
        ADMIN_COLOR_THEME_CODE = colors[ADMIN_COLOR_THEME]["base"]
        AdminSite.site_header = ADMIN_HEADER_TITLE
        request.ADMIN_COLOR_THEME = ADMIN_COLOR_THEME
        request.ALLOW_FORGET_PASSWORD_ADMIN = ALLOW_FORGET_PASSWORD_ADMIN
        request.ADMIN_COLOR_THEME_CODE = ADMIN_COLOR_THEME_CODE
        if request.user.is_superuser and getattr(settings, 'DJADMIN_DYNAMIC_FIELD_DISPLAY', False):
            register_model_list = get_register_model_with_mixin()
            exist_model_list = DjadminModelSetting.objects.all()
            if len(register_model_list) > len(exist_model_list):
                handle_djadmin_field_data(register_model_list, True)  # True = Create
            elif len(register_model_list) < len(exist_model_list):
                handle_djadmin_field_data(register_model_list, False)  # False = Delete
