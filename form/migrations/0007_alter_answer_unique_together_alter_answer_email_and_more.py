# Generated by Django 5.1.4 on 2025-01-14 12:04

from django.db import migrations, models

def populate_email(apps, schema_editor):
    Answer = apps.get_model('form', 'Answer')
    for answer in Answer.objects.all():
        if answer.first_name and answer.last_name:
            answer.email = f"{answer.first_name.lower()}{answer.last_name.lower()}@gmail.com"
            answer.save()

class Migration(migrations.Migration):

    dependencies = [
        ('form', '0006_alter_answer_unique_together_answer_email_and_more'),
    ]

    operations = [
        migrations.RunPython(
            populate_email
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together={('form', 'student_id'), ('form', 'time_slot')},
        ),
        migrations.AlterField(
            model_name='answer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together={('form', 'email'), ('form', 'student_id'), ('form', 'time_slot')},
        ),
    ]
