from django.core.exceptions import PermissionDenied

class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied("You do not have permission to access this page.")
