import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0004_alter_form_valid_student_ids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='course_name',
            field=models.CharField(help_text='نام درس مرتبط با این فرم', max_length=255),
        ),
        migrations.AlterField(
            model_name='form',
            name='professor_name',
            field=models.CharField(help_text='نام استاد درس مرتبط با این فرم', max_length=255),
        ),
        migrations.AlterField(
            model_name='form',
            name='semester',
            field=models.CharField(choices=[('0', 'ترم پاییز'), ('1', 'ترم بهار')], help_text='ترم جاری', max_length=1),
        ),
        migrations.AlterField(
            model_name='form',
            name='year',
            field=models.PositiveIntegerField(help_text='سال تحصیلی (مثلا: ۱۴۰۳)', validators=[django.core.validators.MinValueValidator(1403)]),
        ),
    ]
