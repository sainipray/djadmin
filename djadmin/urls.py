# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views

from djadmin import settings
from .views import configuration, install_library, model_sortable

admin_url = [
    url(r'^model/(?P<model_name>[\w\-]+)/sortable/(?P<type>update|reset)/$', model_sortable, name="djadmin_sortable"),
    url(r'^', admin.site.urls, ),
]
djadmin_config_page = []
if settings.DJADMIN_CONFIG_PAGE:
    djadmin_config_page = [
        url(r'^config/', configuration, name='djadmin_config_page'),
        url(r'^install_lib/', install_library, name='djadmin_install_library'),
    ]
forget_password_url = []
if settings.ALLOW_FORGET_PASSWORD_ADMIN:
    forget_password_url = [
        url(r'^password_reset/$', views.PasswordResetView.as_view(), name='password_reset'),
        url(r'^password_reset/done/$', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
        url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
        url(r'^reset/done/$', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    ]

urlpatterns = admin_url + forget_password_url + djadmin_config_page
