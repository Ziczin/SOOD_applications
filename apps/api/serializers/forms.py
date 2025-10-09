from rest_framework import serializers
from apps.forms.models import FormField, Form, Field, FieldType, EnumTag


class FieldTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldType
        fields = ("label",)

class EnumTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnumTag
        fields = ("name", )

class FieldSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="type.label", read_only=True)
    tag = serializers.CharField(source="tag.name", read_only=True)
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
        fields = [
            "id",
            "department",
            "label",
            "confirm_button_text",
            "available",
            "visible",
        ]
        read_only_fields = ["id"]
