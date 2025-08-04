from django.urls import path
from .views import form_creation, field_creation, field_type_creation
from .views import enum_elem_creation, enum_tag_creation
from .views import get_form_data, get_forms_by_user_department

urlpatterns = [
    path('form-creation/', form_creation, name='form-creation'),
    path('field-creation/', field_creation, name='field-creation'), # type: ignore
    path('field-type-creation/', field_type_creation, name='field-type-creation'), # type: ignore
    path('enum-elem-creation/', enum_elem_creation, name='enum-elem-creation'), # type: ignore
    path('enum-tag-creation/', enum_tag_creation, name='enum-tag-creation'), # type: ignore
    path('get-form-data/', get_form_data, name='get-form-data'),
    path('api/forms/', get_forms_by_user_department, name='get_forms_by_user_department'), # type: ignore
]

