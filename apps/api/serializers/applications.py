from rest_framework import serializers
from apps.forms.models import Form, FormField, Enum
from apps.application.models import (
    Application,
    ApplicationFormField,
    ApplicationStatus,
)
from apps.users.models import CustomUser, Department, UserRole


class ApplicationStatusListSerializer(serializers.Serializer):
    key = serializers.CharField()
    label = serializers.CharField()


class ApplicationStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=[(c.name, c.label) for c in ApplicationStatus]
    )


class ApplicationFormFieldCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    value = serializers.CharField(allow_blank=True, allow_null=True)


class ApplicationCreateSerializer(serializers.Serializer):
    form = serializers.IntegerField()
    data = ApplicationFormFieldCreateSerializer(many=True)
    user = serializers.IntegerField(required=False)
    executor = serializers.IntegerField(required=False)

    def validate_form(self, value):
        return Form.objects.get(pk=value)

    def validate(self, attrs):
        form = attrs["form"]
        form_field_ids = set(
            FormField.objects.filter(form=form).values_list("pk", flat=True)
        )
        for item in attrs["data"]:
            if item["id"] not in form_field_ids:
                raise serializers.ValidationError(
                    f"FormField id {item['id']} does not belong to form {form.pk}"
                )
        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        user = None
        if validated_data.get("user"):
            user = CustomUser.objects.filter(pk=validated_data["user"]).first()
        if (
            user is None
            and request
            and getattr(request, "user", None)
            and request.user.is_authenticated
        ):
            user = request.user
        executor = None
        if validated_data.get("executor"):
            executor = CustomUser.objects.filter(pk=validated_data["executor"]).first()
        app = Application.objects.create(
            form=validated_data["form"], user=user, executor=executor
        )
        app_fields = []
        for item in validated_data["data"]:
            ff = FormField.objects.filter(pk=item["id"]).first()
            if ff:
                af = ApplicationFormField(
                    application=app, form_field=ff, value=item.get("value", "") or ""
                )
                app_fields.append(af)
        ApplicationFormField.objects.bulk_create(app_fields)
        return app


class SimpleFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ["id", "label", "department"]


class SimpleDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name"]


class SimpleUserSerializer(serializers.ModelSerializer):
    department = SimpleDepartmentSerializer()
    role = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ("id", "fullname", "department", "role")

    def get_role(self, obj):
        return {"id": dict(UserRole.choices).get(obj.role, ""), "name": obj.role}


class ApplicationFieldOutputSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="form_field_id")
    type = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    class Meta:
        model = ApplicationFormField
        fields = ["id", "type", "label", "tag", "value"]

    def get_type(self, obj):
        field = getattr(obj, "form_field", None)
        f = getattr(field, "field", None)
        t = getattr(f, "type", None)
        if not t:
            return None
        return {"name": t.name, "label": t.label}

    def get_label(self, obj):
        field = getattr(obj, "form_field", None)
        f = getattr(field, "field", None)
        if not f:
            return None
        return f.label

    def get_tag(self, obj):
        field = getattr(obj, "form_field", None)
        f = getattr(field, "field", None)
        tag = getattr(f, "tag", None)
        if not tag:
            return None
        return tag.name

    def get_value(self, obj):
        field = getattr(obj, "form_field", None)
        f = getattr(field, "field", None)
        tag = getattr(f, "tag", None)
        val = obj.value
        if not tag or val is None or val == "":
            return val
        if isinstance(val, str) and val.isdigit():
            enum_obj = Enum.objects.filter(pk=int(val), enum_tag=tag).first()
            if enum_obj:
                return enum_obj.value
        return val


class ApplicationNoFieldsSerializer(serializers.ModelSerializer):
    form = SimpleFormSerializer(read_only=True)
    user = SimpleUserSerializer(read_only=True)
    executor = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Application
        fields = ["id", "form", "user", "executor", "date", "status", "msg"]


class ApplicationSerializer(serializers.ModelSerializer):
    application_fields = ApplicationFieldOutputSerializer(many=True, read_only=True)
    form = SimpleFormSerializer(read_only=True)
    user = SimpleUserSerializer(read_only=True)
    executor = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Application
        fields = [
            "id",
            "form",
            "user",
            "executor",
            "date",
            "status",
            "msg",
            "application_fields",
            "last_status_change",
        ]


class ApplicationUpdateSerializer(serializers.ModelSerializer):
    executor = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = Application
        fields = ["status", "msg", "executor"]
