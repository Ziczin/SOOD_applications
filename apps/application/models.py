from django.db import models
from apps.users.models import CustomUser
from apps.forms.models import Form, Field, Service

class Application(models.Model):
    def __str__(self): return str(self.form) + ' | ' + str(self.user)
    form = models.ForeignKey(Form, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

class ApplicationField(models.Model):
    def __str__(self): return str(self.application) + ' | ' + str(self.field) + ' | ' + str(self.value)
    application = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True)
    field = models.ForeignKey(Field, on_delete=models.SET_NULL, null=True)
    value = models.CharField(max_length=100)

class ApplicationService(models.Model):
    def __str__(self): return str(self.application) + ' | ' + str(self.service)
    application = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
