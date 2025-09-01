# protector.py
from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from typing import Callable

def protected_api_view(cls):
    """
    Оборачивает dispatch и выполняет:
    - все проверки из _required_checks_all (AND)
    - хотя бы одну проверку из _required_checks_any (OR)
    Если ни одного типа меток нет — пропускает.
    Проверки — callables: (request, view, *args, **kwargs) -> bool | (bool, Response)
    """
    original_dispatch = cls.dispatch

    @wraps(original_dispatch)
    def wrapped_dispatch(self, request, *args, **kwargs):
        handler = getattr(self, request.method.lower(), None)
        if handler is not None:
            all_checks = getattr(handler, "_required_checks_all", [])
            for chk in all_checks:
                if not callable(chk):
                    return Response({"detail": f"Invalid check: {repr(chk)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                result = chk(request, self, *args, **kwargs)
                if isinstance(result, tuple):
                    allowed, resp = result
                    if not allowed:
                        return resp
                else:
                    if not result:
                        return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

            any_checks = getattr(handler, "_required_checks_any", [])
            if any_checks:
                any_ok = False
                any_resp = None
                for chk in any_checks:
                    if not callable(chk):
                        return Response({"detail": f"Invalid check: {repr(chk)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    result = chk(request, self, *args, **kwargs)
                    if isinstance(result, tuple):
                        allowed, resp = result
                        if allowed:
                            any_ok = True
                            break
                        else:
                            any_resp = any_resp or resp
                    else:
                        if result:
                            any_ok = True
                            break
                if not any_ok:
                    return any_resp or Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        return original_dispatch(self, request, *args, **kwargs)

    cls.dispatch = wrapped_dispatch
    return cls

def reqall(*checks: Callable):
    """Требует пройти все проверки (AND)."""
    def decorator(func):
        if not hasattr(func, "_required_checks_all"):
            func._required_checks_all = []
        func._required_checks_all.extend(checks)
        return func
    return decorator

def reqany(*checks: Callable):
    """Требует пройти любую из проверок (OR)."""
    def decorator(func):
        if not hasattr(func, "_required_checks_any"):
            func._required_checks_any = []
        func._required_checks_any.extend(checks)
        return func
    return decorator
