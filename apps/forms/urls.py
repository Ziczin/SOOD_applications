from django.urls import path
from .views import get_forms_by_user_department

urlpatterns = [
    path(
        "api/forms/", get_forms_by_user_department, name="get_forms_by_user_department"
    ),  # type: ignore
]
