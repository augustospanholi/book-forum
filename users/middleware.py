from django.shortcuts import redirect

ALLOWED_URLS = ['/banned', '/logout']


class BannedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_active:
            if not any(request.path.startswith(url) for url in ALLOWED_URLS):
                return redirect('banned')
        return self.get_response(request)
