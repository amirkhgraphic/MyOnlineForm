from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(max_length=30, help_text=_('نام'))
    last_name = models.CharField(max_length=30, help_text=_('نام خانوادگی'))
    student_id = models.CharField(max_length=15, help_text=_('کد دانشچویی'), blank=True, null=True)
    email = models.EmailField(unique=True, help_text=_('آدرس ایمیل'))
    phone = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message=_('Phone number must start with 09 and be exactly 11 digits.')
            ),
        ],
        blank=True,
        null=True,
        help_text=_('شماره تماس'),
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text=_('تاریخ ساخت'))
    is_active = models.BooleanField(default=True, help_text=_('فعال بودن'))
    is_admin = models.BooleanField(default=False, help_text=_('ادمین بودن'))

    def __str__(self):
        return self.username
