from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Answer
from .tasks import send_booking_email_task, send_cancel_mail_task
from utils.persian import convert_to_jalali


@receiver(post_save, sender=Answer)
def send_email_on_answer_create(sender, instance, created, **kwargs):
    """
    Send an email to the student and TA whenever a new Answer is created.
    """
    if not created:
        return

    student_email = instance.email
    ta_email = instance.form.created_by.email
    email_data = {
        'first_name': instance.first_name,
        'last_name': instance.last_name,
        'student_id': instance.student_id,
        'datetime': convert_to_jalali([instance.time_slot])[0]['datetime'],
        'form_name': instance.form.name,
    }
    send_booking_email_task(student_email, email_data, ta_email)


@receiver(post_delete, sender=Answer)
def send_cancel_email_on_answer_delete(sender, instance, **kwargs):
    """
    Send an email to the student and TA whenever a Answer is deleted.
    """
    student_email = instance.email
    ta_email = instance.form.created_by.email
    jalali_datetime = convert_to_jalali([instance.time_slot])[0]['datetime']
    email_data = {
        'first_name': instance.first_name,
        'last_name': instance.last_name,
        'student_id': instance.student_id,
        'datetime': jalali_datetime,
        'form_name': instance.time_slot.form.name,
    }
    send_cancel_mail_task(student_email, email_data, ta_email)
