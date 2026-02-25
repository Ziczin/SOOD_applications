from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    """Базовый сериализатор с общими методами"""

    def validate_blank_field(self, value, field_name):
        """Универсальная валидация для текстовых полей"""
        return "" if value is None else value.strip()

    def set_defaults(self, validated_data, defaults):
        """Установка значений по умолчанию"""
        for field, default in defaults.items():
            validated_data.setdefault(field, default)
        return validated_data

    def clean_validated_data(self, validated_data, fields_to_clean):
        """Очистка полей в validated_data"""
        for field in fields_to_clean:
            if field in validated_data and validated_data[field] is None:
                validated_data[field] = ""
        return validated_data
