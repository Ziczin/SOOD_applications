from rest_framework import serializers
from apps.forms.models import FormField, Form, Field

class FormFieldSerializer(serializers.ModelSerializer):
    form = serializers.PrimaryKeyRelatedField(queryset=Form.objects.all())
    field = serializers.PrimaryKeyRelatedField(queryset=Field.objects.all())

    class Meta:
        model = FormField
        fields = ("id", "form", "field", "order")

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = [
            "id",
            "form_name",
            "department",
            "page_label",
            "form_label",
            "confirm_button_text",
            "sub_button_link_text",
            "sub_button_link_route",
            "available",
            "visible",
        ]
        read_only_fields = ["id"]
