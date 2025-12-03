from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Q

from apps.forms.models import EnumTag, Enum, FormField
from apps.api.serializers.enums import EnumTagSerializer, EnumSerializer, EnumTagHistorySerializer
from apps.api.core.permissions import permissions
from apps.api.cache_tools.helper import CacheHelper
from apps.api.cache_tools.forms_cache import (
    forms_data_cache,
    forms_list_cache,
    cache_key_for_form
)

enums_by_tag_cache = CacheHelper("enums:by_tag")

@permissions('r: user; 3p: admin, proxy')
class EnumTagViewSet(viewsets.ModelViewSet):
    queryset = EnumTag.objects.all()
    serializer_class = EnumTagSerializer

    def get_queryset(self):
        user = self.request.user
        department = getattr(user, "department", None)
        base_qs = EnumTag.objects.filter(available=True)
        return base_qs.filter(Q(department=department) | Q(shared=True)) if department is not None else base_qs.filter(shared=True)

    def perform_create(self, serializer):
        department = getattr(self.request.user, "department", None)
        with transaction.atomic():
            instance = serializer.save(department=department) if department is not None else serializer.save()
        enums_by_tag_cache.delete(f"tag:{getattr(instance, 'pk', 'none')}")
        form_ids = FormField.objects.filter(field__tag_id=getattr(instance, 'pk', None)).values_list('form_id', flat=True).distinct()
        for form_id in form_ids:
            forms_data_cache.delete(cache_key_for_form(form_id))
        forms_list_cache.delete_pattern()

    def perform_update(self, serializer):
        instance = serializer.save()
        enums_by_tag_cache.delete(f"tag:{getattr(instance, 'pk', 'none')}")
        form_ids = FormField.objects.filter(field__tag_id=getattr(instance, 'pk', None)).values_list('form_id', flat=True).distinct()
        for form_id in form_ids:
            forms_data_cache.delete(cache_key_for_form(form_id))
        forms_list_cache.delete_pattern()

    def perform_destroy(self, instance):
        pk = instance.pk
        form_ids = FormField.objects.filter(field__tag_id=pk).values_list('form_id', flat=True).distinct()
        instance.delete()
        enums_by_tag_cache.delete(f"tag:{pk}")
        for form_id in form_ids:
            forms_data_cache.delete(cache_key_for_form(form_id))
        forms_list_cache.delete_pattern()

    @action(detail=True, methods=['get'], url_path='items')
    def items(self, request, pk=None):
        cache_key = f"tag:{pk}"
        cached = enums_by_tag_cache.get(cache_key)
        if cached is not None:
            return Response(cached)
        tag = self.get_object()
        queryset = Enum.objects.filter(available=True, enum_tag=tag)
        serializer = EnumSerializer(queryset, many=True)
        enums_by_tag_cache.set(serializer.data, cache_key)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='history')
    def history_list(self, request, *args, **kwargs):
        queryset = EnumTag.objects.all()
        serializer = EnumTagHistorySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='history')
    def history_detail(self, request, pk=None, *args, **kwargs):
        tag = self.get_object()
        serializer = EnumTagHistorySerializer(tag, context={'request': request})
        return Response(serializer.data)


@permissions('r: user; 3p: admin, proxy')
class EnumViewSet(viewsets.ModelViewSet):
    queryset = Enum.objects.all()
    serializer_class = EnumSerializer

    def list(self, request, *args, **kwargs):
        tag_param = request.GET.get('tag')
        cache_key = f"tag:{tag_param}" if tag_param is not None else "all"
        cached = enums_by_tag_cache.get(cache_key)
        if cached is not None:
            return Response(cached)
        response = super().list(request, *args, **kwargs)
        enums_by_tag_cache.set(response.data, cache_key)
        return response

    def perform_create(self, serializer):
        instance = serializer.save()
        tag_id = getattr(instance, 'enum_tag_id', None)
        enums_by_tag_cache.delete(f"tag:{tag_id}")
        form_ids = FormField.objects.filter(field__tag_id=tag_id).values_list('form_id', flat=True).distinct()
        for form_id in form_ids:
            forms_data_cache.delete(cache_key_for_form(form_id))
        forms_list_cache.delete_pattern()

    def perform_update(self, serializer):
        instance = serializer.save()
        tag_id = getattr(instance, 'enum_tag_id', None)
        enums_by_tag_cache.delete(f"tag:{tag_id}")
        form_ids = FormField.objects.filter(field__tag_id=tag_id).values_list('form_id', flat=True).distinct()
        for form_id in form_ids:
            forms_data_cache.delete(cache_key_for_form(form_id))
        forms_list_cache.delete_pattern()

    def perform_destroy(self, instance):
        tag_id = getattr(instance, 'enum_tag_id', None)
        form_ids = FormField.objects.filter(field__tag_id=tag_id).values_list('form_id', flat=True).distinct()
        instance.delete()
        enums_by_tag_cache.delete(f"tag:{tag_id}")
        for form_id in form_ids:
            forms_data_cache.delete(cache_key_for_form(form_id))
        forms_list_cache.delete_pattern()