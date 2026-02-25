from rest_framework.permissions import BasePermission, AllowAny
from apps.api.core.get_permissions import get_permissions
import re

ALIAS_METHODS = {
    "r": "get",
    "3p": "post patch put",
    "pppd": "post patch put delete",
    "ppp": "post patch put",
    "del": "delete",
    "all": "get post patch put delete head options trace",
    "read": "get head options",
    "g3p": "get post patch put",
    "r3p": "get post patch put",
    "gppp": "get post patch put",
    "rppp": "get post patch put",
    **{a: a for a in "get post patch put delete head options trace".split()},
}


def _expand_method_keys(key):
    keys = key.replace(",", " ").split(" ")
    res = set()
    for key in keys:
        res.update(ALIAS_METHODS[key].upper().split())
    return res


def parse(rules):
    if ":" not in rules:
        return {"*": [rules]}
    result = {}
    for part in rules.split(";"):
        method_key, roles_part = part.split(":", 1)
        for expanded_method in _expand_method_keys(method_key):
            if not result.get(expanded_method):
                result[expanded_method] = set()
            result[expanded_method].update(roles_part.split(","))
    return result


def user_has_role(user, role_name):
    return getattr(user, "is_authenticated", False) and role_name in set(
        get_permissions(user) or []
    )


def make_permission_class(*roles):
    class_name = "RequireRoles_" + "_".join(roles)

    def has_permission(self, request, view, *a):
        if not getattr(request.user, "is_authenticated", False):
            return False
        return any(user_has_role(request.user, role) for role in roles)

    attrs = {
        "has_permission": has_permission,
        "has_object_permission": has_permission,
    }
    return type(class_name, (BasePermission,), attrs)


def permissions(*rules):
    rules = ";".join(rules)
    rules = re.sub(r";+", ";", rules)
    normalized = re.sub(r"\s+", "", rules).rstrip(";")
    parsed_rules = parse(normalized)
    permission_factories = {}
    for method_key, role_list in parsed_rules.items():
        permission_factories[method_key] = make_permission_class(*role_list)

    def decorator(view_class):
        original_get_permissions = getattr(view_class, "get_permissions", None)
        original_permission_classes = getattr(view_class, "permission_classes", None)

        def get_permissions(self):
            selected_key = None
            http_method = getattr(self.request, "method", None)
            if http_method and http_method.upper() in permission_factories:
                selected_key = http_method.upper()
            elif "*" in permission_factories:
                selected_key = "*"
            if selected_key:
                return [permission_factories[selected_key]()]
            if original_get_permissions:
                return original_get_permissions(self)
            if original_permission_classes:
                return [
                    permission_class()
                    for permission_class in original_permission_classes
                ]
            return [AllowAny()]

        setattr(view_class, "get_permissions", get_permissions)
        setattr(view_class, "required_roles_raw", parsed_rules)
        return view_class

    return decorator
