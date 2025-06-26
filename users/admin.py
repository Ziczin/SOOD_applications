from django.contrib import admin
from .models import Application, ApplicationService, CustomUser, Department
from .models import Field, FieldType, Form, ParentForm, RequiredModel
from .models import Service, ServiceAttribute, Status

models_list = [
    Application, ApplicationService, CustomUser, Department,
    Field, FieldType, Form, ParentForm, RequiredModel,
    Service, ServiceAttribute, Status
]

admin.site.register(models_list)
