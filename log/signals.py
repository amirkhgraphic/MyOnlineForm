from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import ActivityLog
from .middleware import get_current_request

@receiver(post_save)
def log_model_save(sender, instance, created, **kwargs):
    """
    Logs create and update actions for model instances.
    """
    if sender == ActivityLog:
        return

    request = get_current_request()
    action = 'create' if created else 'update'

    ActivityLog.objects.create(
        user=getattr(request, 'user', None),
        action=action,
        model_name=sender.__name__,
        model_instance_id=instance.pk,
        ip_address=getattr(request, 'META', {}).get('REMOTE_ADDR'),
        device_info=request.META.get('HTTP_USER_AGENT') if request else None,
    )


@receiver(post_delete)
def log_model_delete(sender, instance, **kwargs):
    """
    Logs delete actions for model instances.
    """
    if sender == ActivityLog:
        return

    request = get_current_request()

    ActivityLog.objects.create(
        user=getattr(request, 'user', None),
        action='delete',
        model_name=sender.__name__,
        model_instance_id=instance.pk,
        ip_address=getattr(request, 'META', {}).get('REMOTE_ADDR'),
        device_info=request.META.get('HTTP_USER_AGENT') if request else None,
    )
