# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models.signals import post_migrate


def DjadminModelSettings(sender, **kwargs):
    from .signals import handle_djadmin_field_data, get_register_model_with_mixin
    register_model_list = get_register_model_with_mixin()
    handle_djadmin_field_data(register_model_list, True)


class ActivityAppConfig(AppConfig):
    name = 'djadmin'

    def ready(self):
        import djadmin.signals
        from djadmin import settings
        if settings.DJADMIN_DYNAMIC_FIELD_DISPLAY:
            post_migrate.connect(DjadminModelSettings, sender=self)
