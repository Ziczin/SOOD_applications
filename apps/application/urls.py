from django.urls import path
from .views import (
    DashboardView,
    FormManagerView,
    EnumsManagerView,
    UsersManagerView,
    FieldsManagerView,
    CharsetManagerView,
    DepartmentsManagerView,
    StuffManagerView,
)

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("forms-manager/", FormManagerView.as_view(), name="forms-manager"),
    path("enums-manager/", EnumsManagerView.as_view(), name="enums-manager"),
    path("charsets-manager/", CharsetManagerView.as_view(), name="charsets-manager"),
    path("users-manager/", UsersManagerView.as_view(), name="users-manager"),
    path("fields-manager/", FieldsManagerView.as_view(), name="fields-manager"),
    path("departments-manager/", DepartmentsManagerView.as_view(), name="deaprtments-manager"),
    path("stuff-manager/", StuffManagerView.as_view(), name="stuff-manager"),
]
