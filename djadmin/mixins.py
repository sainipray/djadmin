from django.conf import settings
from django.contrib import admin
from six import with_metaclass

from .models import DjadminModelSetting, DjadminField

LIST_PAGE, FORM_PAGE, = 0, 1


# from reference https://djangosnippets.org/snippets/2887/
def getter_for_related_field(name, admin_order_field=None, short_description=None):
    """
        Create a function that can be attached to a ModelAdmin to use as a list_display field, e.g:
        client__name = getter_for_related_field('client__name', short_description='Client')
    """
    related_names = name.split('__')

    def getter(self, obj):
        for related_name in related_names:
            try:
                obj = getattr(obj, related_name)
            except AttributeError:
                obj = None
        return obj

    getter.admin_order_field = admin_order_field or name
    getter.short_description = short_description or related_names[-1].title().replace('_', ' ')
    return getter


class RelatedFieldAdminMetaclass(type(admin.ModelAdmin)):
    """
        Metaclass used by RelatedFieldAdmin to handle fetching of related field values.
        We have to do this as a metaclass because Django checks that list_display fields are supported by the class.
    """

    # def __new__(cls, name, bases, attrs):
    #     new_class = super(RelatedFieldAdminMetaclass, cls).__new__(cls, name, bases, attrs)
    #     # list_display = ('product_class__id', 'product_class__options', 'product_class__slug',)
    #     for field in new_class.list_display:
    #         if '__' in field:
    #             setattr(new_class, field, getter_for_related_field(field))
    #     return new_class
    pass


class DjadminMixin(with_metaclass(RelatedFieldAdminMetaclass, admin.ModelAdmin)):
    djadmin_change_form_buttons = None
    djadmin_widgets = None
    djadmin_list_display = None
    djadmin_list_display_links = None
    djadmin_list_filter = None
    djadmin_list_select_related = None
    djadmin_list_per_page = None
    djadmin_list_max_show_all = 200
    djadmin_list_editable = None
    djadmin_search_fields = None
    djadmin_date_hierarchy = None

    def is_available(self):
        if hasattr(settings, 'DJADMIN_DYNAMIC_FIELD_DISPLAY'):
            if settings.DJADMIN_DYNAMIC_FIELD_DISPLAY:
                return True
        return False

    def __init__(self, model, admin_site):
        self.model = model
        self.opts = model._meta
        self.admin_site = admin_site
        self.djadmin_list_display = self.list_display
        self.djadmin_list_display_links = self.list_display_links
        self.djadmin_list_filter = self.list_filter
        self.djadmin_list_select_related = self.list_select_related
        self.djadmin_list_per_page = self.list_per_page
        self.djadmin_list_max_show_all = self.list_max_show_all
        self.djadmin_list_editable = self.list_editable
        self.djadmin_search_fields = self.search_fields
        self.djadmin_date_hierarchy = self.date_hierarchy
        super(DjadminMixin, self).__init__(model, admin_site)

    def get_model_object(self, model):
        return DjadminModelSetting.objects.get(model=model)

    def get_djadmin_cards(self, model_obj, type):
        cards = model_obj.djadmincard_set.all()
        cards = cards.filter(location=type)
        return cards

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        if not self.is_available():
            return super(DjadminMixin, self).render_change_form(request, context, add=add, change=change,
                                                                form_url=form_url,
                                                                obj=obj)
        ModelsSetting = self.get_model_object(self.model.__name__)
        context.update({
            'djadmin_card': self.get_djadmin_cards(ModelsSetting, FORM_PAGE)
        })
        return super(DjadminMixin, self).render_change_form(request, context, add=add, change=change, form_url=form_url,
                                                            obj=obj)

    def changelist_view(self, request, extra_context=None):
        if not self.is_available():
            return super(DjadminMixin, self).changelist_view(request, extra_context=extra_context)
        ModelsSetting = self.get_model_object(self.model.__name__)

        # Register all foreignkey field with class
        all_field = DjadminField.objects.filter(model=self.model.__name__)
        for field in all_field:
            field_name = str(field.name)
            if '__' in field_name:
                setattr(self.__class__, field_name, getter_for_related_field(field_name))

        # List Display
        self.list_display = self.djadmin_list_display
        if self.list_display == ('__str__',):
            if len(ModelsSetting.list_display.all()):
                self.list_display = [str(field.name) for field in ModelsSetting.list_display.all()]
            else:
                self.list_display = ('__str__',)

        # List Display Link
        self.list_display_links = self.djadmin_list_display_links
        if not self.list_display_links:
            if len(ModelsSetting.list_display_links.all()):
                self.list_display_links = [field for field in
                                           [field.name for field in ModelsSetting.list_display_links.all()]
                                           if field in self.list_display]
                if not len(self.list_display_links):
                    self.list_display_links = self.list_display[:1]
            else:
                self.list_display_links = self.list_display[:1]

        # List Filter
        self.list_filter = self.djadmin_list_filter
        if not self.list_filter:
            if len(ModelsSetting.list_filter.all()):
                self.list_filter = [field.name for field in ModelsSetting.list_filter.all()]
            else:
                self.list_filter = ()

        self.list_per_page = self.djadmin_list_per_page
        if self.list_per_page == 100:
            self.list_per_page = ModelsSetting.list_per_page
            if not self.list_per_page:
                self.list_per_page = 100

        self.list_max_show_all = self.djadmin_list_max_show_all
        if self.list_max_show_all == 200:
            self.list_max_show_all = ModelsSetting.list_max_show_all
            if not self.list_max_show_all:
                self.list_max_show_all = 200

        self.list_editable = self.djadmin_list_editable
        if not self.list_editable:
            if (len(ModelsSetting.list_editable.all())):
                self.list_editable = [field for field in [field.name for field in ModelsSetting.list_editable.all()] if
                                      field in self.list_display and field not in self.list_display_links]

        self.search_fields = self.djadmin_search_fields
        if not self.search_fields:
            if (len(ModelsSetting.search_fields.all())):
                self.search_fields = [field.name for field in ModelsSetting.search_fields.all()]
            else:
                self.search_fields = ()

        self.date_hierarchy = self.djadmin_date_hierarchy
        if not self.date_hierarchy:
            try:
                self.date_hierarchy = ModelsSetting.date_hierarchy.name
            except Exception as e:
                self.date_hierarchy = None

        self.djadmin_card = self.get_djadmin_cards(ModelsSetting, LIST_PAGE)
        return super(DjadminMixin, self).changelist_view(request, extra_context=extra_context)
