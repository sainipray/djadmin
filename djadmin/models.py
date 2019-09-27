# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.db import models
from django.db.models import Count
from django.db.models import When, Case
from django.utils.translation import ugettext_lazy as _,ugettext

from djadmin import settings

LIST_PAGE, FORM_PAGE, = 0, 1
AUTH_USER_MODEL = settings.AUTH_USER_MODEL


class Visitor(models.Model):
    """
    It will store information about user when logged in using django admin
    """
    name = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_('User'), null=True, on_delete=models.CASCADE)
    city = models.CharField(_('City'), max_length=255, null=True)
    state = models.CharField(_('State'), max_length=50, null=True)
    country = models.CharField(_('Country'), max_length=50, null=True)
    visit_datetime = models.DateTimeField(_('Login Date Time'), auto_now=True)
    browser = models.CharField(_('Browser'), max_length=30, null=True)
    browser_version = models.CharField(_('Browser Version'), max_length=20, null=True)
    ipaddress = models.CharField(_('IP Address'), max_length=20, null=True)
    os_info = models.CharField(_('OS Information'), max_length=30, null=True)
    os_info_version = models.CharField(_('OS Version'), max_length=20, null=True)
    device_type = models.CharField(_('Device Type'), max_length=20,
                                   null=True)
    device_name = models.CharField(_('Device Name'), max_length=20, null=True)
    device_name_brand = models.CharField(_('Device Brand Name'), max_length=20, null=True)
    device_name_model = models.CharField(_('Device Model Name'), max_length=20, null=True)
    unique_computer_processor = models.CharField(_('Computer Processor'), max_length=255, null=True)
    session = models.ForeignKey(Session, verbose_name=_('Session'), null=True, blank=True, on_delete=models.SET_NULL)
    latitude = models.DecimalField(_('Latitude'), max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(_('Longitude'), max_digits=9, decimal_places=6, null=True)
    http_referer = models.URLField(_('HTTP_REFERER URL'), null=True, blank=True)
    request_url = models.URLField(_('Request URL'), null=True)

    class Meta:
        ordering = ['visit_datetime']
        verbose_name = _("visitor")
        verbose_name_plural = _("visitors")

    def __str__(self):
        return self.os_info

    @staticmethod
    def get_visitors(field_name):
        """
        It will provide distinct field value's according to any given field and
         also provide count of repeat value of field.
        :param field_name:
        :return:
        """
        return Visitor.objects.values(field_name).annotate(count=Count('id')).order_by(field_name)


class DjadminField(models.Model):
    """
    It will store field's related information about admin registered
     model that inherit 'DjadminMixin' class.
    """
    name = models.CharField(_('Field Name'), max_length=255)
    type = models.CharField(_('Field Type'), max_length=30)
    model = models.CharField(_('Model Name'), max_length=50)
    depth = models.IntegerField(_('Field Depth'))
    foreignkey_model = models.CharField(_('Foreign Key Model Name'), max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'djadmin_field'
        verbose_name = _('Djadmin Field')
        verbose_name_plural = _('Djadmin Fields')

    def __str__(self):
        return self.name


class DjadminModelSetting(models.Model):
    """
    It will store Model information that inherit 'DjadminMixin' class
    This model entry work dynamically. When any admin registerd model inherit mentions class
    then this model automatic store information about model's.
    Note: When you remove inherit class from admin model then model stored entry will be deleted automatically
    """
    model = models.CharField(_('Model Name'), max_length=50)
    app_label = models.CharField(_('Model App Label Name'), max_length=50)
    list_display = models.ManyToManyField(DjadminField,
                                          verbose_name=_("List Display"),
                                          related_name='list_display',
                                          help_text=_("Set list_display to control which fields are displayed "
                                                      "on the change list page of the admin."),
                                          blank=True)
    list_display_links = models.ManyToManyField(DjadminField,
                                                verbose_name=_("List Display Link"),
                                                related_name='list_display_links',
                                                blank=True,
                                                help_text=_("Use list_display_links to control if and which fields "
                                                            "in list_display should be linked to the change"
                                                            " list page for an object."))
    list_filter = models.ManyToManyField(DjadminField,
                                         verbose_name=_("List Filter"),
                                         related_name='list_filter',
                                         blank=True,
                                         help_text=_("Set list_filter to activate filters in the right sidebar of"
                                                     " the change list page of the admin"))
    list_per_page = models.IntegerField(_('List Per Page'),
                                        null=True,
                                        blank=True,
                                        help_text=_("Set list_per_page to control how many items appear on each"
                                                    " paginated admin change list page."))
    list_max_show_all = models.IntegerField(_('List Max Show All'),
                                            null=True,
                                            blank=True,
                                            help_text=_("Set list_max_show_all to control how many items can "
                                                        "appear on a 'Show all' admin change list page."))
    list_editable = models.ManyToManyField(DjadminField,
                                           verbose_name=_("List Editable"),
                                           related_name='list_editable',
                                           blank=True,
                                           help_text=_("Set list_editable to a list of field names on the model"
                                                       " which will allow editing on the change list page."))
    search_fields = models.ManyToManyField(DjadminField,
                                           verbose_name=_("Search Fields"),
                                           related_name='search_fields',
                                           blank=True,
                                           help_text=_("Set search_fields to enable a search box on the admin"
                                                       " change list page."))
    date_hierarchy = models.ForeignKey(DjadminField,
                                       related_name='date_hierarchy',
                                       blank=True,
                                       null=True,
                                       verbose_name=_('Date Hierarchy'),
                                       help_text=_("Set date_hierarchy to the name of a DateField or DateTimeField"
                                                   " in your model, and the change list page will include a date-based"
                                                   " drilldown navigation by that field."),on_delete=models.CASCADE)

    actions_on_top = models.BooleanField(_('Actions on Top'),
                                         default=True,
                                         help_text=_('Controls where on the page the actions bar appears'))
    actions_on_bottom = models.BooleanField(_('Actions on Bottom'),
                                            default=False)

    has_add_permission = models.BooleanField(_('Has Add Permission?'), default=True)
    has_change_permission = models.BooleanField(_('Has Change Permission?'), default=True)
    has_delete_permission = models.BooleanField(_('Has Delete Permission?'), default=True)

    # 2) Show all inline form list with manytomany of particular model

    # 3)number of forms in inline
    # extra max_num min_num

    class Meta:
        db_table = 'djadmin_model_setting'
        ordering = ['model']
        verbose_name = _('Djadmin Model Setting')
        verbose_name_plural = _('Djadmin Model Settings')

    def __unicode__(self):
        return self.model


class DjadminCard(models.Model):
    LOCATION_CHOICES = (
        (LIST_PAGE, _('LIST PAGE')),
        (FORM_PAGE, _('FORM PAGE')),
    )
    model = models.ForeignKey(DjadminModelSetting, on_delete=models.CASCADE)
    name = models.CharField(_('Name of Card'), max_length=255)
    html = models.TextField(_('HTML Code'))
    location = models.SmallIntegerField(_('Select Location'),
                                        choices=LOCATION_CHOICES,
                                        help_text=_('It will help to show this card on selected '
                                                    'location for this model'))
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_created']
        verbose_name = _('Djadmin Card')
        verbose_name_plural = _('Djadmin Cards')

    def __str__(self):
        return self.name


class Sortable(models.Model):
    """
    It will store django admin changelist page row's pk.
    But It will store when admin change any row, Otherwise it will not store default changelist
    row's pk. It also provide reset to sortable from icon in table head tag.
    """
    model = models.ForeignKey(ContentType, verbose_name=_('Model'), on_delete=models.CASCADE)
    sort_array = models.TextField(_('Model Sortable Array'))

    class Meta:
        verbose_name = _('Sortable Model')
        verbose_name_plural = _('Sortable Models')

    def __str__(self):
        return self.model.model

    @property
    def get_list(self):
        """
        It will convert string list to int list
        ['1', '2', '3'] -> [1, 2, 3]
        :return list:
        """
        model_id_list = []
        for model_id in json.loads(self.sort_array):
            model_id_list.append(int(model_id))
        return model_id_list

    @staticmethod
    def get_sortable_row(model, queryset):
        """
        It will sort queryset(admin registered models) according to django admin changelist page.
        :param model:
        :param queryset:
        :return queryset:
        """
        model = ContentType.objects.get(model=model)
        try:
            sort_model = Sortable.objects.get(model=model)
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(sort_model.get_list)])
            queryset = queryset.order_by(preserved)
        except Sortable.DoesNotExist:
            pass
        return queryset
