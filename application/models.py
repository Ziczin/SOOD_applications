from django.db import models

class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=50)
    data = models.JSONField()

    def __str__(self):
        return f"Service for {self.form.form_name}"

class Application(models.Model):
    data = models.JSONField()

