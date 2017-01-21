from distutils.version import StrictVersion as Version

import django
from django.conf import settings
from django.contrib.admin.sites import AdminSite
from django.utils.functional import SimpleLazyObject

from djadmin.colors import colors
from .util import get_user_agent

if Version(django.get_version()) >= Version('1.10.0'):
    from django.utils.deprecation import MiddlewareMixin as object


class DJMiddleware(object):
    # A middleware that adds a "user_agent" object to request
    def process_request(self, request):
        # It is use for find user agent and add in request
        request.user_agent = SimpleLazyObject(lambda: get_user_agent(request))

        ADMIN_HEADER_TITLE = "Django administrator"
        ADMIN_COLOR_THEME = "cyan"
        ALLOW_FORGET_PASSWORD_ADMIN = False
        ADMIN_COLOR_THEME_CODE = "#00bcd4"
        # Add language for django admin
        if hasattr(settings, 'ALLOW_FORGET_PASSWORD_ADMIN'):
            ALLOW_FORGET_PASSWORD_ADMIN = settings.ALLOW_FORGET_PASSWORD_ADMIN

        if hasattr(settings, 'ADMIN_COLOR_THEME'):
            ADMIN_COLOR_THEME = settings.ADMIN_COLOR_THEME
            ADMIN_COLOR_THEME_CODE = colors[ADMIN_COLOR_THEME]["base"]

        if hasattr(settings, 'ADMIN_HEADER_TITLE'):
            ADMIN_HEADER_TITLE = settings.ADMIN_HEADER_TITLE

        AdminSite.site_header = ADMIN_HEADER_TITLE
        request.ADMIN_COLOR_THEME = ADMIN_COLOR_THEME
        request.ALLOW_FORGET_PASSWORD_ADMIN = ALLOW_FORGET_PASSWORD_ADMIN
        request.ADMIN_COLOR_THEME_CODE = ADMIN_COLOR_THEME_CODE
