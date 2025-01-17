# Generated by Django 5.1.4 on 2025-01-11 16:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='course_name',
            field=models.CharField(blank=True, help_text='نام درس مرتبط با این فرم', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='form',
            name='professor_name',
            field=models.CharField(blank=True, help_text='نام استاد درس مرتبط با این فرم', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='form',
            name='semester',
            field=models.CharField(blank=True, choices=[('0', 'ترم پاییز'), ('1', 'ترم بهار')], help_text='ترم جاری', max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='form',
            name='year',
            field=models.PositiveIntegerField(blank=True, help_text='سال تحصیلی (مثلا: ۱۴۰۳)', null=True, validators=[django.core.validators.MinValueValidator(1403)]),
        ),
    ]
