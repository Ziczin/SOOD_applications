from django.contrib import admin
from .models import Application, ApplicationFormField


models_list = [
    Application, ApplicationFormField,
]

admin.site.register(models_list)
