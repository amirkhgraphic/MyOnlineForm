from django.urls import path

from . import views


urlpatterns = [
    path('', views.form_list, name='form_list'),
    path('form/<slug:slug>/', views.form_detail, name='form_detail'),
    path('form/<slug:slug>/<int:pk>/book/', views.book_time_slot, name='book_time_slot'),
    path('form/<slug:slug>/booked/', views.booked_time_slots, name='book_time_slot'),
    path('success/', views.success_view, name='success'),
]
