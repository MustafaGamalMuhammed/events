from django.contrib.auth.mixins import AccessMixin


class OwnerRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        """Verify that the current user is authenticated and is the owner."""

        event = self.get_object()

        if not request.user.is_authenticated or not event.is_owner(request):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)