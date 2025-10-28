from rest_framework import serializers, views, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.forms.models import Form, Field
from apps.application.models import Application, ApplicationField

class ApplicationFieldInputSerializer(serializers.Serializer):
    value = serializers.CharField(allow_blank=True)
    id = serializers.IntegerField()

class ApplicationCreateSerializer(serializers.Serializer):
    data = ApplicationFieldInputSerializer(many=True)
    form = serializers.IntegerField()

    def create(self, validated_data):
        form_id = validated_data["form"]
        form_obj = get_object_or_404(Form, pk=form_id)
        user = self.context.get("request").user if self.context.get("request") and self.context.get("request").user.is_authenticated else None
        app = Application.objects.create(form=form_obj, user=user)
        fields_input = validated_data["data"]
        app_fields = []
        for item in fields_input:
            field_obj = get_object_or_404(Field, pk=item["id"])
            app_field = ApplicationField(application=app, field=field_obj, value=item.get("value", ""))
            app_fields.append(app_field)
        ApplicationField.objects.bulk_create(app_fields)
        return app

class ApplicationCreateAPIView(views.APIView):
    serializer_class = ApplicationCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        app = serializer.save()
        return Response({"application_id": app.id}, status=status.HTTP_201_CREATED)
