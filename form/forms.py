from django import forms
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from .models import Form, TimeSlot


class FormCreateForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = [
            'name',
            'course_name',
            'professor_name',
            'year',
            'semester',
            'valid_student_ids',
        ]
        widgets = {
            'valid_student_ids': forms.TextInput(attrs={
                'placeholder': _('شماره‌های دانشجویی مجاز جهت رزرو تایم را وارد کنید'),
                'class': 'form-control tagify-input',
                'data-tagify': 'true',
            }),
        }
        labels = {
            'name': 'نام فرم',
            'course_name': 'درس',
            'professor_name': 'استاد',
            'year': 'سال تحصیلی',
            'semester': 'ترم جاری',
            'valid_student_ids': 'شماره های دانشجویی مجاز',
        }

    def clean_valid_student_ids(self):
        valid_ids = self.cleaned_data['valid_student_ids']
        return list(map(lambda x: str(x['value']), valid_ids)) if valid_ids else []


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

    def clean_datetime(self):
        selected_datetime = self.cleaned_data.get('datetime')
        if selected_datetime < now():
            raise forms.ValidationError(_('زمان انتخاب شده شما گذشته است.'))
        return selected_datetime


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
