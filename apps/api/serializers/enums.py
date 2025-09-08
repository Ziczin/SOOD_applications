from rest_framework import serializers
from apps.forms.models import EnumTag, Enum

class EnumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enum
        fields = ('id', 'value', 'available', 'visible', 'enum_tag')
        read_only_fields = ('id',)

    def validate_value(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("value cannot be empty")
        return value.strip()

    def create(self, validated_data):
        validated_data.setdefault('available', True)
        validated_data.setdefault('visible', True)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.setdefault('available', instance.available)
        validated_data.setdefault('visible', instance.visible)
        return super().update(instance, validated_data)

class EnumTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnumTag
        fields = ('id', 'name', 'shared', 'available', 'department')
        read_only_fields = ('id',)

    def validate_name(self, name):
        if not name or not name.strip():
            raise serializers.ValidationError("name cannot be empty")
        return name.strip()

    def create(self, validated_data):
        validated_data.setdefault('shared', False)
        validated_data.setdefault('available', True)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.setdefault('shared', instance.shared)
        validated_data.setdefault('available', instance.available)
        return super().update(instance, validated_data)