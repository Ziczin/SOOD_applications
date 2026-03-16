from django.conf import settings

def minified_js(request):
    return {
        'SEND_MINIFIED_JS': getattr(settings, 'SEND_MINIFIED_JS', False)
    }
