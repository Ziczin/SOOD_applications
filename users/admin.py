from django.contrib import admin
from .models import CustomUser, Department

models_list = [
    CustomUser, Department
]

admin.site.register(models_list)
