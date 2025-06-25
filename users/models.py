from django.contrib.auth.models import AbstractUser
from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    department = models.CharField(max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.full_name or self.username
