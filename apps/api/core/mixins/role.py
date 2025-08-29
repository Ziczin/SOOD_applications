# apps/users/mixins.py
from typing import Iterable, Optional, Tuple, Union
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.urls import reverse_lazy

# По умолчанию
DEFAULT_LOGIN_URL = reverse_lazy("users:login")  # или 'users/login' если нет namespaced URL
DEFAULT_FAIL_REDIRECT = resolve_url("application:dashboard")  # или '/application/dashboard'

RoleLike = Union[str, Iterable[str]]

def _normalize_roles(roles: Optional[RoleLike]) -> Tuple[str, ...]:
    if roles is None:
        return ()
    if isinstance(roles, str):
        return (roles,)
    try:
        return tuple(roles)
    except TypeError:
        return (str(roles),)


class RoleRequiredMixin(LoginRequiredMixin):
    """
    Требует, чтобы request.user.role совпадал с одной из required_roles.
    По умолчанию:
      - при неаутентифицированности -> redirect to users/login
      - при отсутствии роли -> redirect to application/dashboard
    Использование:
      class V(RoleRequiredMixin, TemplateView):
          required_roles = 'MODERATOR'  # или ['ADMIN','MODERATOR']
    Также можно создавать класс вызовом RoleRequiredMixin.with_roles(...)
      class V(RoleRequiredMixin.with_roles('ADMIN'), TemplateView): ...
    """
    login_url = DEFAULT_LOGIN_URL
    redirect_field_name = "next"

    required_roles: Tuple[str, ...] = ()

    fail_redirect = DEFAULT_FAIL_REDIRECT

    @classmethod
    def with_roles(cls, roles: RoleLike):
        """Фабрика: возвращает новый класс с захваченными required_roles."""
        normalized = _normalize_roles(roles)

        name = f"{cls.__name__}_" + "_".join(normalized) if normalized else cls.__name__ + "_Any"
        attrs = {"required_roles": normalized}
        return type(name, (cls,), attrs)

    def get_required_roles(self) -> Tuple[str, ...]:
        return tuple(self.required_roles)

    def get_fail_redirect(self):
        return resolve_url(self.fail_redirect)

    def _has_role(self, user) -> bool:
        if not user:
            return False
        required = self.get_required_roles()
        if not required:
            return True
        user_role = getattr(user, "role", None)
        if user_role in required:
            return True
        return False

    def handle_no_permission(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return HttpResponseRedirect(self.get_fail_redirect())

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        if not self._has_role(request.user):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)




