from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('kitchen', 'Kitchen'),
    )
    
    department = models.CharField(max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.full_name or self.username
