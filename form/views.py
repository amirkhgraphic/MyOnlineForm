from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Form, TimeSlot, Answer
from .permissions import admin_required


@admin_required
def form_list(request):
    forms = Form.objects.all()
    return render(request, 'form/form_list.html', {'forms': forms})


def form_detail(request, slug):
    form = get_object_or_404(Form, slug=slug)
    time_slots = form.time_slots.all().order_by('datetime')
    return render(request, 'form/form_detail.html', {'form': form, 'time_slots': time_slots})


def success_view(request):
    return render(request, 'form/success.html')


def book_time_slot(request, slug, pk):
    time_slot = get_object_or_404(TimeSlot, pk=pk, is_available=True)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')

        if not time_slot.form.valid_student_ids or int(student_id) in time_slot.form.valid_student_ids:
            try:
                Answer.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    student_id=student_id,
                    form=time_slot.form,
                    time_slot=time_slot
                )
                time_slot.mark_unavailable()
                return redirect('success')
            except IntegrityError:
                messages.error(request, "شما قبلا با این کد دانشجویی ثبت نام کرده اید")
        else:
            messages.error(request, "شما نمی‌توانید برای این فرم پاسخی ثبت کنید!")

    return render(request, 'form/book_time_slot.html', {'time_slot': time_slot})


@admin_required
def booked_time_slots(request, slug):
    form = get_object_or_404(Form, slug=slug)
    booked_slots = TimeSlot.objects.filter(form=form, is_available=False)

    return render(request, 'form/booked_time_slots.html', {
        'form': form,
        'booked_slots': booked_slots
    })
