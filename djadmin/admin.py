# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import Q

from djadmin import settings
from .models import DjadminField, DjadminModelSetting, DjadminCard

User = get_user_model()

LIST_PAGE, FORM_PAGE, = 0, 1


class DjadminCardInline(admin.TabularInline):
    model = DjadminCard


class AdminDjangoModelSettings(admin.ModelAdmin):
    list_display = ('model',)
    inlines = [DjadminCardInline, ]
    fieldsets = (
        (None, {
            'fields': ('model', 'app_label',)
        }),
        ('Basic', {
            'fields': ('list_per_page', 'list_max_show_all',
                       'date_hierarchy', 'actions_on_top', 'actions_on_bottom',)
        }),
        ('Permissions', {
            'fields': ('has_add_permission', 'has_delete_permission', 'has_change_permission',),
        }),
        ('Choices', {
            'fields': ('list_display', 'list_display_links', 'list_filter', 'list_editable', 'search_fields',),
        }),
    )
    filter_horizontal = (
        'list_display', 'list_display_links', 'list_filter', 'list_editable', 'search_fields',)
    readonly_fields = ('model', 'app_label',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    object_data = ""  # Get current form model name

    def get_queryset(self, request):
        register_model = [model.__name__ for model, model_admin in self.admin_site._registry.items()]
        qs = self.model._default_manager.get_queryset()
        qs = qs.filter(model__in=register_model).exclude(model=self.model.__name__)
        return qs

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.object_data = object_id
        return super(AdminDjangoModelSettings, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        model_name = DjadminModelSetting.objects.get(pk=self.object_data)
        kwargs["queryset"] = DjadminField.objects.filter(model=model_name.model)
        if db_field.name == "list_display_links":
            kwargs["queryset"] = model_name.list_display.all()
        if db_field.name == "list_editable":
            exclude_field_ids = model_name.list_display_links.all().values_list("id", flat=True)
            kwargs["queryset"] = model_name.list_display.exclude(Q(id__in=exclude_field_ids) |
                                                                 Q(type__in=['DateTimeField', 'DateField',
                                                                             'TimeField']) | Q(depth__gt=0))
        if db_field.name == "search_fields":
            kwargs["queryset"] = kwargs["queryset"].exclude(
                Q(type__in=['DateTimeField', 'DateField', 'TimeField', 'ForeignKey']) | Q(depth__gt=0))
        return super(AdminDjangoModelSettings, self).formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        model_name = DjadminModelSetting.objects.get(pk=self.object_data)
        kwargs["queryset"] = DjadminField.objects.filter(model=model_name.model)
        if db_field.name == "date_hierarchy":
            kwargs["queryset"] = kwargs["queryset"].filter(type__in=['DateTimeField', 'DateField'])
        return super(AdminDjangoModelSettings, self).formfield_for_foreignkey(db_field, request, **kwargs)


if settings.DJADMIN_DYNAMIC_FIELD_DISPLAY:
    admin.site.register(DjadminModelSetting, AdminDjangoModelSettings)
