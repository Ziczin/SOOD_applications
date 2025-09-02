from django.urls import path
from apps.api.views.users import (
    RegisterView, LoginView, LogoutView,
    UsersAPIView, RolesAPIView,
    CurrentUserAPIView, CurrentUserRoleAPIView,
    DepartmentAPIView
)
from apps.api.views.forms import FormListView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('users/', UsersAPIView.as_view(), name='api-users-list'),
    path('me/', CurrentUserAPIView.as_view(), name='api-current-user'),
    path('roles/', RolesAPIView.as_view(), name='api-roles'),
    path('roles/<str:username>/', RolesAPIView.as_view(), name='api-roles-list'),
    path('departments/', DepartmentAPIView.as_view(), name='api-departments'),
    path('departments/<str:username>/', DepartmentAPIView.as_view(), name='api-departments-list'),
    path('my-role/', CurrentUserRoleAPIView.as_view(), name='api-current-user-role'),
]
