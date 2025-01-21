from celery import shared_task

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


@shared_task
def send_booking_email_task(user_email, context, ta_email):
    subject = "تایید رزرو"
    message = render_to_string('emails/booking_confirmation.html', context)
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
    email.content_subtype = 'html'
    email.send()

    subject = f"رزرو جدید برای فرم {context['form_name']}"
    message = render_to_string('emails/booking_confirmation_ta.html', context)
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [ta_email])
    email.content_subtype = 'html'
    email.send()


@shared_task
def send_admin_request_email_task(context):
    subject = "درخواست ثبت‌نام به عنوان ادمین"
    message = render_to_string('emails/admin_request.html', context)
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, ['amirhosseinkhalili901@gmail.com'])
    email.content_subtype = 'html'
    email.send()

@shared_task
def send_cancel_mail_task(user_mail, context, ta_email):
    subject = "کنسل کردن تایم رزرو شده"
    message = render_to_string('emails/canceling_confirmation.html', context)
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [user_mail])
    email.content_subtype = 'html'
    email.send()

    subject = f"کنسل کردن تایم رزرو شده برای فرم {context['form_name']}"
    message = render_to_string('emails/canceling_confirmation_ta.html', context)
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [ta_email])
    email.content_subtype = 'html'
    email.send()
