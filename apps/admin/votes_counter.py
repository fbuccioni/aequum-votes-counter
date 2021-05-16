"""
django-votes_counter.rst: App admin example, this file must have the name of the app
"""
from django.contrib import admin
from django.core.exceptions import ValidationError
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as gettext

from ..votes_counter import models


UserAdmin.ignore_auto = True


class InlinePollingPlace(admin.TabularInline):
    model = models.PollingPlace
    extra = 1


class Comuna(admin.ModelAdmin):
    inlines = (InlinePollingPlace,)


class InlinePollingPlaceTable(admin.TabularInline):
    model = models.PollingPlaceTable
    extra = 1


class PollingPlace(admin.ModelAdmin):
    inlines = (InlinePollingPlaceTable,)


class InlineVotes(admin.TabularInline):
    model = models.Votes
    readonly_fields = ('candidate',)
    exclude = ('polling_place_tables',)
    extra = 0
    max_num = 0
    fields = ('candidate', 'count')
    can_delete = False
    empty_value_display = gettext("Total")
    ordering = ('candidate__user__first_name', 'candidate__user__last_name')


class PollingPlaceTable(admin.ModelAdmin):
    inlines = (InlineVotes,)


class ProfileInline(admin.StackedInline):
    model = models.UserCandidate
    can_delete = False
    verbose_name_plural = gettext("Candidate")
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    ignore_auto = True
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


class List(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = list_display
