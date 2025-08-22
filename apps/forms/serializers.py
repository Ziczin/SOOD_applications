from rest_framework import serializers
from .models import (
    Form,
    FieldType,
    EnumTag,
    Enum,
    Field,
    ServiceGroup,
    Service,
    ServiceValue,
)

class FieldTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldType
        fields = ('id', 'name')

class EnumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enum
        fields = ('id', 'value')

class EnumTagSerializer(serializers.ModelSerializer):
    enums = EnumSerializer(source='enum_set', many=True, read_only=True)

    class Meta:
        model = EnumTag
        fields = ('id', 'name', 'available', 'enums')

class FieldSerializer(serializers.ModelSerializer):
    type = FieldTypeSerializer(read_only=True)
    enum_values = serializers.SerializerMethodField()

    class Meta:
        model = Field
        fields = ('id', 'label', 'type', 'enum_values')

    def get_enum_values(self, obj):
        if obj.enum_tag and obj.enum_tag.available:
            return EnumSerializer(
                obj.enum_tag.enum_set.filter(available=True), many=True
            ).data
        return []

class ServiceValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceValue
        fields = ('id', 'label', 'value')

class ServiceSerializer(serializers.ModelSerializer):
    values = ServiceValueSerializer(source='servicevalue_set', many=True)

    class Meta:
        model = Service
        fields = ('id', 'name', 'description', 'available', 'values')

class ServiceGroupSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(source='service_set', many=True)

    class Meta:
        model = ServiceGroup
        fields = ('id', 'name', 'available', 'services')

class FormSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source='department.name', allow_null=True)
    fields = FieldSerializer(source='field_set', many=True)
    service_groups = ServiceGroupSerializer(source='servicegroup_set', many=True)

    class Meta:
        model = Form
        fields = (
            'id',
            'form_name',
            'page_label',
            'form_label',
            'confirm_button_text',
            'sub_button_link_text',
            'sub_button_link_route',
            'available',
            'department',
            'fields',
            'service_groups',
        )
