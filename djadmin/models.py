from django.conf import settings
from django.db import models

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Visitor(models.Model):
    name = models.ForeignKey(AUTH_USER_MODEL, null=True)
    city = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    visit_datetime = models.DateTimeField(auto_now=True)
    browser = models.CharField(max_length=30, null=True)
    browser_version = models.CharField(max_length=20, null=True)
    ipaddress = models.CharField(max_length=20, null=True)
    os_info = models.CharField(max_length=30, null=True)
    os_info_version = models.CharField(max_length=20, null=True)
    device_type = models.CharField(max_length=20,
                                   null=True)  # TODO: It store visitor user device type like is_mobile,is_pc
    device_name = models.CharField(max_length=20, null=True)  # TODO: It store visitor device family name
    device_name_brand = models.CharField(max_length=20, null=True)  # TODO: It store visitor device family name
    device_name_model = models.CharField(max_length=20, null=True)  # TODO: It store visitor device family name
    unique_computer_processor = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ['visit_datetime']
        verbose_name = "visitor"
        verbose_name_plural = "visitors"

    def __str__(self):
        return self.os_info

    def __unicode__(self):
        return self.os_info
