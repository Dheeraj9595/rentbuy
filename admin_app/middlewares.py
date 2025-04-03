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
