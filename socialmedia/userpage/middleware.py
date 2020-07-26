from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_fun, view_args, view_kwargs):
        authenticated = request.user.is_authenticated
        url = request.path

        if authenticated and url == settings.HOME_URL:
            logout(request)
            
        if not authenticated and (url != settings.HOME_URL and url not in settings.EXEMPT_URL):
            return redirect(settings.HOME_URL)
