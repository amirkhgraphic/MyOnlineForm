import io
import json

from django.core.exceptions import PermissionDenied
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.core.management import call_command


class ReadFixturesView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied()

        buffer = io.StringIO()
        call_command('dumpdata', 'users', 'form', '--indent', '4', stdout=buffer)
        buffer.seek(0)
        fixtures_data = json.loads(buffer.read())
        return JsonResponse(fixtures_data, safe=False)


class DownloadFixturesView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied()

        buffer = io.StringIO()
        call_command('dumpdata', 'users', 'form', '--indent', '4', stdout=buffer)
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="db-fixtures.json"'
        return response
