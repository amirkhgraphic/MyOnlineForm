from django.urls import path

from . import views


urlpatterns = [
    path('', views.FormListView.as_view(), name='list'),
    path('create/', views.FormCreateView.as_view(), name='create'),
    path('<slug:slug>/', views.FormDetailView.as_view(), name='detail'),
    path('<slug:slug>/update/', views.FormUpdateView.as_view(), name='update'),
    path('<slug:slug>/time/<int:pk>/', views.BookTimeSlotView.as_view(), name='book-time-slot'),
    path('<slug:slug>/answers/', views.BookedTimeSlotsView.as_view(), name='answers'),
    path('<slug:slug>/success/', views.SuccessView.as_view(), name='success'),
    path('delete-time-slot/<int:pk>/', views.AnswerDeleteView.as_view(), name='delete-answer'),
    path('add-timeslot/<int:form_id>/', views.TimeSlotCreateView.as_view(), name='add-time-slot'),
    path('add-timeslots/<int:form_id>/', views.TimeSlotsCreateView.as_view(), name='add-time-slots'),
    path('<slug:slug>/time-slot/delete/<int:pk>/', views.TimeSlotDeleteView.as_view(), name='delete-time-slot'),
]
