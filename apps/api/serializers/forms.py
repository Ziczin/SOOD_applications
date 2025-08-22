from rest_framework import serializers

class FormDataSerializer(serializers.Serializer):
    label = serializers.CharField()
    name = serializers.CharField()