from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('form/', include(('form.urls', 'form'), namespace='form')),
]
