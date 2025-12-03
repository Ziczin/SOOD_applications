from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import transaction

from apps.api.core.permissions import permissions
from apps.forms.models import FormField, Form, Enum, Field
from apps.api.serializers.forms import (
    FormFieldSerializer,
    FormSerializer,
    FormFieldWithEnumsSerializer
)
from apps.api.cache_tools.forms_cache import (
    forms_data_cache,
    forms_list_cache,
    cache_key_for_form,
    cache_key_for_forms_list
)

@permissions('r: user; 3p: admin, proxy')
class FormFieldViewSet(viewsets.ModelViewSet):
    queryset = FormField.objects.select_related('field', 'field__type', 'field__tag').filter(available=True)
    serializer_class = FormFieldSerializer

    def get_queryset(self):
        queryset = super().get_queryset().order_by('order')
        form_param = self.request.query_params.get('form')
        if form_param is not None:
            return queryset.filter(form=form_param, available=True)
        return queryset

    @action(detail=False, methods=['patch'])
    def swap(self, request):
        first_id = request.data.get('a')
        second_id = request.data.get('b')
        queryset = FormField.objects.select_related('field', 'field__type', 'field__tag').all()
        first = get_object_or_404(queryset, id=first_id)
        second = get_object_or_404(queryset, id=second_id)
        with transaction.atomic():
            FormField.objects.filter(pk=first.pk).update(order=second.order)
            FormField.objects.filter(pk=second.pk).update(order=first.order)
        first.refresh_from_db()
        second.refresh_from_db()
        serialized = self.get_serializer([first, second], many=True).data
        forms_data_cache.delete(cache_key_for_form(getattr(first, 'form_id', None)))
        forms_data_cache.delete(cache_key_for_form(getattr(second, 'form_id', None)))
        forms_list_cache.delete_pattern()
        return Response(serialized, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        instance = serializer.save()
        forms_data_cache.delete(cache_key_for_form(getattr(instance, 'form_id', None)))
        forms_list_cache.delete_pattern()

    def perform_update(self, serializer):
        instance = serializer.save()
        forms_data_cache.delete(cache_key_for_form(getattr(instance, 'form_id', None)))
        forms_list_cache.delete_pattern()

    def perform_destroy(self, instance):
        form_id = getattr(instance, 'form_id', None)
        instance.delete()
        forms_data_cache.delete(cache_key_for_form(form_id))
        forms_list_cache.delete_pattern()

@permissions('r: user; 3p: admin, proxy')
class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.filter(available=True).select_related('department')
    serializer_class = FormSerializer

    def get_queryset(self):
        base = self.queryset
        dept_param = self.request.query_params.get('department')
        if dept_param is None:
            qs = base
        else:
            if dept_param.isdigit():
                qs = base.filter(department_id=int(dept_param))
            else:
                qs = base.filter(department_id=None)
        return qs

    def list(self, request, *args, **kwargs):
        dept_param = self.request.query_params.get('department')
        department_id = dept_param if dept_param and dept_param.isdigit() else None
        cache_key = cache_key_for_forms_list(department_id=department_id)
        
        cached = forms_list_cache.get(cache_key)
        if cached is not None:
            return Response(cached, status=status.HTTP_200_OK)
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        forms_list_cache.set(serializer.data, cache_key)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        department = getattr(self.request.user, "department", None)
        with transaction.atomic():
            instance = serializer.save(department=department)
        forms_data_cache.delete(cache_key_for_form(getattr(instance, 'pk', None)))
        forms_list_cache.delete_pattern()

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        serialized = self.get_serializer(instance).data
        return Response(serialized, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='visible')
    def visible(self, request):
        cache_key = cache_key_for_forms_list(visible=True)
        
        cached = forms_list_cache.get(cache_key)
        if cached is not None:
            return Response(cached, status=status.HTTP_200_OK)
        
        forms = Form.objects.filter(available=True, visible=True)
        serialized = self.get_serializer(forms, many=True).data
        forms_list_cache.set(serialized, cache_key)
        return Response(serialized, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='data')
    def data(self, request, pk=None):
        cache_key = cache_key_for_form(pk)
        cached = forms_data_cache.get(cache_key)
        if cached is not None:
            return Response(cached, status=status.HTTP_200_OK)

        form = get_object_or_404(Form.objects.filter(available=True), pk=pk)
        form_fields_qs = (
            FormField.objects.filter(form=form, available=True)
            .order_by('order')
            .select_related('field', 'field__type', 'field__tag')
        )
        tag_ids = {ff.field.tag_id for ff in form_fields_qs if ff.field and ff.field.tag_id}
        enums_by_tag = {}
        if tag_ids:
            enums_qs = Enum.objects.filter(enum_tag_id__in=tag_ids, available=True).order_by('id')
            for enum in enums_qs:
                enums_by_tag.setdefault(enum.enum_tag_id, []).append({"id": enum.id, "value": enum.value})
        serializer = FormFieldWithEnumsSerializer(form_fields_qs, many=True, context={'enums_map': enums_by_tag})
        form_data = {"id": form.id, "label": form.label}
        payload = {"form": form_data, "fields": serializer.data}

        forms_data_cache.set(payload, cache_key)
        return Response(payload, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        instance = serializer.save()
        forms_data_cache.delete(cache_key_for_form(getattr(instance, 'pk', None)))
        forms_list_cache.delete_pattern()
        return instance

    def perform_destroy(self, instance):
        pk = getattr(instance, 'pk', None)
        instance.delete()
        forms_data_cache.delete(cache_key_for_form(pk))
        forms_list_cache.delete_pattern()