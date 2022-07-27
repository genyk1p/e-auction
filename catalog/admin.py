from django.contrib import admin
from .models import *
from modeltranslation.admin import TabbedTranslationAdmin
import os
from django import forms

is_hidden = os.environ.get('is_hidden')
if is_hidden is None:
    is_hidden = False

# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('id', 'admin_name', 'price')
#     list_display_links = ('id', 'admin_name')
#     search_fields = ('id', 'name','admin_name')


class OptionSelectElementAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


#
class OptionCheckBoxElementAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'total', 'user_buyer', 'user_driver', 'product', 'formed_data')
    search_fields = ('user_buyer', 'user_driver', 'product')
    list_display_links = ('status', 'total', 'product')


class MaximumTradingTimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'max_time')
    list_display_links = ('id', 'max_time')
    search_fields = ('id', 'max_time')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'rating', 'user_buyer', 'user_driver', 'review_status')
    list_display_links = ('id', 'rating', 'user_buyer', 'user_driver', 'review_status')
    search_fields = ('order', 'user_buyer', 'user_driver')


class OptionSelectFirstSummaryAdmin(admin.ModelAdmin):
    list_display = ('id',  '__str__')
    list_display_links = ('id', '__str__')
    search_fields = ('option_select__admin_name',)


class OptionSelectSecondSummaryAdmin(admin.ModelAdmin):
    list_display = ('id',  '__str__')
    list_display_links = ('id', '__str__')
    search_fields = ('option_select__admin_name',)

class OptionSelect3SummaryAdmin(admin.ModelAdmin):
    list_display = ('id',  '__str__')
    list_display_links = ('id', '__str__')
    search_fields = ('option_select__admin_name',)


class OptionSelectPercentSummaryAdmin(admin.ModelAdmin):
    list_display = ('id',  '__str__')
    list_display_links = ('id', '__str__')
    search_fields = ('option_select__admin_name',)


class OptionCheckBoxFirstSummaryAdmin(admin.ModelAdmin):
    list_display = ('id',  '__str__')
    list_display_links = ('id', '__str__')
    search_fields = ('option_check_box__admin_name',)


class OptionCheckBoxSecondSummaryAdmin(admin.ModelAdmin):
    list_display = ('id',  '__str__')
    list_display_links = ('id', '__str__')
    search_fields = ('option_check_box__admin_name',)

class DriverAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_driver', 'number_done_orders', 'rating', 'can_do_piloted', 'driver_rank', 'skype', 'telegram')
    list_display_links = ('id', 'user_driver')
    search_fields = ('user_driver__username',)


class LabelTextAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

    def get_queryset(self, request):
        qs = super(LabelTextAdmin, self).get_queryset(request)
        return qs.filter(is_hidden=is_hidden)


# Этот клас необходим на для того чтобы отфильтровать значения передаваемые в LabelTextChoiceField в Product
class LabelTextChoiceField(forms.ModelChoiceField):
    pass


class ProductAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'admin_name', 'price')
    list_display_links = ('id', 'admin_name')
    search_fields = ('id', 'name', 'admin_name')
    group_fieldsets = True

    # Так как продукт в дальнейшем возможно надо будет удалить, а из базы данных его удалять нельзя, используется эта
    # конструкция, которая скрывает поля у которых is_hidden == True, также можно поменять поведение админки и
    # отобразить скрытые продукты указав в переменных среды в хероку show_hidden == True
    def get_queryset(self, request):
        qs = super(ProductAdmin, self).get_queryset(request)
        return qs.filter(is_hidden=is_hidden)

    # Эта конструкция позволяет передать в виджет селект выбора нужного нам лейбел текста, только значения у которых
    # параметер is_hidden установлен в положение False
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'first_label_name' or db_field.name == 'second_label_name' or db_field.name == 'third_label_name' or db_field.name == 'fourth_label_name' or db_field.name == 'fifth_label_name':
            return LabelTextChoiceField(LabelText.objects.filter(is_hidden=is_hidden), required=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ProjectSettings)
admin.site.register(OptionSelectFirst)
admin.site.register(MaxTime)
admin.site.register(OptionSelectSecond)
admin.site.register(OptionSelectPercent)
admin.site.register(OptionSelect3)
admin.site.register(OptionCheckBoxFirst)
admin.site.register(OptionCheckBoxSecond)
admin.site.register(OptionSelectElement, OptionSelectElementAdmin)
admin.site.register(OptionCheckBoxElement, OptionCheckBoxElementAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category)
admin.site.register(Game)
admin.site.register(BidedOrder)
admin.site.register(Payment_system_settings)
admin.site.register(Driver, DriverAdmin)
admin.site.register(OptionSelectFirstSummary, OptionSelectFirstSummaryAdmin)
admin.site.register(OptionSelectSecondSummary, OptionSelectSecondSummaryAdmin)
admin.site.register(OptionCheckBoxFirstSummary, OptionCheckBoxFirstSummaryAdmin)
admin.site.register(OptionCheckBoxSecondSummary, OptionCheckBoxSecondSummaryAdmin)
admin.site.register(OptionSelectPercentSummary, OptionSelectPercentSummaryAdmin)
admin.site.register(OptionSelect3Summary, OptionSelect3SummaryAdmin)
admin.site.register(LabelText, LabelTextAdmin)

