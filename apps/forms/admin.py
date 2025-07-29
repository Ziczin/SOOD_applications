from django.contrib import admin

from apps.forms.models import Enum, EnumTag, FieldType

models_list = [
    Enum, EnumTag, FieldType,
]

admin.site.register(models_list)
