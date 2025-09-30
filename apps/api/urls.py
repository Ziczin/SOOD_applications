from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.api.views.users import (
    RegisterView, LoginView, LogoutView,
    UsersViewSet, CurrentUserAPIView,
    DepartmentViewSet, RoleListView,
)
from apps.api.views.enums import EnumTagViewSet, EnumViewSet
from apps.api.views.fields import FieldViewSet, FieldTypeViewSet
from apps.api.views.forms import FormFieldViewSet, FormViewSet
from apps.api.views.auth import csrf_token_view

CRUD = {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}
RU = {'get': 'list', 'post': 'create'}

enumtag_list = EnumTagViewSet.as_view(RU)
enumtag_detail = EnumTagViewSet.as_view(CRUD)

enumtag_items = EnumTagViewSet.as_view({'get': 'items'})

enums_list = EnumViewSet.as_view(RU)
enums_detail = EnumViewSet.as_view(CRUD)
enumtag_all = EnumTagViewSet.as_view({'get': 'all'})

router = DefaultRouter()

for viewset in [
    [r'users', UsersViewSet],
    [r'roles', RoleListView],
    [r'fields', FieldViewSet],
    [r'forms', FormViewSet],
    [r'departments', DepartmentViewSet, 'departmento'],
    [r'field-types', FieldTypeViewSet],
    [r'form-fields', FormFieldViewSet],
]:
    router.register(*viewset)

urlpatterns = [path(*path_) for path_ in [
    ['enum-tags/', enumtag_list],
    ['enum-tags/<int:pk>/', enumtag_detail],
    ['enum-tags/<int:pk>/items/', enumtag_items],
    ['enum-tags/history/', EnumTagViewSet.as_view({'get': 'history_list'})],
    ['enum-tags/history/<int:pk>/', EnumTagViewSet.as_view({'get': 'history_detail'})],
    ['enums/', enums_list],
    ['enums/<int:pk>/', enums_detail],
    ['auth/register/', RegisterView.as_view()],
    ['auth/login/', LoginView.as_view()],
    ['auth/logout/', LogoutView.as_view()],
    ['me/', CurrentUserAPIView.as_view()],
    ['csrf-token/', csrf_token_view],
    ['', include(router.urls)],
]]