from django.conf import settings
from slugify import slugify

from django.db import models


class Form(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    valid_student_ids = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='forms',
        default=1
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, separator='-')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'#{self.id}: {self.name}'


class TimeSlot(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='time_slots')
    datetime = models.DateTimeField()
    is_available = models.BooleanField(default=True, blank=True)

    class Meta:
        unique_together = ('form', 'datetime')

    def mark_unavailable(self):
        self.is_available = False
        self.save()

    def __str__(self):
        return f'{self.datetime} - {self.form.name}'


class Answer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=15)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='answers')
    time_slot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE, related_name='answer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.time_slot.is_available:
            raise ValueError("This time slot is no longer available.")

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.time_slot.is_available = True
        self.time_slot.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}: {self.time_slot}'

    class Meta:
        unique_together = (
            ('form', 'student_id'),
            ('form', 'time_slot')
        )
