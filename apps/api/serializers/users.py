from rest_framework import serializers
from apps.users.models import CustomUser, Department, UserRole


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя"""

    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    department = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2", "fullname", "department"]

    def validate(self, data):
        """Проверяет уникальность username и совпадение паролей"""
        if CustomUser.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError(
                "Пользователь с таким логином уже существует!"
            )
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Пароли не совпадают!")
        return data

    def create(self, validated_data):
        """Создаёт нового пользователя с хешированным паролем"""
        return CustomUser.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password1"],
            fullname=validated_data.get("fullname", ""),
            department=Department.objects.get(pk=int(validated_data["department"])),
        )


class DepartmentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Department"""

    class Meta:
        model = Department
        fields = ("id", "name")
        read_only_fields = ("id",)


class UserDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о пользователе"""

    department = DepartmentSerializer()
    role = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ("id", "username", "fullname", "department", "role", "verified")

    def get_role(self, obj):
        """Возвращает представление роли в виде словаря с id и name"""
        return {"id": dict(UserRole.choices).get(obj.role, ""), "name": obj.role}


class RoleChoiceSerializer(serializers.Serializer):
    """Сериализатор для выбора роли (используется для списка доступных ролей)"""

    id = serializers.CharField()
    name = serializers.CharField()


class ChangeRoleSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения роли пользователя"""

    role = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ["role"]

    def validate_role(self, value):
        """Проверяет, что роль является допустимой (по label или value)"""
        labels_map = {c.label: c.value for c in UserRole}
        ids_map = {c.value for c in UserRole}
        if value in labels_map:
            return labels_map[value]
        if value in ids_map:
            return value
        raise serializers.ValidationError("Недопустимая роль.")

    def update(self, instance, validated_data):
        """Обновляет роль пользователя"""
        instance.role = validated_data["role"]
        instance.save()
        return instance


class ChangeDepartmentSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения отдела пользователя"""

    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())

    class Meta:
        model = CustomUser
        fields = ["department"]


class ChangeUsernameSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения имени пользователя. Проверяет уникальность нового username, исключая текущего пользователя"""

    username = serializers.CharField(max_length=150)

    class Meta:
        model = CustomUser
        fields = ["username"]

    def validate_username(self, value):
        """Проверяет, что username уникален (кроме текущего пользователя)"""
        if (
            CustomUser.objects.filter(username=value)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise serializers.ValidationError(
                "Пользователь с таким логином уже существует."
            )
        return value

    def update(self, instance, validated_data):
        """Обновляет username пользователя"""
        instance.username = validated_data["username"]
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения пароля. Проверяет длину пароля (минимум 8 символов) и хеширует его перед сохранением"""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ["password"]

    def validate_password(self, value):
        """Дополнительная проверка длины пароля (хотя DRF уже проверяет min_length)"""
        if len(value) < 8:
            raise serializers.ValidationError(
                "Пароль должен содержать минимум 8 символов."
            )
        return value

    def update(self, instance, validated_data):
        """Хеширует и сохраняет новый пароль"""
        instance.set_password(validated_data["password"])
        instance.save()
        return instance
