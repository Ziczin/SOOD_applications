from django.db import models
from users.models import Department

class Form(models.Model):
    def __str__(self): return self.form_name
    form_name = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
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
