from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from form.tasks import send_admin_request_email_task
from .forms import UserSignUpForm, UserProfileForm
from .models import User


class UserSignUpView(FormView):
    template_name = 'users/signup.html'
    form_class = UserSignUpForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()

        username = form.cleaned_data['username']
        raw_password = form.cleaned_data['password1']
        user = authenticate(username=username, password=raw_password)

        if form.cleaned_data['apply_for_ta']:
            send_admin_request_email_task({
                'username': username,
            })

        if user is not None:
            login(self.request, user)
     
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
