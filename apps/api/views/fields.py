from django.db.models import Q
from apps.api.serializers.fields import FieldCharSetSerializer, FieldSerializer, FieldTypeSerializer
from apps.forms.models import Field, FieldCharSet, FieldType, FormField
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
        fields_qs = Field.objects.filter(type=field_type).select_related('type', 'tag', 'charset')
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
    queryset = Field.objects.select_related('type', 'tag', 'charset').all()
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

    def _clear_field_caches(self, instance):
        fields_cache.delete("all")
        fields_cache.delete(f"type:{getattr(instance, 'type_id', None)}")
        fields_cache.delete(f"items:type:{getattr(instance, 'type_id', None)}")
        form_ids = FormField.objects.filter(field_id=getattr(instance, 'pk', None)).values_list('form_id', flat=True).distinct()
        for form_id in form_ids:
            forms_data_cache.delete(cache_key_for_form(form_id))
        forms_list_cache.delete_pattern()

    def perform_create(self, serializer):
        instance = serializer.save()
        self._clear_field_caches(instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        self._clear_field_caches(instance)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        charset_id = data.get('charset') or data.get('fieldcharset') or data.get('field_charset')
        if charset_id is not None:
            try:
                charset_obj = FieldCharSet.objects.get(pk=charset_id)
                data['charset'] = charset_obj.pk
            except FieldCharSet.DoesNotExist:
                data.pop('charset', None)
        request._full_data = data
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        charset_id = data.get('charset') or data.get('fieldcharset') or data.get('field_charset')
        if charset_id is not None:
            try:
                charset_obj = FieldCharSet.objects.get(pk=charset_id)
                data['charset'] = charset_obj.pk
            except FieldCharSet.DoesNotExist:
                data.pop('charset', None)
        request._full_data = data
        return super().update(request, *args, **kwargs)


from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

field_charsets_cache = CacheHelper("field_charsets")

class FieldCharSetViewSet(viewsets.ModelViewSet):
    queryset = FieldCharSet.objects.all()
    serializer_class = FieldCharSetSerializer

    def _get_cache_key(self, suffix=""):
        """Генерирует ключ кеша с учетом пользователя и параметров"""
        user = self.request.user if self.request.user.is_authenticated else None
        visible_q = self.request.query_params.get('visible', None)
        
        key_parts = []
        if user and getattr(user, 'department', None):
            key_parts.append(f"dep:{user.department.id}")
        else:
            key_parts.append("dep:anonymous")
        
        if visible_q is not None:
            key_parts.append(f"visible:{visible_q}")
        
        key_parts.append(suffix)
        return ":".join(filter(None, key_parts))

    def list(self, request, *args, **kwargs):
        cache_key = self._get_cache_key("list")
        cached = field_charsets_cache.get(cache_key)
        if cached is not None:
            return Response(cached, status=status.HTTP_200_OK)
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        field_charsets_cache.set(serializer.data, cache_key)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        cache_key = f"pk:{pk}"
        cached = field_charsets_cache.get(cache_key)
        if cached is not None:
            return Response(cached, status=status.HTTP_200_OK)
        
        response = super().retrieve(request, *args, **kwargs)
        field_charsets_cache.set(response.data, cache_key)
        return response

    def get_queryset(self):
        user = self.request.user if self.request.user.is_authenticated else None
        visible_q = self.request.query_params.get('visible', None)
        base_q = Q(available=True)
        
        if user and getattr(user, 'department', None):
            dep = user.department
            base_q &= (Q(shared=True) | Q(department=dep))
        else:
            base_q &= Q(shared=True)
            
        if visible_q is not None:
            if visible_q.lower() in ['1', 'true', 'yes']:
                base_q &= Q(visible=True)
            else:
                base_q &= Q(visible=False)
        
        return FieldCharSet.objects.filter(base_q)

    def _clear_charset_caches(self, instance):
        """Очищает все связанные кеши при изменении FieldCharSet"""
        field_charsets_cache.delete_pattern()
        
        # Очищаем кеши полей, которые используют этот charset
        fields_using_charset = Field.objects.filter(charset_id=getattr(instance, 'pk', None))
        for field in fields_using_charset:
            fields_cache.delete("all")
            fields_cache.delete(f"type:{getattr(field, 'type_id', None)}")
            fields_cache.delete(f"items:type:{getattr(field, 'type_id', None)}")
        
        # Очищаем кеши форм, которые содержат поля с этим charset
        form_ids = FormField.objects.filter(
            field__charset_id=getattr(instance, 'pk', None)
        ).values_list('form_id', flat=True).distinct()
        
        for form_id in form_ids:
            forms_data_cache.delete(cache_key_for_form(form_id))
        
        forms_list_cache.delete_pattern()


    def perform_create(self, serializer):
        instance = serializer.save()
        self._clear_charset_caches(instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        self._clear_charset_caches(instance)

    def perform_destroy(self, instance):
        pk = getattr(instance, 'pk', None)
        self._clear_charset_caches(instance)
        instance.delete()

    @action(detail=False, methods=['get'], url_path='history', url_name='history')
    def history(self, request):
        cache_key = self._get_cache_key("history")
        cached = field_charsets_cache.get(cache_key)
        if cached is not None:
            return Response(cached, status=status.HTTP_200_OK)
        
        qs = FieldCharSet.objects.all()
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            field_charsets_cache.set(response.data, cache_key)
            return response
        
        serializer = self.get_serializer(qs, many=True)
        response_data = serializer.data
        field_charsets_cache.set(response_data, cache_key)
        return Response(response_data)