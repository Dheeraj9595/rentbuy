import logging

logger = logging.getLogger('django')


class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Log only authenticated users' requests
        if request.user.is_authenticated:
            logger.info(f"User: {request.user.username}, Method: {request.method}, Path: {request.path}")

        return response

from django.shortcuts import redirect
from django.conf import settings

class RedirectRootMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Redirect only the root URL
        # breakpoint()
        if request.path == '/':
            return redirect('/home/')  # or use reverse() if you prefer named URL
        return self.get_response(request)
