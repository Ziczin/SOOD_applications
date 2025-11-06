from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class UserRole(models.TextChoices):
    USER = 'Пользователь'
    MODERATOR = 'Исполнитель'
    ADMIN = 'Руководитель'

class Department(models.Model):
    name = models.CharField(max_length=127)

    def __str__(self):
        return self.name

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

    class Meta:
        indexes = [
            models.Index(fields=['department']),
        ]

    def __str__(self):
        return self.username

from django.db import models
from django.utils import timezone
from django.conf import settings

class EventSubscriber(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.CharField(max_length=255)
    response = models.TextField(null=True, blank=True)
    last_check = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'event']),
            models.Index(fields=['last_check']),
        ]

