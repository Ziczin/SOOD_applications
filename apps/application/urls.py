from django.urls import path
from .views import (
    DashboardView,
    FormManagerView,
    DemoDashboardView,
    DemoFormManagerView,
    EnumsManagerView,
    UsersManagerView,
    FieldsManagerView
)
urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='old-dashboard'),
    path('form-manager/', FormManagerView.as_view(), name="old-form-manager"),
    path('demo-dashboard/', DemoDashboardView.as_view(), name="dashboard"),
    path('demo-form-manager/', DemoFormManagerView.as_view(), name="form-manager"),
    path('enums-manager/', EnumsManagerView.as_view(), name="enums-manager"),
    path('users-manager/', UsersManagerView.as_view(), name="users-manager"),
    path('fields-manager/', FieldsManagerView.as_view(), name="fields-manager"),
]

