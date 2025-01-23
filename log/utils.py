from .models import EmailLog, ActivityLog


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_device_info(request):
    user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
    return user_agent


def log_activity(action, instance, request):
    """
    Logs an activity related to a model instance.

    Args:
        action (str): The action being performed ('create', 'update', 'delete', 'access', etc.).
        instance (Model): The model instance the action relates to.
        request (Request): The request sent by the client.
    """
    model_name = instance.__class__.__name__
    instance_id = instance.pk
    user = request.user if request.user.is_authenticated else None
    ip_address = get_client_ip(request)
    device_info = get_device_info(request)

    ActivityLog.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        model_instance_id=instance_id,
        ip_address=ip_address,
        device_info=device_info,
    )


def log_email(sender_email, subject, receiver_email, status):
    """
    Logs email-related activities.
    """
    EmailLog.objects.create(
        sender=sender_email,
        receiver=receiver_email,
        subject=subject,
        status=status,
    )
