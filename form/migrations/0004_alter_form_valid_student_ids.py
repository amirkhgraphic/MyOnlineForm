# Generated by Django 5.1.4 on 2025-01-11 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0003_alter_form_valid_student_ids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='valid_student_ids',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
