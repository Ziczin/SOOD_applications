from django.contrib import admin

from apps.forms.models import Enum, EnumTag, Form, Field, FieldCharSet, FieldType

models_list = [Enum, EnumTag, Field, Form, FieldCharSet, FieldType]

admin.site.register(models_list)
