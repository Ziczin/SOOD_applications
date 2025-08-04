from django.contrib import admin
from .models import Application, ApplicationField, ApplicationService
from .models import Field, Form


models_list = [
    Application, ApplicationField, ApplicationService,
    Field, Form,
]

admin.site.register(models_list)
