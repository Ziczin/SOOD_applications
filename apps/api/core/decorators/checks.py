from rest_framework.response import Response
from rest_framework import status

def is_authenticated(request, view, *args, **kwargs):
    user = getattr(request, "user", None)
    return bool(user and user.is_authenticated)

def role_admin(request, view, *args, **kwargs):
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return False
    return getattr(user, "role", None) == "admin"

def role_moderator(request, view, *args, **kwargs):
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return False
    return getattr(user, "role", None) == "moderator"

def status_proxy(request, view, *args, **kwargs):
    user = getattr(request, "user", None)
    if not user:
        return False
    return getattr(user, "proxy", None) is True