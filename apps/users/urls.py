from django.urls import path
from .views import (
    register,
    login_view,
    logout_view,
    sandbox,
    sandbox2,
    permission_denied_view
)

urls = {
    'register/': register,
    'login/': login_view,
    'logout/': logout_view,
    'sandbox/': sandbox,
    'sandbox2/': sandbox2,
    '403/': permission_denied_view
}

urlpatterns = [path(url, urls[url], name=url[:-1]) for url in urls]
