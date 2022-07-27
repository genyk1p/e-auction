from django import forms
from django.forms import ModelForm
from .models import Review, ProjectSettings
from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['review_text', 'rating']
        labels = {'review_text': _('Please write your review'), 'rating': _('Select rating')}


class BidOrderFormS(forms.Form):
    time_prefix = ProjectSettings.objects.get(pk=1).time_prefix
    # time_prefix='CCC'
    var1 = _('Specify the start time of the order ')
    var2 = str(time_prefix)
    var3 = _(', write a colon separated for example 21:00 (21-00 or 21.00 will not work!)')
    total_rub = forms.DecimalField(label=_('Price:'),
                                   help_text=_('Indicate the price in rubles according to which you are ready to fulfill the order'))
    schedule_value1_date = forms.DateTimeField(
        label=_('Order start date'),
        help_text=_('Indicate the start date of the order, for example, if the order is a raid that you do on schedule, then indicate all the possible options for this raid, a maximum of 4 dates can be specified'),
        widget=forms.SelectDateWidget()
    )
    schedule_value1_time = forms.TimeField(
        label=format_lazy('{var1} {var2} {var3}', var1=var1, var2=var2, var3=var3),
        help_text=_('Specify the start time of order execution CET / CEST (Central European time, winter / summer, respectively). Differs from "MSK" by +2 hours winter and +1 hour summer)'),
        widget=forms.TimeInput(format='%H:%M')
    )
    schedule_value2_date = forms.DateTimeField(
        label=_('Specify a second start date for the product if needed'),
        widget=forms.SelectDateWidget()
    )
    schedule_value2_time = forms.TimeField(
        label=_('Specify the second start time of the order'),
        widget=forms.TimeInput(format='%H:%M'),
        required=False
    )
    schedule_value3_date = forms.DateTimeField(
        label=_('Specify a third product start date, if needed'),
        widget=forms.SelectDateWidget()
    )
    schedule_value3_time = forms.TimeField(
        label=_('Specify the third start time of the order'),
        widget=forms.TimeInput(format='%H:%M'),
        required=False
    )
    schedule_value4_date = forms.DateTimeField(
        label=_('Specify a fourth product start date if needed'),
        widget=forms.SelectDateWidget()
    )
    schedule_value4_time = forms.TimeField(
        label=_('Specify the fourth start time of the order'),
        widget=forms.TimeInput(format='%H:%M'),
        required=False
    )


class BidOrderForm(forms.Form):
    total_rub = forms.DecimalField(
        label=_('Price:'),
        help_text=_('Indicate the price in rubles according to which you are ready to fulfill the order')
    )

