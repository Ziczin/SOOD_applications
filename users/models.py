from django.db import models
from django.contrib.auth.models import AbstractUser
 
class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

