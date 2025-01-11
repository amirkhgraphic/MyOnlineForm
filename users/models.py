from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(max_length=30, help_text=_('first name'))
    last_name = models.CharField(max_length=30, help_text=_('last name'))
    email = models.EmailField(unique=True, help_text=_('email address'))
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
        help_text=_('number'),
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text=_('creation date'))
    is_active = models.BooleanField(default=True, help_text=_('is active'))
    is_admin = models.BooleanField(default=False, help_text=_('is admin'))

    def __str__(self):
        return self.username
