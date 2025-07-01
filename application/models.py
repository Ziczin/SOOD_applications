from django.db import models
from users.models import Department, CustomUser

class Style(models.Model):
    def __str__(self): return self.name
    name = models.CharField(max_length=50)
    path = models.CharField(max_length=100)

class Model(models.Model):
    def __str__(self): return self.name
    name = models.CharField(max_length=50)

class ParentForm(models.Model):
    def __str__(self): return self.name
    name = models.CharField(max_length=50)

class Form(models.Model):
    def __str__(self): return self.form_name
    form_name = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey(Model, on_delete=models.SET_NULL, null=True)
    parent_form = models.ForeignKey(ParentForm, on_delete=models.SET_NULL, null=True)
    page_label = models.CharField(max_length=100)
    form_label = models.CharField(max_length=100)
    confirm_button_text = models.CharField(max_length=100)
    sub_button_link_text = models.CharField(max_length=100)
    sub_button_link_route = models.CharField(max_length=100)

class FieldType(models.Model):
    def __str__(self): return self.name
    name = models.CharField(max_length=50)

class EnumTag(models.Model):
    def __str__(self): return self.name
    name = models.CharField(max_length=50)

class Enum(models.Model):
    def __str__(self): return str(self.enum_tag) + ' | ' + str(self.value) 
    value = models.CharField(max_length=50)
    enum_tag = models.ForeignKey(EnumTag, on_delete=models.SET_NULL, null=True)

class Field(models.Model):
    def __str__(self): return str(self.field_type) + ' | ' + str(self.label)
    form = models.ForeignKey(Form, on_delete=models.SET_NULL, null=True, default=None)
    field_type = models.ForeignKey(FieldType, on_delete=models.SET_NULL, null=True)
    label = models.CharField(max_length=50)
    enum_tag = models.ForeignKey(EnumTag, on_delete=models.SET_NULL, null=True, default=None)

class Service(models.Model):
    def __str__(self): return self.name
    form = models.ForeignKey(Form, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

class ServiceValue(models.Model):
    def __str__(self): return self.label
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    label = models.CharField(max_length=50)
    value = models.FloatField()

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