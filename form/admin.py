from django.contrib import admin

from .models import Form, TimeSlot, Answer
from utils.persian import convert_to_jalali


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'form', 'jalali_datetime', 'is_available')
    list_filter = ('form', 'is_available', 'datetime')
    search_fields = ('form__name',)
    ordering = ('-datetime',)
    actions = ['mark_as_unavailable', 'mark_as_available']

    def jalali_datetime(self, obj):
        return convert_to_jalali([obj])[0]['datetime']

    jalali_datetime.short_description = 'Jalali DateTime'

    @admin.action(description='Mark selected time slots as unavailable')
    def mark_as_unavailable(self, request, queryset):
        queryset.update(is_available=False)
        self.message_user(request, "Selected time slots have been marked as unavailable.")

    @admin.action(description='Mark selected time slots as available')
    def mark_as_available(self, request, queryset):
        queryset.update(is_available=True)
        self.message_user(request, "Selected time slots have been marked as available.")


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'student_id', 'form', 'jalali_datetime', 'created_at')
    list_filter = ('form', 'created_at')
    search_fields = ('first_name', 'last_name', 'student_id', 'time_slot__datetime', 'form__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    def jalali_datetime(self, obj):
        return convert_to_jalali([obj.time_slot])[0]['datetime']

    jalali_datetime.short_description = 'Jalali DateTime'
