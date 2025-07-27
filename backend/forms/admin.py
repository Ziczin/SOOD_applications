from django.contrib import admin

from forms.models import Enum, EnumTag, FieldType

models_list = [
    Enum, EnumTag, FieldType,
]

admin.site.register(models_list)
