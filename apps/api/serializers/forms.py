from rest_framework import serializers
from apps.forms.models import FormField, Form, Field, FieldType, EnumTag

class FieldSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(slug_field='name', read_only=True)
    tag = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Field
        fields = ("id", "type", "label", "tag")


def build_humanized_preview(charset_obj):
    if charset_obj is None:
        return None
    preview = charset_obj.build_charset()
    parts = []
    if getattr(charset_obj, 'cyrillic_lower', False) and getattr(charset_obj, 'cyrillic_upper', False):
        parts.append('Кириллица')
    else:
        if getattr(charset_obj, 'cyrillic_lower', False):
            parts.append('Кириллица (строчные)')
        if getattr(charset_obj, 'cyrillic_upper', False):
            parts.append('Кириллица (прописные)')
    if getattr(charset_obj, 'latin_lower', False) and getattr(charset_obj, 'latin_upper', False):
        parts.append('Латиница')
    else:
        if getattr(charset_obj, 'latin_lower', False):
            parts.append('Латиница (строчные)')
        if getattr(charset_obj, 'latin_upper', False):
            parts.append('Латиница (прописные)')
    if getattr(charset_obj, 'space', False):
        parts.append('Пробел')
    if getattr(charset_obj, 'digits', False):
        parts.append('Цифры')
    if getattr(charset_obj, 'special', False):
        parts.append('Спецсимволы')
    if getattr(charset_obj, 'included', None):
        parts.append(f"Включая [{charset_obj.included}]")
    if getattr(charset_obj, 'excluded', None):
        parts.append(f"Исключая [{charset_obj.excluded}]")
    length_parts = []
    if charset_obj.min_length is not None:
        length_parts.append(f"Мин {charset_obj.min_length}")
    if charset_obj.max_length is not None:
        length_parts.append(f"Макс {charset_obj.max_length}")
    humanized_main = ', '.join(parts) if parts else None
    length_str = ', '.join(length_parts) if length_parts else None
    if humanized_main and length_str:
        return f"{humanized_main} ({length_str})"
    if humanized_main:
        return f"{humanized_main}"
    if length_str:
        return f"{length_str}"
    return preview

class FieldNestedSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(slug_field='name', read_only=True)
    tag = serializers.SerializerMethodField()
    charset = serializers.SerializerMethodField()

    class Meta:
        model = Field
        fields = ("id", "type", "label", "tag", "charset", "placeholder")

    def get_tag(self, obj):
        tag_obj = getattr(obj, 'tag', None)
        if tag_obj is None:
            return None
        return {"id": tag_obj.pk, "label": getattr(tag_obj, 'name', None)}

    def get_charset(self, obj):
        charset_obj = getattr(obj, 'charset', None)
        if charset_obj is None:
            return None
        return {
            "id": charset_obj.id,
            "min_length": charset_obj.min_length,
            "max_length": charset_obj.max_length,
            "preview": charset_obj.build_charset(),
            "humanized_preview": build_humanized_preview(charset_obj)
        }

    def get_humanized_preview(self, obj):
        charset_obj = getattr(obj, 'charset', None)
        return build_humanized_preview(charset_obj)

class FormFieldSerializer(serializers.ModelSerializer):
    form = serializers.PrimaryKeyRelatedField(queryset=FormField._meta.get_field('form').related_model.objects.all())
    field = FieldNestedSerializer(read_only=True)
    field_id = serializers.PrimaryKeyRelatedField(source="field", queryset=Field.objects.all(), write_only=True)

    class Meta:
        model = FormField
        fields = ("id", "form", "field", "field_id", "order", "available")

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
    charset = serializers.DictField(allow_null=True)
    enums = serializers.ListField(child=serializers.DictField(), source='enums_list')

    def to_representation(self, instance):
        field_instance = getattr(instance, 'field', None)
        charset_obj = getattr(field_instance, 'charset', None) if field_instance is not None else None
        charset_value = None
        if charset_obj is not None:
            charset_value = {
                'id': charset_obj.id,
                'min_length': charset_obj.min_length,
                'max_length': charset_obj.max_length,
                'preview': charset_obj.build_charset(),
                'humanized_preview': build_humanized_preview(charset_obj)
            }
        base = {
            'id': instance.id if field_instance else None,
            'type': getattr(getattr(field_instance, 'type', None), 'name', None) if field_instance else None,
            'label': getattr(field_instance, 'label', None) if field_instance else None,
            'placeholder': getattr(field_instance, 'placeholder', None) if field_instance else None,
            'charset': charset_value,
        }
        tag_id = getattr(field_instance, 'tag_id', None) if field_instance else None
        enums_map = self.context.get('enums_map', {})
        base['enums'] = enums_map.get(tag_id, []) if tag_id else []
        return base
    
