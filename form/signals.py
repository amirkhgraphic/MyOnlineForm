from datetime import timedelta

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now

from .models import Answer
from .tasks import (
    send_booking_email_task,
    send_cancel_mail_task,
    send_presentation_reminder,
)
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
        'user_email': instance.email,
    }
    send_booking_email_task.delay(student_email, email_data, ta_email)

    reserved_time = instance.timeslot.datetime
    jalali_datetime = convert_to_jalali([instance.time_slot])[0]['datetime']
    context = {
        "title": instance.form.name,
        "first_name": instance.first_name,
        "last_name": instance.last_name,
        "datetime": jalali_datetime,
        "google_meet_link": instance.form.google_meet_url,
        "delta_phrase": "فلان قدر",
    }

    # for test only ------------------------------------------------------------- be gone!
    send_presentation_reminder.apply_async(
        args=[context, student_email],
        eta=now() + timedelta(minutes=2)
    )
    # be gone seriously ------------------------------------------------------------- :_)

    if reserved_time - timedelta(days=1) > now():
        # One day before
        context['delta_phrase'] = "۱ روز"
        send_presentation_reminder.apply_async(
            args=[context, student_email],
            eta=reserved_time - timedelta(days=1)
        )

    if reserved_time - timedelta(hours=1) > now():
        # One hour before
        context['delta_phrase'] = "۱ ساعت"
        send_presentation_reminder.apply_async(
            args=[context, student_email],
            eta=reserved_time - timedelta(hours=1)
        )

    if reserved_time - timedelta(minutes=30) > now():
        # 30 minutes before
        context['delta_phrase'] = "۳۰ دقیقه"
        send_presentation_reminder.apply_async(
            args=[context, student_email],
            eta=reserved_time - timedelta(minutes=30)
        )


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
    send_cancel_mail_task.delay(student_email, email_data, ta_email)
