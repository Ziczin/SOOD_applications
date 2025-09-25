from apps.users.models import UserRole

def get_permissions(user):
    permissions = []
    if user.verified:
        permissions.append('user')
        if user.role == UserRole.ADMIN:
            permissions.append('admin')
            permissions.append('moderator')
        if user.role == UserRole.MODERATOR:
            permissions.append('moderator')
    if user.proxy:
        permissions.append('proxy')
    return permissions