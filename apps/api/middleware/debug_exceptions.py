import traceback
from django.http import HttpResponseServerError

class DebugExceptionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception:
            traceback.print_exc()
            raise