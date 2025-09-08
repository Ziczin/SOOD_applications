from django.urls import path
from .views import (
    DashboardView,
    FormManagerView,
    DemoDashboardView,
    DemoFormManagerView,
    EnumsManager,
)
urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='old-dashboard'),
    path('form-manager/', FormManagerView.as_view(), name="old-form-manager"),
    path('demo-dashboard/', DemoDashboardView.as_view(), name="dashboard"),
    path('demo-form-manager/', DemoFormManagerView.as_view(), name="form-manager"),
    path('enums-manager/', EnumsManager.as_view(), name="enums-manager"),
]

