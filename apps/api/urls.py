from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.api.views.users import UsersViewSet
from apps.api.views.roles import RoleListView
from apps.api.views.enums import EnumTagViewSet, EnumViewSet
from apps.api.views.forms import FormFieldViewSet, FormViewSet
from apps.api.views.events import EventCheckView
from apps.api.views.report import ReportXlsxView
from apps.api.views.departments import DepartmentViewSet

from apps.api.views.auth import (
    RegisterView,
    LoginView,
    LogoutView,
    CurrentUserAPIView,
    csrf_token_view
)
from apps.api.views.fields import (
    FieldViewSet,
    FieldTypeViewSet,
    FieldCharSetViewSet,
)
from apps.api.views.applications import (
    ApplicationAPIView,
    ApplicationRetrieveUpdateAPIView,
    ApplicationStatusListAPIView,
    ApplicationStatusUpdateAPIView,
)

CRUD = {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}
RU = {'get': 'list', 'post': 'create'}

enumtag_list = EnumTagViewSet.as_view(RU)
enumtag_detail = EnumTagViewSet.as_view(CRUD)
enumtag_items = EnumTagViewSet.as_view({'get': 'items'})

enums_list = EnumViewSet.as_view(RU)
enums_detail = EnumViewSet.as_view(CRUD)
enumtag_all = EnumTagViewSet.as_view({'get': 'all'})

router = DefaultRouter()

# Регистрируем ViewSets в роутере
router.register(r'users', UsersViewSet, basename='users')
router.register(r'departments', DepartmentViewSet, basename='departments')
router.register(r'fields', FieldViewSet, basename='fields')
router.register(r'forms', FormViewSet, basename='forms')
router.register(r'field-types', FieldTypeViewSet, basename='field-types')
router.register(r'form-fields', FormFieldViewSet, basename='form-fields')
router.register(r'field-charsets', FieldCharSetViewSet, basename='field-charset')

urlpatterns = [
    # Enum endpoints
    path('enum-tags/', enumtag_list, name='enum-tags-list'),
    path('enum-tags/<int:pk>/', enumtag_detail, name='enum-tags-detail'),
    path('enum-tags/<int:pk>/items/', enumtag_items, name='enum-tags-items'),
    path('enum-tags/history/', EnumTagViewSet.as_view({'get': 'history_list'}), name='enum-tags-history'),
    path('enum-tags/history/<int:pk>/', EnumTagViewSet.as_view({'get': 'history_detail'}), name='enum-tags-history-detail'),
    path('enums/', enums_list, name='enums-list'),
    path('enums/<int:pk>/', enums_detail, name='enums-detail'),
    
    # Auth endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('me/', CurrentUserAPIView.as_view(), name='current-user'),
    path('csrf-token/', csrf_token_view, name='csrf-token'),
    
    # Roles endpoint (RoleListView - это APIView, не ViewSet)
    path('roles/', RoleListView.as_view(), name='roles-list'),
    
    # Applications endpoints
    path('applications/', ApplicationAPIView.as_view(), name='applications'),
    path('applications/<int:id>/', ApplicationRetrieveUpdateAPIView.as_view(), name='application-detail'),
    path('application-statuses/', ApplicationStatusListAPIView.as_view(), name='application-statuses'),
    path('applications/<int:id>/status/', ApplicationStatusUpdateAPIView.as_view(), name='application-status-update'),
    
    # Report endpoint
    path('report/', ReportXlsxView.as_view(), name='report'),
    
    # Events endpoints
    path('events/check/', EventCheckView.as_view(), name='check'),
    
    # Router URLs (должен быть последним)
    path('', include(router.urls)),
]