import datetime

from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone
from django.utils.timezone import make_aware
from django.views import View, generic
from django.urls import reverse, reverse_lazy

from .forms import FormCreateForm, TimeSlotCreateForm, TimeSlotsCreateForm
from .models import Form, TimeSlot, Answer
from .permissions import AdminRequiredMixin
from utils.persian import convert_to_jalali


class FormListView(AdminRequiredMixin, generic.ListView):
    model = Form
    template_name = 'form/list.html'
    context_object_name = 'forms'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)


class FormDetailView(generic.DetailView):
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


class FormCreateView(AdminRequiredMixin, generic.CreateView):
    model = Form
    template_name = 'form/create.html'
    form_class = FormCreateForm
    success_url = reverse_lazy('form:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class FormUpdateView(generic.UpdateView):
    model = Form
    form_class = FormCreateForm
    template_name = 'form/update.html'

    def get_success_url(self):
        return reverse_lazy('form:detail', kwargs={'slug': self.object.slug})


class TimeSlotCreateView(generic.CreateView):
    model = TimeSlot
    form_class = TimeSlotCreateForm
    template_name = 'form/time-slot-create.html'

    def form_valid(self, form):
        form_id = self.kwargs.get('form_id')
        form_instance = get_object_or_404(Form, pk=form_id)
        form.instance.form = form_instance
        return super().form_valid(form)

    def get_success_url(self):
        form_id = self.kwargs.get('form_id')
        form_instance = get_object_or_404(Form, id=form_id)
        return reverse_lazy('form:detail', kwargs={'slug': form_instance.slug})

    def get_context_data(self, **kwargs):
        form_id = self.kwargs.get('form_id')
        context = super().get_context_data(**kwargs)
        context['obj'] = get_object_or_404(Form, id=form_id)
        return context


class TimeSlotsCreateView(generic.View):
    template_name = 'form/time-slots-create.html'

    def get(self, request, *args, **kwargs):
        form_id = kwargs.get('form_id')
        obj = get_object_or_404(Form, id=form_id)
        form = TimeSlotsCreateForm()
        return render(request, self.template_name, {
            'form': form,
            'obj': obj,
        })

    def post(self, request, *args, **kwargs):
        form_id = kwargs.get('form_id')
        obj = get_object_or_404(Form, pk=form_id)
        form = TimeSlotsCreateForm(request.POST)

        if form.is_valid():
            date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']
            slot_count = form.cleaned_data['slot_count']
            duration = form.cleaned_data['duration']
            breaktime = form.cleaned_data['breaktime']

            day = date
            start = start_time
            current_time = datetime.datetime.combine(day, start)
            aware_start_time = make_aware(current_time)

            time_slots = [
                TimeSlot(form_id=form_id, datetime=aware_start_time + datetime.timedelta(minutes=duration * i))
                for i in range(slot_count)
            ]
            TimeSlot.objects.bulk_create(time_slots)
            return redirect('form:detail', slug=obj.slug)

        return render(request, self.template_name, {'form': form})


class TimeSlotDeleteView(AdminRequiredMixin, generic.DeleteView):
    model = TimeSlot
    template_name = 'form/time-slot-confirm-delete.html'
    context_object_name = 'time_slot'

    def get_success_url(self):
        return reverse_lazy('form:detail', kwargs={'slug': self.object.form.slug})

    def get_object(self, queryset=None):
        time_slot = get_object_or_404(TimeSlot, pk=self.kwargs['pk'])
        form = get_object_or_404(Form, slug=self.kwargs['slug'])

        if form.created_by != self.request.user or time_slot.form != form:
            raise PermissionDenied()

        return time_slot

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datetime'] = convert_to_jalali([context['time_slot']])[0]['datetime']
        return context


class SuccessView(generic.TemplateView):
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


class BookedTimeSlotsView(AdminRequiredMixin, generic.ListView):
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


class AnswerDeleteView(generic.DeleteView):
    model = Answer
    template_name = 'form/delete-answer-confirm.html'
    context_object_name = 'answer'

    def get_success_url(self):
        return reverse_lazy('form:booked-time-slots', kwargs={'slug': self.object.form.slug})

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user == queryset.first().form.created_by:
            return queryset

        return queryset.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['datetime'] = convert_to_jalali([context['answer'].time_slot])[0]['datetime']
        return context