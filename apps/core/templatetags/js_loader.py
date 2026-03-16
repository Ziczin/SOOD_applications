from django import template
from django.templatetags.static import static
from django.conf import settings
import os

register = template.Library()


@register.simple_tag
def js_file(original_path):
    clean_path = original_path.lstrip("/")
    if getattr(settings, "SEND_MINIFIED_JS", True):
        name_without_ext = os.path.splitext(clean_path)[0]
        return static(f"collected/js/{name_without_ext}.js")
    return static(f"deps/js/{clean_path}")
