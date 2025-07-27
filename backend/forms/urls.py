from django.urls import path
from .views import form_creation, field_creation, field_type_creation
from .views import enum_elem_creation, enum_tag_creation
from .views import get_form_data

urlpatterns = [
    path('form-creation/', form_creation, name='form-creation'),
    path('field-creation/', field_creation, name='field-creation'),
    path('field-type-creation/', field_type_creation, name='field-type-creation'),
    path('enum-elem-creation/', enum_elem_creation, name='enum-elem-creation'),
    path('enum-tag-creation/', enum_tag_creation, name='enum-tag-creation'),
    path('get-form-data/', get_form_data, name='get-form-data'),
]

