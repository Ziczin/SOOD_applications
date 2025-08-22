from functools import wraps
from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required as django_login_required

def protected_api_view(cls):
    cls.permissions_dict = {}
    return cls

def protected_method(*permissions):
    def decorator(func):
        if not hasattr(func, 'permissions_dict'):
            raise ValueError("The class must be decorated with @protected_api_view")

        method_name = func.__name__
        
        if method_name not in func.permissions_dict:
            func.permissions_dict[method_name] = list(permissions)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
    
    return decorator

def login_required(func):
    return protected_method('IsAuthenticated')(func)

def role_required(role, redir='/applications/dashboard/'):
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
