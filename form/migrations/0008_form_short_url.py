# Generated by Django 5.1.4 on 2025-01-18 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0007_alter_answer_unique_together_alter_answer_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='short_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
