from django.contrib import admin

from .models import ActivityLog, EmailLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'model_name', 'model_instance_id', 'created_at')
    search_fields = ('user', 'model_name', 'action')
    list_filter = ('action', 'created_at')


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('sender', 'subject', 'receiver', 'status', 'created_at')
    search_fields = ('sender', 'subject', 'receiver')
    list_filter = ('created_at', 'subject', 'sender', 'receiver', 'status')
