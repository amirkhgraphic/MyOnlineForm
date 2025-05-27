from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ActivityLog(models.Model):
    """Logs activities related to model instances."""
    ACTIONS_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('access', 'Access'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTIONS_CHOICES)
    model_name = models.CharField(max_length=255, null=True, blank=True)
    model_instance_id = models.CharField(max_length=511, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device_info = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action}: {self.model_name} <#{self.model_instance_id}>"


class EmailLog(models.Model):
    """Logs email activities."""
    STATUS_CHOICES = (
        ('sent', 'Sent'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    sender = models.EmailField(max_length=255)
    receiver = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    error = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver} [{self.status.upper()}]"
