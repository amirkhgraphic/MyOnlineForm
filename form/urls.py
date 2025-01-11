from django.urls import path

from . import views


urlpatterns = [
    path('', views.FormListView.as_view(), name='list'),
    path('create/', views.FormCreateView.as_view(), name='create'),
    path('<slug:slug>/', views.FormDetailView.as_view(), name='detail'),
    path('<slug:slug>/time/<int:pk>/', views.BookTimeSlotView.as_view(), name='book-time-slot'),
    path('<slug:slug>/answers/', views.BookedTimeSlotsView.as_view(), name='booked-time-slots'),
    path('<slug:slug>/success/', views.SuccessView.as_view(), name='success'),
    path('delete-time-slot/<int:pk>/', views.AnswerDeleteView.as_view(), name='delete-answer'),
]
