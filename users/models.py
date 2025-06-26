from django.db import models
from django.contrib.auth.models import AbstractUser

class RequiredModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.objects.get_or_create('CustomUser')

    def __str__(self):
        return self.name

class ParentForm(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.objects.get_or_create('UserCreationForm')
        self.objects.get_or_create('ModelForm')

    def __str__(self):
        return self.name
    
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

class FieldType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    additional = models.CharField(max_length=50, default=None)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.objects.get_or_create('String')
        self.objects.get_or_create('Text')
        self.objects.get_or_create('Password')

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.objects.get_or_create('Не прочитано')
        self.objects.get_or_create('Принято к исполнению')
        self.objects.get_or_create('Исполнено')
        self.objects.get_or_create('Отказано')
        self.objects.get_or_create('Отменено')

    def __str__(self):
        return self.name

class Form(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='forms')
    form_object_name = models.CharField(max_length=255)
    css = models.CharField(max_length=255)
    model = models.ForeignKey(RequiredModel, on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey(ParentForm, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    form_name = models.CharField(max_length=255)
    btn_confirm = models.CharField(max_length=255)
    sub_btn_link = models.CharField(max_length=255)
    sub_btn_link_text = models.CharField(max_length=255)

    def __str__(self):
        return self.form_name

class Field(models.Model):
    form = models.ForeignKey(Form, on_delete=models.SET_NULL, null=True, related_name='fields')
    field_id = models.CharField(max_length=255)
    field_type = models.ForeignKey(FieldType, on_delete=models.SET_NULL, null=True)
    label = models.CharField(max_length=255)
    placeholder = models.CharField(max_length=255)
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.label

class Service(models.Model):
    form = models.ForeignKey(Form, on_delete=models.SET_NULL, null=True, related_name='services')
    count = models.IntegerField()

    def __str__(self):
        return f"Service for {self.form.form_name}"

class ServiceAttribute(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='attributes')
    attribute_key = models.CharField(max_length=255)
    attribute_value = models.TextField()

    def __str__(self):
        return f"{self.attribute_key}: {self.attribute_value}"

class Application(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    form = models.ForeignKey(Form, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)  # Связь со статусом
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Application by {self.user.username} for {self.form.form_name}"

class ApplicationService(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='application_services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return f"{self.count} of {self.service} in {self.application}"
