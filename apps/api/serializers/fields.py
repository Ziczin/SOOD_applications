from rest_framework import serializers
from apps.forms.models import FieldType, Field, EnumTag

class FieldTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(allow_blank=True, allow_null=True, required=False)

    class Meta:
        model = FieldType
        fields = ('id', 'name', 'label')
        read_only_fields = ('id',)

    def validate_name(self, value):
        if value is None:
            return ''
        return value.strip()

    def create(self, validated_data):
        validated_data['name'] = validated_data.get('name', '')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['name'] = validated_data.get('name') or ''
        else:
            validated_data.pop('name', None)
        return super().update(instance, validated_data)

class FieldSerializer(serializers.ModelSerializer):
    label = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    # представляем type и tag как PK (совместимо с существующими сериализаторами Enum/EnumTag)
    type = serializers.PrimaryKeyRelatedField(queryset=FieldType.objects.all(), allow_null=True, required=False)
    tag = serializers.PrimaryKeyRelatedField(queryset=EnumTag.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Field
        fields = ('id', 'type', 'label', 'tag')
        read_only_fields = ('id',)

    def validate_label(self, value):
        if value is None:
            return ''
        return value.strip()

    def create(self, validated_data):
        validated_data['label'] = validated_data.get('label', '')
        # по модели type и tag могут быть null, поэтому оставляем как есть
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'label' in validated_data:
            validated_data['label'] = validated_data.get('label') or ''
        else:
            validated_data.pop('label', None)
        # сохраняем существующие type/tag, если не переданы
        validated_data.setdefault('type', instance.type)
        validated_data.setdefault('tag', instance.tag)
        return super().update(instance, validated_data)
