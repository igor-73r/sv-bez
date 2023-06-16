from django.urls import reverse
from django.http import Http404

class RestrictStaffToAdminMiddleware:
    """
    A middleware that restricts staff members access to administration panels.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_ips = ['127.0.0.1']
        ip = request.META.get('REMOTE_ADDR')
        if request.path.startswith(reverse('admin:index')):
            if ip not in allowed_ips:
                raise Http404
        return self.get_response(request)
