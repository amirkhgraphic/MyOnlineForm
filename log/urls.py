from django.urls import path

from .views import DownloadFixturesView, ReadFixturesView


urlpatterns = [
    path('backup/db/d/', DownloadFixturesView.as_view(), name='download-db-backup'),
    path('backup/db/r/', ReadFixturesView.as_view(), name='read-db-backup'),
]