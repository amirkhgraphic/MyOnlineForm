from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.urls import reverse

from .models import Form, TimeSlot, Answer
from .permissions import AdminRequiredMixin
from utils.persian import convert_to_jalali


class FormListView(AdminRequiredMixin, ListView):
    model = Form
    template_name = 'form/list.html'
    context_object_name = 'forms'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)


class FormDetailView(DetailView):
    model = Form
    template_name = 'form/detail.html'
    context_object_name = 'form'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        time_slots = self.object.time_slots.all().order_by('datetime')
        context['time_slots'] = convert_to_jalali(time_slots)
        return context


class SuccessView(TemplateView):
    template_name = 'form/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs.get('slug')
        return context


class BookTimeSlotView(View):
    def get(self, request, slug, pk):
        time_slot = get_object_or_404(TimeSlot, pk=pk, is_available=True)

        now = timezone.now()
        if time_slot.datetime < now or time_slot.form.slug != slug:
            raise Http404()

        context = {
            'time_slot': convert_to_jalali([time_slot])[0],
            'form_slug': time_slot.form.slug,
        }
        return render(request, 'form/book-time-slot.html', context)

    def post(self, request, slug, pk):
        time_slot = get_object_or_404(TimeSlot, pk=pk, is_available=True)
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

                if int(student_id) == 1401020111157:
                    return render(request, 'form/nothing-special.html')

                return redirect(reverse('form:success', kwargs={'slug': slug}))
            except IntegrityError:
                messages.error(request, "شما قبلا با این کد دانشجویی ثبت نام کرده اید")
        else:
            messages.error(request, "شما نمی‌توانید برای این فرم پاسخی ثبت کنید!")

        context = {
            'time_slot': convert_to_jalali([time_slot])[0],
            'form_slug': time_slot.form.slug,
        }
        return render(request, 'form/book-time-slot.html', context)


class BookedTimeSlotsView(AdminRequiredMixin, ListView):
    template_name = 'form/booked-time-slots.html'
    context_object_name = 'booked_slots'

    def get_queryset(self):
        form = get_object_or_404(Form, slug=self.kwargs['slug'])

        if form.created_by != self.request.user:
            raise PermissionDenied()

        booked_slots = TimeSlot.objects.filter(form=form, is_available=False)
        return convert_to_jalali(booked_slots)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = get_object_or_404(Form, slug=self.kwargs['slug'])
        context['form'] = form
        return context
