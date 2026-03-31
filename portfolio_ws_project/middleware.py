from django.http import HttpResponsePermanentRedirect

class RedirectWwwMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_redirects = {
            "www.kathysnell.dev": "https://kathysnell.dev",
        }

    def __call__(self, request):
        host = request.get_host().lower()
        if host in self.allowed_redirects:
            return HttpResponsePermanentRedirect(f"{self.allowed_redirects[host]}{request.path}")
        return self.get_response(request)
