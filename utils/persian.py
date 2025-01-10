import datetime
import jdatetime

from django.db.models import QuerySet
from django.utils import timezone

from form.models import TimeSlot


def convert_numbers(input_str: str):
    english_to_persian_digits = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
    return input_str.translate(english_to_persian_digits)


def convert_to_jalali(time_slots: list[TimeSlot] | QuerySet) -> list[dict]:
    jdatetime.set_locale(jdatetime.FA_LOCALE)
    now = timezone.now()

    return [
        {
            'id': slot.id,
            'is_passed': bool(slot.datetime < now),
            'answer': slot.answer if hasattr(slot, 'answer') else None,
            'datetime': convert_numbers((jdatetime.datetime.fromgregorian(datetime=slot.datetime) + datetime.timedelta(hours=3, minutes=30)).strftime('%A %d %B %Y - %H:%M')),
        }
        for slot in time_slots
    ]
