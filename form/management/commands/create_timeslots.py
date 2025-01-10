import datetime
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware

from form.models import TimeSlot


class Command(BaseCommand):
    help = "Generate time slots for a specific day."

    def add_arguments(self, parser):
        parser.add_argument('date', type=str, help="Date in YYYY-MM-DD format")
        parser.add_argument('start_time', type=str, help="Start time in HH:MM format")
        parser.add_argument('slot_count', type=int, help="Number of time slots to create")
        parser.add_argument('duration', type=int, help="Duration of each slot in minutes")
        parser.add_argument('form_id', type=int, help="ID of the Form to create timeslots")

    def handle(self, *args, **kwargs):
        date = kwargs['date']
        start_time = kwargs['start_time']
        slot_count = kwargs['slot_count']
        duration = kwargs['duration']
        form_id = kwargs['form_id']

        try:
            day = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            start = datetime.datetime.strptime(start_time, '%H:%M').time()
            current_time = datetime.datetime.combine(day, start)
            aware_start_time = make_aware(current_time)

            TimeSlot.objects.bulk_create([
                TimeSlot(form_id=form_id, datetime=aware_start_time + datetime.timedelta(minutes=duration * i))
                for i in range(slot_count)
            ])

            self.stdout.write(self.style.SUCCESS(f"Successfully created {slot_count} time slots for from #{form_id}."))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating time slots: {e}"))
