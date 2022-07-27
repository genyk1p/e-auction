from django.contrib import admin
from information.models import Information
from modeltranslation.admin import TabbedTranslationAdmin


class InformationAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    group_fieldsets = True


admin.site.register(Information, InformationAdmin)
