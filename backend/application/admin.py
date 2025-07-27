from django.contrib import admin
from .models import Application, ApplicationField, ApplicationService
from .models import Field, Form
from .models import Service, ServiceValue

models_list = [
    Application, ApplicationField, ApplicationService,
    Field, Form,
    Service, ServiceValue,
]

admin.site.register(models_list)
