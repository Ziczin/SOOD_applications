from apps.api.serializers.fields import FieldSerializer, FieldTypeSerializer
from apps.forms.models import Field, FieldType
from rest_framework import viewsets


from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from apps.api.serializers.fields import FieldSerializer

class FieldTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FieldType.objects.all()
    serializer_class = FieldTypeSerializer

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        field_type = self.get_object()
        fields_qs = Field.objects.filter(type=field_type).select_related('type', 'tag')
        page = self.paginate_queryset(fields_qs)
        if page is not None:
            serializer = FieldSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = FieldSerializer(fields_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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