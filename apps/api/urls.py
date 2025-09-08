from django.urls import path
from apps.api.views.users import (
    RegisterView, LoginView, LogoutView,
    UsersAPIView, RolesAPIView,
    CurrentUserAPIView, CurrentUserRoleAPIView,
    DepartmentAPIView
)
from django.urls import path
from apps.api.views.enums import EnumTagViewSet, EnumViewSet

enumtag_list = EnumTagViewSet.as_view({
    'get': 'list', 'post': 'create'
})
enumtag_detail = EnumTagViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
enums_list = EnumViewSet.as_view({
    'get': 'list', 'post': 'create'
})
enums_detail = EnumViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
enumtag_items_list = EnumTagViewSet.as_view({
    'get': 'items_list',
    'post': 'items_create'
})
enumtag_item_detail = EnumTagViewSet.as_view({
    'get': 'item_detail',
    'put': 'item_detail',
    'patch': 'item_detail',
    'delete': 'item_detail'
})

urlpatterns = [
    path('enum-tags/', enumtag_list, name='enumtag-list'),
    path('enum-tags/<int:pk>/', enumtag_detail, name='enumtag-detail'),
    path('enums/', enums_list, name='enum-list'),
    path('enums/<int:pk>/', enums_detail, name='enum-detail'),
    path('enum-tags/<int:pk>/items/', enumtag_items_list, name='enumtag-items-list'),
    path('enum-tags/<int:pk>/items/<int:item_pk>/', enumtag_item_detail, name='enumtag-item-detail'),
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
