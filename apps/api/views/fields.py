from apps.api.serializers.fields import FieldSerializer, FieldTypeSerializer
from apps.forms.models import Field, FieldType
from rest_framework import viewsets


class FieldTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для FieldType - только чтение
    """
    queryset = FieldType.objects.all()
    serializer_class = FieldTypeSerializer


class FieldViewSet(viewsets.ModelViewSet):
    """
    ViewSet для Field - полный CRUD
    """
    queryset = Field.objects.select_related('type', 'tag').all()
    serializer_class = FieldSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        type_id = self.request.query_params.get('type')
        if type_id:
            queryset = queryset.filter(type_id=type_id)
        return queryset