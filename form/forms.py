from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Form, TimeSlot


class FormCreateForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['name', 'valid_student_ids']
        widgets = {
            'valid_student_ids': forms.TextInput(attrs={
                'placeholder': _('Enter student IDs'),
                'class': 'form-control tagify-input',
                'data-tagify': 'true',
            }),
        }


class TimeSlotCreateForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['datetime']
        widgets = {
            'datetime': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
        }
        labels = {
            'datetime': _('تاریخ و زمان'),
        }


class TimeSlotsCreateForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label=_('تاریخ شروع'),
        help_text=_('تاریخ شروع به میلادی'),
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label=_('زمان شروع'),
        help_text=_('ساعت شروع به وقت Asia/Tehran'),
    )
    slot_count = forms.IntegerField(
        min_value=1,
        label=_('تعداد'),
        help_text=_("تعداد نوبت‌های مورد نیاز"),
    )
    duration = forms.IntegerField(
        min_value=1,
        label=_('مدت‌زمان'),
        help_text=_("مدت‌زمان هر نوبت (به دقیقه)"),
    )
    breaktime = forms.IntegerField(
        initial=0,
        min_value=0,
        label=_('زمان استراحت'),
        help_text=_("زمان استراحت بین هر نوبت (به دقیقه)"),
    )
