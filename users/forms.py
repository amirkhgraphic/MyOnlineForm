from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserSignUpForm(UserCreationForm):
    apply_for_ta = forms.BooleanField(label='می‌خواهم به عنوان دستیار آموزشی (TA) ثبت‌نام کنم', required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'student_id',
            'email',
            'phone',
            'password1',
            'password2',
            'apply_for_ta',
        ]
        labels = {
            'username': 'نام کاربری',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'student_id': 'کد دانشجویی',
            'email': 'ایمیل',
            'phone': 'تلفن',
            'password1': 'گذرواژه',
            'password2': 'تایید گذرواژه',
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'student_id',
            'email',
            'phone',
        ]
        labels = {
            'username': 'نام کاربری',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'student_id': 'کد دانشجویی',
            'email': 'ایمیل',
            'phone': 'تلفن',
        }
