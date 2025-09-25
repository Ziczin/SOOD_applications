from django.urls import path
from .views import get_form_data, get_forms_by_user_department

urlpatterns = [
    path('get-form-data/', get_form_data, name='get-form-data'),
    path('api/forms/', get_forms_by_user_department, name='get_forms_by_user_department'), # type: ignore
]

