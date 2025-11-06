from django.db import models
from apps.users.models import Department
from django.core.validators import MinValueValidator

class EnumTag(models.Model):
    def __str__(self): return self.name
    name = models.CharField(max_length=50, default='', blank=True)
    shared = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='enum_tags')
    
    class Meta:
        indexes = [
            models.Index(fields=['department', 'available']),
            models.Index(fields=['available', 'visible']),
        ]

class Enum(models.Model):
    def __str__(self): return str(self.enum_tag) + ' | ' + str(self.value) 
    value = models.CharField(max_length=50, default='', blank=True)
    enum_tag = models.ForeignKey(EnumTag, on_delete=models.SET_NULL, null=True)
    available = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['enum_tag', 'available']),
            models.Index(fields=['available', 'visible']),
        ]

class FieldType(models.Model):
    def __str__(self): return self.name
    name = models.CharField(max_length=50)
    label = models.CharField(max_length=100)
    allow_tags = models.BooleanField(default=False)

class Field(models.Model):
    def __str__(self): return str(self.type) + ' | ' + str(self.label)
    type = models.ForeignKey(FieldType, on_delete=models.SET_NULL, null=True)
    label = models.CharField(max_length=50)
    tag = models.ForeignKey(EnumTag, on_delete=models.SET_NULL, null=True, default=None)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, default=None)
    
    class Meta:
        indexes = [
            models.Index(fields=['department']),
            models.Index(fields=['type']),
        ]

class Form(models.Model):
    def __str__(self): return self.label
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    label = models.CharField(max_length=100, blank=True, default='')
    confirm_button_text = models.CharField(max_length=100, blank=True, default='')
    available = models.BooleanField(default=True)
    visible = models.BooleanField(default=False)
    
    class Meta:
        indexes = [
            models.Index(fields=['department']),
            models.Index(fields=['department', 'available']),
            models.Index(fields=['available', 'visible']),
        ]

class FormField(models.Model):
    def __str__(self): return f"{self.form} | {self.field} ({self.order})"
    def outer_str(self): return f"{self.form} | {self.field}"
    form = models.ForeignKey('Form', on_delete=models.CASCADE, related_name='form_fields')
    field = models.ForeignKey('Field', on_delete=models.CASCADE, related_name='field_forms')
    order = models.PositiveIntegerField(validators=[MinValueValidator(1)], null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['form', '-order']),
            models.Index(fields=['field', 'form']),
        ]

    def save(self, *args, **kwargs):
        if self.pk is None and (self.order is None):
            super().save(*args, **kwargs)
            FormField.objects.filter(pk=self.pk).update(order=self.pk)
            self.refresh_from_db(fields=['order'])
            return
        super().save(*args, **kwargs)