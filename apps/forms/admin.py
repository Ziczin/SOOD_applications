from django.contrib import admin

from apps.forms.models import Enum, EnumTag, Form, Field

models_list = [
    Enum, EnumTag, Field, Form,
    
]

admin.site.register(models_list)
