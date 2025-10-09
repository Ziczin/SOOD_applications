from django.contrib import admin
from .models import Field, Form


models_list = [
    Field, Form,
]

admin.site.register(models_list)
