from rest_framework import serializers
from apps.forms.models import EnumTag, Enum

class EnumSerializer(serializers.ModelSerializer):
    value = serializers.CharField(allow_blank=True, allow_null=True, required=False)

    class Meta:
        model = Enum
        fields = ('id', 'value', 'available', 'visible', 'enum_tag')
        read_only_fields = ('id',)

    def validate_value(self, value):
        if value is None:
            return ''
        return value.strip()

    def create(self, validated_data):
        validated_data['value'] = validated_data.get('value', '')
        validated_data.setdefault('available', True)
        validated_data.setdefault('visible', True)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'value' in validated_data:
            validated_data['value'] = validated_data.get('value') or ''
        else:
            validated_data.pop('value', None)
        validated_data.setdefault('available', instance.available)
        validated_data.setdefault('visible', instance.visible)
        return super().update(instance, validated_data)


class EnumTagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(allow_blank=True, allow_null=True, required=False)

    class Meta:
        model = EnumTag
        fields = ('id', 'name', 'shared', 'available', 'department', 'visible')
        read_only_fields = ('id',)

    def validate_name(self, value):
        if value is None:
            return ''
        return value.strip()

    def create(self, validated_data):
        validated_data['name'] = validated_data.get('name', '')
        validated_data.setdefault('shared', False)
        validated_data.setdefault('visible', True)
        validated_data.setdefault('available', True)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['name'] = validated_data.get('name') or ''
        else:
            validated_data.pop('name', None)
        validated_data.setdefault('shared', instance.shared)
        validated_data.setdefault('visible', instance.visible)
        validated_data.setdefault('available', instance.available)
        return super().update(instance, validated_data)
