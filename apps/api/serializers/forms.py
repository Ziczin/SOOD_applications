from rest_framework import serializers
from apps.forms.models import FormField, Form, Field, FieldType, EnumTag

class FieldSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(slug_field='name', read_only=True)
    tag = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Field
        fields = ("id", "type", "label", "tag")


class FormFieldSerializer(serializers.ModelSerializer):
    form = serializers.PrimaryKeyRelatedField(queryset=Form.objects.all())
    field = FieldSerializer(read_only=True)
    field_id = serializers.PrimaryKeyRelatedField(source="field", queryset=Field.objects.all(), write_only=True)

    class Meta:
        model = FormField
        fields = ("id", "form", "field", "field_id", "order")


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = (
            "id",
            "department",
            "label",
            "available",
            "visible",
        )
        read_only_fields = ("id",)


class FormFieldWithEnumsSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=True)
    type = serializers.CharField(allow_null=True)
    label = serializers.CharField(allow_null=True)
    enums = serializers.ListField(child=serializers.DictField(), source='enums_list')

    def to_representation(self, instance):
        field_instance = getattr(instance, 'field', None)
        base = {
            'id': instance.id if field_instance else None,
            'type': getattr(getattr(field_instance, 'type', None), 'name', None) if field_instance else None,
            'label': getattr(field_instance, 'label', None) if field_instance else None,
        }
        tag_id = getattr(field_instance, 'tag_id', None) if field_instance else None
        enums_map = self.context.get('enums_map', {})
        base['enums'] = enums_map.get(tag_id, []) if tag_id else []
        return base