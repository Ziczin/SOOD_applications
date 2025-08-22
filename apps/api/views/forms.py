from rest_framework import generics
from django.db.models import F
from apps.forms.models import Form
from apps.api.serializers.forms import FormDataSerializer

class FormListView(generics.ListAPIView):
    queryset = Form.objects.all()
    serializer_class = FormDataSerializer
    
    def get_queryset(self):
        return super().get_queryset().annotate(
            label=F('form_label'),
            name=F('form_name'),
        ).values('label','name','available')