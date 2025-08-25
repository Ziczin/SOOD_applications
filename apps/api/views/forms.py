from rest_framework import generics
from django.db.models import F
from apps.forms.models import Form
from apps.api.serializers.forms import FormDataSerializer
from urllib.parse import unquote

class FormListView(generics.ListAPIView):
    serializer_class = FormDataSerializer
    
    def get_queryset(self):
        form_name = self.request.query_params.get('form_name')
        department_name = self.request.query_params.get('department')
        
        if form_name:
            form_name = unquote(form_name)
        if department_name:
            department_name = unquote(department_name)
        
        queryset = Form.objects.all()
        
        if form_name:
            queryset = queryset.filter(form_name=form_name)
        
        if department_name:
            queryset = queryset.filter(department__name=department_name)
        
        return queryset.annotate(
            label=F('form_label'),
            name=F('form_name')
        )