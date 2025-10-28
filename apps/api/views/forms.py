from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.forms.models import FormField, Form, Enum
from apps.api.serializers.forms import FormFieldSerializer, FormSerializer
from django.shortcuts import get_object_or_404
from django.db import transaction

class FormFieldViewSet(viewsets.ModelViewSet):
    queryset = FormField.objects.all()
    serializer_class = FormFieldSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        form = self.request.query_params.get('form')
        if form is not None:
            return qs.filter(form=form).order_by('order')
        return qs.order_by('order')
    
    @action(detail=False, methods=['patch'])
    def swap(self, request):
        a = request.data.get('a')
        b = request.data.get('b')

        qs = self.get_queryset()
        a = qs.get(id=a)
        b = qs.get(id=b)

        with transaction.atomic():
            tmp = a.order
            FormField.objects.filter(pk=a.pk).update(order=b.order)
            FormField.objects.filter(pk=b.pk).update(order=tmp)

        a.refresh_from_db()
        b.refresh_from_db()
        return Response(self.get_serializer([a, b], many=True).data)

class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer

    def get_queryset(self):
        qs = Form.objects.filter(available=True)
        dept_param = self.request.query_params.get('department')
        if not dept_param:
            return qs
        if dept_param.isdigit():
            return qs.filter(department_id=int(dept_param))
        return qs.filter(department_id=None)

    def perform_create(self, serializer):
        user = self.request.user
        dept = getattr(user, "department", None)
        with transaction.atomic():
            if dept is not None:
                serializer.save(department=dept)
            else:
                serializer.save()

    def retrieve(self, request, pk=None):
        form = get_object_or_404(Form.objects.all(), pk=pk)
        serializer = self.get_serializer(form)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='visible')
    def visible(self, request):
        forms = Form.objects.filter(available=True, visible=True)
        serializer = self.get_serializer(forms, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='data')
    def data(self, request, pk=None):
        form = get_object_or_404(Form.objects.filter(available=True), pk=pk)

        form_fields_qs = FormField.objects.filter(form=form).order_by('order').select_related('field', 'field__type', 'field__tag')
        tag_ids = [ff.field.tag_id for ff in form_fields_qs if ff.field and ff.field.tag_id]
        enums_by_tag = {}
        if tag_ids:
            enums = Enum.objects.filter(enum_tag_id__in=tag_ids, available=True).order_by('id')
            for e in enums:
                enums_by_tag.setdefault(e.enum_tag_id, []).append({"id": e.id, "value": e.value})

        fields = []
        for ff in form_fields_qs:
            f = ff.field
            field_obj = {
                "id": ff.id if f else None,
                "type": f.type.name if f and f.type else None,
                "label": f.label if f else None,
            }
            if f and f.tag_id:
                field_obj["enums"] = enums_by_tag.get(f.tag_id, [])
            else:
                field_obj["enums"] = []
            fields.append(field_obj)

        form_data = {
            "id": form.id,
            "label": form.label,
        }

        return Response({"form": form_data, "fields": fields}, status=200)

















