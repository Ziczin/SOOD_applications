from django.contrib import admin
from .models import Application, ApplicationField, ApplicationService
from .models import Enum, EnumTag
from .models import Field, FieldType, Form
from .models import Model, ParentForm, Style
from .models import Service, ServiceValue

models_list = [
    Application, ApplicationField, ApplicationService,
    Enum, EnumTag,
    Field, FieldType, Form,
    Model, ParentForm, Style,
    Service, ServiceValue,
]

admin.site.register(models_list)
