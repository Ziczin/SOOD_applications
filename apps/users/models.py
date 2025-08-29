from django.db import models
from django.contrib.auth.models import AbstractUser

class UserRole(models.TextChoices):
    USER = 'USER', 'Пользователь'
    MODERATOR = 'MODERATOR', 'Модератор'
    ADMIN = 'ADMIN', 'Администратор'

class Department(models.Model):
    name = models.CharField(max_length=63, unique=True)
    label = models.CharField(max_length=127)

    def __str__(self):
        return self.label

class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=100, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER,
    )
    verified = models.BooleanField(default=False)
    proxy = models.BooleanField(default=False)

    def __str__(self):
        return self.username

from django.db import models


