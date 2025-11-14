import string

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
    type = models.CharField(max_length=10, blank=True)

class Field(models.Model):
    def __str__(self): return str(self.type) + ' | ' + str(self.label)
    type = models.ForeignKey(FieldType, on_delete=models.SET_NULL, null=True)
    label = models.CharField(max_length=50)
    placeholder = models.CharField(max_length=100, blank=True, default='')
    tag = models.ForeignKey(EnumTag, on_delete=models.SET_NULL, null=True, default=None)
    charset = models.ForeignKey('FieldCharSet', on_delete=models.SET_NULL, null=True, blank=True, default=None, related_name='fields')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, default=None)
    required = models.BooleanField(default=False)
    
    class Meta:
        indexes = [
            models.Index(fields=['department']),
            models.Index(fields=['type']),
        ]

class Form(models.Model):
    def __str__(self): return self.label
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    label = models.CharField(max_length=100, blank=True, default='')
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
    available = models.BooleanField(default=True)

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

class FieldCharSet(models.Model):
    def __str__(self): return ' | '.join([self.label, self.build_charset_repr(), self.build_charset()])
    label = models.CharField(max_length=200, blank=True)
    cyrillic_lower = models.BooleanField(default=False)
    cyrillic_upper = models.BooleanField(default=False)
    latin_lower = models.BooleanField(default=False)
    latin_upper = models.BooleanField(default=False)
    space = models.BooleanField(default=False)
    digits = models.BooleanField(default=False)
    special = models.BooleanField(default=False)
    included = models.TextField(blank=True)
    excluded = models.TextField(blank=True)
    min_length = models.PositiveIntegerField(null=True, blank=True)
    max_length = models.PositiveIntegerField(null=True, blank=True)
    available = models.BooleanField(default=True)
    visible = models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='field_charsets')
    shared = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['department', 'available']),
            models.Index(fields=['available', 'visible']),
            models.Index(fields=['shared', 'available']),
        ]

    def build_charset(self):
        parts = []
        if self.cyrillic_lower: parts.append('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        if self.cyrillic_upper: parts.append('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
        if self.latin_lower:  parts.append(string.ascii_lowercase)
        if self.latin_upper: parts.append(string.ascii_uppercase)
        if self.space: parts.append(' ')
        if self.digits: parts.append(string.digits)
        if self.special: parts.append(string.punctuation)
        if self.included: parts.append(self.included)
        combined = ''.join(parts)
        if self.excluded:
            excluded_set = set(self.excluded)
            combined = ''.join(ch for ch in combined if ch not in excluded_set)
        return combined
    
    def build_charset_repr(self):
        parts = []
        if self.cyrillic_lower: parts.append('кириллица')
        if self.cyrillic_upper: parts.append('КИРИЛЛИЦА')
        if self.latin_lower:  parts.append('latin')
        if self.latin_upper: parts.append('LATIN')
        if self.space: parts.append('пробел')
        if self.digits: parts.append("цифры")
        if self.special: parts.append("спецсимволы")
        if self.included: parts.append(f"включая: `{self.included}`")
        if self.excluded: parts.append(f"исключая: `{self.excluded}`")
        return ', '.join(parts)
