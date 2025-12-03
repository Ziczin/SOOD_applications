from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from apps.api.core.get_permissions import get_permissions
from apps.api.core.permissions import permissions

class RoleRedirectMixin:
    required_role = None

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        if self.required_role:
            roles = set(get_permissions(request.user) or [])
            if self.required_role not in roles:
                return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

class Mixed(LoginRequiredMixin, RoleRedirectMixin, TemplateView):
    template_name = 'application/builder.html'

class DashboardView(Mixed):
    extra_context = {'variant': 'dashboard'}

@permissions("get:admin")
class FormManagerView(Mixed):
    required_role = 'admin'
    extra_context = {'variant': 'forms_manager'}

@permissions("get:admin")
class EnumsManagerView(Mixed):
    required_role = 'admin'
    extra_context = {'variant': 'enums_manager'}

@permissions("get:admin")
class CharsetManagerView(Mixed):
    required_role = 'admin'
    extra_context = {'variant': 'charsets_manager'}

@permissions("get:admin")
class UsersManagerView(Mixed):
    required_role = 'admin'
    extra_context = {'variant': 'users_manager'}

@permissions("get:admin")
class FieldsManagerView(Mixed):
    required_role = 'admin'
    extra_context = {'variant': 'fields_manager'}
