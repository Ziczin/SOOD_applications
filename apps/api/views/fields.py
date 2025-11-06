
from apps.api.serializers.fields import FieldSerializer, FieldTypeSerializer
from apps.forms.models import Field, FieldType, FormField
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from apps.api.cache_tools.helper import CacheHelper
from apps.api.cache_tools.forms_cache import (
    forms_data_cache,
    forms_list_cache,
    cache_key_for_form
)
field_types_cache = CacheHelper("field_types")
fields_cache = CacheHelper("fields")

class FieldTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FieldType.objects.all()
    serializer_class = FieldTypeSerializer

    def list(self, request, *args, **kwargs):
        cache_key = "all"
        cached = field_types_cache.get(cache_key)
        if cached is not None:
            return Response(cached, status=status.HTTP_200_OK)
        response = super().list(request, *args, **kwargs)
        field_types_cache.set(response.data, cache_key)
        return response

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        cache_key = f"pk:{pk}"
        cached = field_types_cache.get(cache_key)
        if cached is not None:
            return Response(cached, status=status.HTTP_200_OK)
        response = super().retrieve(request, *args, **kwargs)
        field_types_cache.set(response.data, cache_key)
        return response

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        cache_key = f"items:type:{pk}"
        cached = fields_cache.get(cache_key)
        if cached is not None:
            return Response(cached, status=status.HTTP_200_OK)
        field_type = self.get_object()
        fields_qs = Field.objects.filter(type=field_type).select_related('type', 'tag')
        serializer = FieldSerializer(fields_qs, many=True)
        fields_cache.set(serializer.data, cache_key)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        instance = serializer.save()
        field_types_cache.delete("all")
        field_types_cache.delete(f"pk:{getattr(instance, 'pk', None)}")
        fields_cache.delete(f"items:type:{getattr(instance, 'pk', None)}")
        form_field_qs = FormField.objects.filter(field__type_id=getattr(instance, 'pk', None)).values_list('form_id', flat=True).distinct()
        for form_id in form_field_qs:
            forms_data_cache.delete(cache_key_for_form(form_id))
        forms_list_cache.delete_pattern()

    def perform_destroy(self, instance):
        pk = getattr(instance, 'pk', None)
        form_field_qs = FormField.objects.filter(field__type_id=pk).values_list('form_id', flat=True).distinct()
        instance.delete()
        field_types_cache.delete("all")
        field_types_cache.delete(f"pk:{pk}")
        fields_cache.delete(f"items:type:{pk}")
        for form_id in form_field_qs:
            forms_data_cache.delete(cache_key_for_form(form_id))
        forms_list_cache.delete_pattern()


class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.select_related('type', 'tag').all()
    serializer_class = FieldSerializer

    def get_queryset(self):
        type_id = self.request.query_params.get('type')
        cache_key = f"type:{type_id}" if type_id is not None else "all"
        cached = fields_cache.get(cache_key)
        if cached is not None:
            return Field.objects.none() if not cached else Field.objects.filter(pk__in=[item['id'] for item in cached])
        queryset = super().get_queryset()
        if type_id:
            queryset = queryset.filter(type_id=type_id)
        serialized = self.get_serializer(queryset, many=True).data
        fields_cache.set(serialized, cache_key)
        return queryset

    def perform_create(self, serializer):
        instance = serializer.save()
        fields_cache.delete("all")
        fields_cache.delete(f"type:{getattr(instance, 'type_id', None)}")
        fields_cache.delete(f"items:type:{getattr(instance, 'type_id', None)}")
        form_ids = FormField.objects.filter(field_id=getattr(instance, 'pk', None)).values_list('form_id', flat=True).distinct()
        for form_id in form_ids:
            forms_data_cache.delete(cache_key_for_form(form_id))
        forms_list_cache.delete_pattern()

    def perform_update(self, serializer):
        instance = serializer.save()
        fields_cache.delete("all")
        fields_cache.delete(f"type:{getattr(instance, 'type_id', None)}")
        fields_cache.delete(f"items:type:{getattr(instance, 'type_id', None)}")
        form_ids = FormField.objects.filter(field_id=getattr(instance, 'pk', None)).values_list('form_id', flat=True).distinct()
        for form_id in form_ids:
            forms_data_cache.delete(cache_key_for_form(form_id))
        forms_list_cache.delete_pattern()

    def perform_destroy(self, instance):
        type_id = getattr(instance, 'type_id', None)
        instance.delete()
        fields_cache.delete("all")
        fields_cache.delete(f"type:{type_id}")
        fields_cache.delete(f"items:type:{type_id}")
        form_ids = FormField.objects.filter(field_id=getattr(instance, 'pk', None)).values_list('form_id', flat=True).distinct()
        for form_id in form_ids:
            forms_data_cache.delete(cache_key_for_form(form_id))
        forms_list_cache.delete_pattern()