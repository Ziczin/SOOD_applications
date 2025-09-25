from django.db import models
from apps.users.models import Department

class EnumTag(models.Model):
    def __str__(self): return self.name
    name = models.CharField(max_length=50, default='', blank=True)
    shared = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='enum_tags')

class Enum(models.Model):
    def __str__(self): return str(self.enum_tag) + ' | ' + str(self.value) 
    value = models.CharField(max_length=50, default='', blank=True)
    enum_tag = models.ForeignKey(EnumTag, on_delete=models.SET_NULL, null=True)
    available = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)

class FieldType(models.Model):
    def __str__(self): return self.name
    name = models.CharField(max_length=50)
    label = models.CharField(max_length=100)

class Field(models.Model):
    def __str__(self): return str(self.type) + ' | ' + str(self.label)
    type = models.ForeignKey(FieldType, on_delete=models.SET_NULL, null=True)
    label = models.CharField(max_length=50)
    tag = models.ForeignKey(EnumTag, on_delete=models.SET_NULL, null=True, default=None)

class Form(models.Model):
    def __str__(self): return self.form_name
    form_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    page_label = models.CharField(max_length=100)
    form_label = models.CharField(max_length=100)
    confirm_button_text = models.CharField(max_length=100)
    sub_button_link_text = models.CharField(max_length=100)
    sub_button_link_route = models.CharField(max_length=100)
    available = models.BooleanField(default=False)
    fields = models.ManyToManyField(Field, related_name='forms', blank=True)





class ServiceGroup(models.Model):
    def __str__(self): return str(self.form) + ' | ' + str(self.name)
    form = models.ForeignKey(Form, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    available = models.BooleanField(default=False)

class Service(models.Model):
    def __str__(self): return self.name
    group = models.ForeignKey(ServiceGroup, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    available = models.BooleanField(default=False)

class ServiceValue(models.Model):
    def __str__(self): return self.label
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    label = models.CharField(max_length=50)
    value = models.FloatField()