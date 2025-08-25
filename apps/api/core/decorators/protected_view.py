from functools import wraps

def protected_method(*permissions):
    """
    Декоратор методов: сохраняет права на самой функции в атрибуте _method_permissions.
    Не выполняет проверок сразу — сбор прав происходит в protected_api_view.
    """
    def decorator(func):
        if not hasattr(func, '_method_permissions'):
            func._method_permissions = {}
        func._method_permissions[func.__name__] = list(permissions)
        return func
    return decorator

def protected_api_view(cls):
    """
    Декоратор класса: собирает все _method_permissions из методов (включая
    обычные методы, @classmethod и @staticmethod) и помещает их в cls.permissions_dict.
    """
    permissions = {}
    for name, member in cls.__dict__.items():
        func = None

        # обычный метод или функция в классе
        if hasattr(member, '_method_permissions'):
            func = member
        # classmethod хранится как classmethodobj.__func__
        elif isinstance(member, classmethod) and hasattr(member.__func__, '_method_permissions'):
            func = member.__func__
        # staticmethod хранится как staticmethodobj.__func__
        elif isinstance(member, staticmethod) and hasattr(member.__func__, '_method_permissions'):
            func = member.__func__

        if func:
            # func._method_permissions содержит mapping {method_name: [permissions]}
            # используем update, чтобы объединить все найденные записи
            permissions.update(func._method_permissions)

    cls.permissions_dict = permissions
    return cls

def login_required(func):
    return protected_method('IsAuthenticated')(func)

def role_required(role, redir='/applications/dashboard/'):
    """
    Вспомогательный декоратор для проверки роли на уровне вызова.
    Замечание: role_required возвращает декоратор, который использует
    django.contrib.auth.decorators.login_required (view-level) — в вашем коде
    возможно предпочтительнее проверять роль внутри функции/метода или
    использовать DRF permissions.
    """
    from django.contrib.auth.decorators import login_required as django_login_required
    from functools import wraps
    from django.shortcuts import redirect

    def decorator(func):
        @django_login_required
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if hasattr(request.user, 'role') and request.user.role == role:
                return func(request, *args, **kwargs)
            else:
                return redirect(redir)
        return wrapper
    return decorator
