from rest_framework import serializers
from .models import Department, CustomUser


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("id", "name")


class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    role = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "fullname",
            "department",
            "role",
        )
