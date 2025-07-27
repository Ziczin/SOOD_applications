from rest_framework import serializers
from .models import YTVideo

class YTVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = YTVideo
        fields = ['title', 'author']