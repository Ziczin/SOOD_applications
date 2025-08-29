# apps/users/mixins.py
from typing import Iterable, Union
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.urls import reverse_lazy

DEFAULT_LOGIN_URL = reverse_lazy("users:login")  # или 'users/login' если нет namespaced URL
DEFAULT_FAIL_REDIRECT = resolve_url("application:dashboard")  # или '/application/dashboard'

RoleLike = Union[str, Iterable[str]]

class ProxyRequiredMixin(LoginRequiredMixin):
    """
    Требует user.proxy == True.
    При неаутентифицированности -> users/login.
    При proxy == False -> redirect to application/dashboard.
    """
    login_url = DEFAULT_LOGIN_URL
    redirect_field_name = "next"
    fail_redirect = DEFAULT_FAIL_REDIRECT

    def get_fail_redirect(self):
        return resolve_url(self.fail_redirect)

    def handle_no_permission(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return HttpResponseRedirect(self.get_fail_redirect())

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        if not getattr(request.user, "proxy", False):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
