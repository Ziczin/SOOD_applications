import json
from rest_framework import serializers
from apps.users.models import EventSubscriber

class EventSubscriberCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    event = serializers.CharField(max_length=255)
    response = serializers.JSONField(required=False, allow_null=True)

class EventCheckSerializer(serializers.ModelSerializer):
    response = serializers.SerializerMethodField()

    class Meta:
        model = EventSubscriber
        fields = ['id', 'user', 'event', 'response', 'other', 'last_check']

    def get_response(self, obj):
        if obj.response in (None, ''):
            return None
        try:
            return json.loads(obj.response)
        except Exception:
            return None
