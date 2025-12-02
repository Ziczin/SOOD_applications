from django.shortcuts import render
from django.urls import path
from .views import (
    register,
    login_view,
    logout_view,
    permission_denied_view,
    wnauthorized_view
)


urls = {
    'register/': register,
    'login/': login_view,
    'logout/': logout_view,
    'sandbox/': lambda request: render(request, 'users/sandbox.html'),
    'sandbox2/': lambda request: render(request, 'users/sandbox2.html'),
    'sandbox3/': lambda request: render(request, 'users/sandbox3.html'),
    'testbox/': lambda request: render(request, 'users/testbox.html'),
    '403/': permission_denied_view,
    '401/': wnauthorized_view
}

urlpatterns = [path(url, urls[url], name=url[:-1]) for url in urls]
