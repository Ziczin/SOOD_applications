from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.api.views.users import (
    RegisterView, LoginView, LogoutView,
    UsersViewSet, CurrentUserAPIView,
    DepartmentViewSet, RoleListView
)
from apps.api.views.enums import EnumTagViewSet, EnumViewSet

enumtag_list = EnumTagViewSet.as_view({'get': 'list', 'post': 'create'})
enumtag_detail = EnumTagViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})
enumtag_items_list = EnumTagViewSet.as_view({'get': 'items_list', 'post': 'items_create'})
enumtag_item_detail = EnumTagViewSet.as_view({'get': 'item_detail', 'put': 'item_detail', 'patch': 'item_detail', 'delete': 'item_detail'})

enums_list = EnumViewSet.as_view({'get': 'list', 'post': 'create'})
enums_detail = EnumViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='user')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'roles', RoleListView, basename='roles')

urlpatterns = [
    path('enum-tags/', enumtag_list, name='enumtag-list'),
    path('enum-tags/<int:pk>/', enumtag_detail, name='enumtag-detail'),
    path('enum-tags/<int:pk>/items/', enumtag_items_list, name='enumtag-items-list'),
    path('enum-tags/<int:pk>/items/<int:item_pk>/', enumtag_item_detail, name='enumtag-item-detail'),
    path('enums/', enums_list, name='enum-list'),
    path('enums/<int:pk>/', enums_detail, name='enum-detail'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('me/', CurrentUserAPIView.as_view(), name='me'),
    path('', include(router.urls)),
]
# Users routes (router-generated):
# GET  /users/                          — list пользователей; поддерживает фильтр ?department=<name>
# GET  /users/{username}/               — retrieve пользователя по username (детальная информация)
# PATCH /users/{username}/change_role/  — action change_role: частичное обновление роли
# PATCH /users/{username}/change_department/ — action change_department: частичное обновление department