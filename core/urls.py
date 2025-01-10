from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('form/', include(('form.urls', 'form'), namespace='form')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
