from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from form.views import redirect_to_form

urlpatterns = [
    path('admin/', admin.site.urls),

    path('f/<str:short_key>/', redirect_to_form, name='form-short-url'),
    path('form/', include(('form.urls', 'form'), namespace='form')),
    path('user/', include(('users.urls', 'users'), namespace='users')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
