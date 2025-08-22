from rest_framework import serializers
from .models import (
    Application,
    ApplicationField,
    ApplicationService,
)
from apps.users.serializers import UserSerializer
from apps.forms.serializers import FormSerializer, FieldSerializer, ServiceSerializer

class ApplicationFieldSerializer(serializers.ModelSerializer):
    field = FieldSerializer(read_only=True)

    class Meta:
        model = ApplicationField
        fields = ('id', 'field', 'value')

class ApplicationServiceSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = ApplicationService
        fields = ('id', 'service')

class ApplicationSerializer(serializers.ModelSerializer):
    form = FormSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    fields = ApplicationFieldSerializer(
        source='applicationfield_set', many=True, read_only=True
    )
    services = ApplicationServiceSerializer(
        source='applicationservice_set', many=True, read_only=True
    )

    class Meta:
        model = Application
        fields = (
            'id',
            'form',
            'user',
            'fields',
            'services',
        )
