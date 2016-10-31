from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views

admin_url = [
    url(r'^', admin.site.urls, ),
]
forget_password_url = []
if hasattr(settings, 'ALLOW_FORGET_PASSWORD_ADMIN'):
    if settings.ALLOW_FORGET_PASSWORD_ADMIN:
        forget_password_url = [
            url(r'^password_reset/$', views.password_reset, name='password_reset'),
            url(r'^password_reset/done/$', views.password_reset_done, name='password_reset_done'),
            url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                views.password_reset_confirm, name='password_reset_confirm'),
            url(r'^reset/done/$', views.password_reset_complete, name='password_reset_complete'),
        ]

urlpatterns = admin_url + forget_password_url
