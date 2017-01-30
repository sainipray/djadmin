from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _

LIST_PAGE, FORM_PAGE, = 0, 1
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
                                   null=True)
    device_name = models.CharField(max_length=20, null=True)
    device_name_brand = models.CharField(max_length=20, null=True)
    device_name_model = models.CharField(max_length=20, null=True)
    unique_computer_processor = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ['visit_datetime']
        verbose_name = _("visitor")
        verbose_name_plural = _("visitors")

    def __str__(self):
        return self.os_info

    def __unicode__(self):
        return self.os_info


class DjadminField(models.Model):
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
    model = models.CharField(_('Model Name'), max_length=50)
    app_label = models.CharField(_('Model App Label Name'), max_length=50)
    list_display = models.ManyToManyField(DjadminField, verbose_name="List Display", related_name='list_display',
                                          help_text="Set list_display to control which fields are displayed on the change list page of the admin."
                                          , blank=True)
    list_display_links = models.ManyToManyField(DjadminField, verbose_name="List Display Link",
                                                related_name='list_display_links', blank=True,
                                                help_text="Use list_display_links to control if and which fields in list_display should be linked to the change list page for an object.")
    list_filter = models.ManyToManyField(DjadminField, verbose_name="List Filter", related_name='list_filter',
                                         blank=True,
                                         help_text="Set list_filter to activate filters in the right sidebar of the change list page of the admin")
    list_per_page = models.IntegerField(_('List Per Page'), null=True, blank=True,
                                        help_text="Set list_per_page to control how many items appear on each paginated admin change list page.")
    list_max_show_all = models.IntegerField(_('List Max Show All'), null=True, blank=True,
                                            help_text="Set list_max_show_all to control how many items can appear on a 'Show all' admin change list page.")
    list_editable = models.ManyToManyField(DjadminField, verbose_name="List Editable", related_name='list_editable',
                                           blank=True,
                                           help_text="Set list_editable to a list of field names on the model which will allow editing on the change list page.")
    search_fields = models.ManyToManyField(DjadminField, verbose_name="Search Fields", related_name='search_fields',
                                           blank=True,
                                           help_text="Set search_fields to enable a search box on the admin change list page.")
    date_hierarchy = models.ForeignKey(DjadminField, related_name='date_hierarchy', blank=True, null=True,
                                       help_text="Set date_hierarchy to the name of a DateField or DateTimeField in your model, and the change list page will include a date-based drilldown navigation by that field.")

    class Meta:
        db_table = 'djadmin_model_setting'
        ordering = ['model']
        verbose_name = _('Djadmin Model Setting')
        verbose_name_plural = _('Djadmin Model Settings')

    def __unicode__(self):
        return self.model


class DjadminCard(models.Model):
    LOCATION_CHOICES = (
        (LIST_PAGE, 'LIST PAGE'),
        (FORM_PAGE, 'FORM PAGE'),
    )
    model = models.ForeignKey(DjadminModelSetting)
    name = models.CharField(_('Name of Card'), max_length=255)
    html = models.TextField(_('HTML Code'))
    location = models.SmallIntegerField(_('Select Location'), choices=LOCATION_CHOICES,
                                        help_text='It will help to show this card on selected location for this model')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_created']
        verbose_name = _('Djadmin Card')
        verbose_name_plural = _('Djadmin Cards')

    def __str__(self):
        return self.name
