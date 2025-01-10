from django.urls import path

from . import views


urlpatterns = [
    path('', views.form_list, name='list'),
    path('<slug:slug>/', views.form_detail, name='detail'),
    path('<slug:slug>/time/<int:pk>/', views.book_time_slot, name='book-time-slot'),
    path('<slug:slug>/booked/', views.booked_time_slots, name='booked-time-slots'),
    path('<slug:slug>/success/', views.success_view, name='success'),
]
