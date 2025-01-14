from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def send_booking_email_task(user_email, context):
    subject = "تایید رزرو"
    message = render_to_string('emails/booking_confirmation.html', context)
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
    email.content_subtype = 'html'
    email.send()
