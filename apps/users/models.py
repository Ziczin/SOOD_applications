import threading
import time
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class UserRole(models.TextChoices):
    USER = "Пользователь"
    MODERATOR = "Исполнитель"
    ADMIN = "Руководитель"


class Department(models.Model):
    name = models.CharField(max_length=127)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=100, blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER,
    )
    verified = models.BooleanField(default=False)
    proxy = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["department"]),
        ]

    def __str__(self):
        return self.username


class EventSubscriber(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.CharField(max_length=255)
    response = models.TextField(null=True, blank=True)
    other = models.BigIntegerField(null=True, blank=True)
    last_check = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=["user", "event"]),
            models.Index(fields=["last_check"]),
        ]


def cleanup_old_subscribers():
    cutoff_time = timezone.now() - timedelta(minutes=10)
    return EventSubscriber.objects.filter(last_check__lt=cutoff_time).delete()[0]


def start_cleanup_scheduler():
    def scheduler():
        while True:
            time.sleep(600)
            cleanup_old_subscribers()

    thread = threading.Thread(target=scheduler, daemon=True)
    thread.start()


start_cleanup_scheduler()
