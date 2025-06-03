from celery import shared_task

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from log.models import EmailLog


@shared_task
def send_booking_email_task(user_email, context, ta_email):
    subject = "تایید رزرو"
    message = render_to_string('emails/booking_confirmation.html', context)
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
    email.content_subtype = 'html'
    try:
        email.send()
        EmailLog.objects.create(
            sender=settings.DEFAULT_FROM_EMAIL,
            receiver=user_email,
            subject=subject,
            status='sent'
        )
    except Exception as e:
        EmailLog.objects.create(
            sender=settings.DEFAULT_FROM_EMAIL,
            receiver=user_email,
            subject=subject,
            status='failed',
            error=str(e),
        )

    subject = f"رزرو جدید برای فرم {context['form_name']}"
    message = render_to_string('emails/booking_confirmation_ta.html', context)
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [ta_email])
    email.content_subtype = 'html'
    try:
        email.send()
        EmailLog.objects.create(
            sender=settings.DEFAULT_FROM_EMAIL,
            receiver=ta_email,
            subject=subject,
            status='sent'
        )
    except Exception as e:
        EmailLog.objects.create(
            sender=settings.DEFAULT_FROM_EMAIL,
            receiver=ta_email,
            subject=subject,
            status='failed',
            error=str(e),
        )


@shared_task
def send_admin_request_email_task(context):
    subject = "درخواست ثبت‌نام به عنوان ادمین"
    message = render_to_string('emails/admin_request.html', context)
    receiver_email = 'amirhosseinkhalili901@gmail.com'
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [receiver_email])
    email.content_subtype = 'html'
    try:
        email.send()
        EmailLog.objects.create(
            sender=settings.DEFAULT_FROM_EMAIL,
            receiver=receiver_email,
            subject=subject,
            status='sent'
        )
    except Exception as e:
        EmailLog.objects.create(
            sender=settings.DEFAULT_FROM_EMAIL,
            receiver=receiver_email,
            subject=subject,
            status='failed',
            error=str(e),
        )


@shared_task
def send_cancel_mail_task(user_mail, context, ta_email):
    subject = "کنسل کردن تایم رزرو شده"
    message = render_to_string('emails/canceling_confirmation.html', context)
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [user_mail])
    email.content_subtype = 'html'
    try:
        email.send()
        EmailLog.objects.create(
            sender=settings.DEFAULT_FROM_EMAIL,
            receiver=user_mail,
            subject=subject,
            status='sent'
        )
    except Exception as e:
        EmailLog.objects.create(
            sender=settings.DEFAULT_FROM_EMAIL,
            receiver=user_mail,
            subject=subject,
            status='failed',
            error=str(e),
        )

    subject = f"کنسل کردن تایم رزرو شده برای فرم {context['form_name']}"
    message = render_to_string('emails/canceling_confirmation_ta.html', context)
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [ta_email])
    email.content_subtype = 'html'
    try:
        email.send()
        EmailLog.objects.create(
            sender=settings.DEFAULT_FROM_EMAIL,
            receiver=ta_email,
            subject=subject,
            status='sent'
        )
    except Exception as e:
        EmailLog.objects.create(
            sender=settings.DEFAULT_FROM_EMAIL,
            receiver=ta_email,
            subject=subject,
            status='failed',
            error=str(e),
        )


@shared_task
def send_presentation_reminder(context, user_mail):
    """
    context = {
        title: "form title"
        first_name: "user first_name"
        last_name: "user last_name"
        datetime: "reserved datetime"
        google_meet_link: "google meet link"
        delta_phrase: "time left until the presentation"
    }
    """

    subject = (f"یادآوری! {context["delta_phrase"]} تا ارائه: {context['title']}")
    message = render_to_string('emails/booking_reminder.html', context)
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [user_mail])
    email.content_subtype = 'html'
    try:
        email.send()
        EmailLog.objects.create(
            sender=settings.DEFAULT_FROM_EMAIL,
            receiver=user_mail,
            subject=subject,
            status='sent'
        )
    except Exception as e:
        EmailLog.objects.create(
            sender=settings.DEFAULT_FROM_EMAIL,
            receiver=user_mail,
            subject=subject,
            status='failed',
            error=str(e),
        )
