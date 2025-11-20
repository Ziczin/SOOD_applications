from django.db import models
from apps.users.models import CustomUser
from apps.forms.models import Form, FormField

class ApplicationStatus(models.TextChoices):
    SENDED = "SENDED", "Отправлена"
    IN_PROGRESS = "IN_PROGRESS", "В работе"
    COMPLETED = "COMPLETED", "Выполнена"
    CANCELLED = "CANCELLED", "Отменена отправителем"
    REJECTED = "REJECTED", "Отклонена исполнителем"

class Application(models.Model):
    def __str__(self): return str(self.form) + ' | ' + str(self.user)
    form = models.ForeignKey(Form, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    executor = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        default=None, related_name='executor')
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=32,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.SENDED,
    )
    last_status_change = models.DateTimeField(auto_now_add=True)
    msg = models.CharField(max_length=600, blank=True, default='')

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['-date']),
            models.Index(fields=['user', '-date']),
            models.Index(fields=['executor', 'status']),
            models.Index(fields=['form', '-date']),
        ]

class ApplicationStatusLog(models.Model):
    def __str__(self): return str(self.application) + ' | ' + str(self.status) + ' | ' + str(self.date)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='application_status_log')
    previous_status = models.CharField(
        max_length=32,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.SENDED
    )
    status = models.CharField(
        max_length=32,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.SENDED
    )
    date = models.DateTimeField(auto_now_add=True)
    who = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

class ApplicationFormField(models.Model):
    def __str__(self): return str(self.application) + ' | ' + str(self.form_field.outer_str()) + ' | ' + str(self.value)
    application = models.ForeignKey(
        Application, on_delete=models.SET_NULL, related_name='application_fields', null=True)
    form_field = models.ForeignKey(FormField, on_delete=models.SET_NULL, null=True)
    value = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['application']),
            models.Index(fields=['application', 'form_field']),
        ]