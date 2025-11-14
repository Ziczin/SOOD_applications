from rest_framework import serializers
from apps.forms.models import FieldType, Field, EnumTag, FieldCharSet
from apps.users.models import Department

class FieldTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(allow_blank=True, allow_null=True, required=False)

    class Meta:
        model = FieldType
        fields = ('id', 'name', 'label', 'type')
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

class TagReadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk')
    label = serializers.CharField(source='name')

    class Meta:
        model = EnumTag
        fields = ('id', 'label')

class FieldCharSetSerializer(serializers.ModelSerializer):
    charset = serializers.SerializerMethodField()
    min_length = serializers.IntegerField(allow_null=True, required=False)
    max_length = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = FieldCharSet
        fields = [
            'id', 'label',
            'cyrillic_lower', 'cyrillic_upper', 'latin_lower', 'latin_upper',
            'space', 'digits', 'special',
            'included', 'excluded', 'min_length', 'max_length',
            'available', 'visible', 'department', 'shared',
            'charset'
        ]

    def get_charset(self, obj):
        return obj.build_charset()

    def to_internal_value(self, data):
        if isinstance(data, dict):
            for f in ('min_length', 'max_length'):
                if f in data and data[f] == '':
                    data[f] = None
        return super().to_internal_value(data)

class FieldSerializer(serializers.ModelSerializer):
    label = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    type = serializers.PrimaryKeyRelatedField(queryset=FieldType.objects.all(), allow_null=True, required=False)
    tag = serializers.PrimaryKeyRelatedField(queryset=EnumTag.objects.all(), allow_null=True, required=False, write_only=False)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), allow_null=True, required=False)
    charset = serializers.PrimaryKeyRelatedField(queryset=FieldCharSet.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Field
        fields = ('id', 'type', 'label', 'tag', 'department', 'required', 'charset', 'placeholder')
        read_only_fields = ('id',)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        tag_obj = getattr(instance, 'tag', None)
        if tag_obj is not None:
            rep['tag'] = TagReadSerializer(tag_obj).data
        else:
            rep['tag'] = None
        charset_obj = getattr(instance, 'charset', None)
        if charset_obj is not None:
            rep['charset'] = {
                'id': charset_obj.id,
                'min_length': charset_obj.min_length,
                'max_length': charset_obj.max_length,
                'preview': charset_obj.build_charset()
            }
        else:
            rep['charset'] = None
        return rep

    def validate_label(self, value):
        if value is None:
            return ''
        return value.strip()

    def create(self, validated_data):
        validated_data['label'] = validated_data.get('label', '')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'label' in validated_data:
            validated_data['label'] = validated_data.get('label') or ''
        else:
            validated_data.pop('label', None)
        validated_data.setdefault('type', instance.type)
        validated_data.setdefault('tag', instance.tag)
        return super().update(instance, validated_data)
