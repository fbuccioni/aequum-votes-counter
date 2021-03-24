"""
django-votes_counter.rst: App admin example, this file must have the name of the app
"""
from django.contrib import admin
from django.utils.safestring import mark_safe
from ..votes_counter import models


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

