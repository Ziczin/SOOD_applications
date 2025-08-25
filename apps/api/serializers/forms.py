from rest_framework import serializers

class FormDataSerializer(serializers.Serializer):
    label = serializers.CharField(source='form_label')
    name = serializers.CharField(source='form_name')
    available = serializers.BooleanField()
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if hasattr(instance, 'label'):
            representation['label'] = instance.label
        if hasattr(instance, 'name'):
            representation['name'] = instance.name
            
        return representation