from django.contrib import admin
from .models import CustomUser, Department

models_list = [
    CustomUser, Department
]

admin.site.register(models_list)

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

models_list = [
    Group,
    Site,
]

admin.site.unregister(models_list)
