from rest_framework import serializers
from apps.users.models import CustomUser, UserRole, Department

class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'full_name', 'department']

    def validate(self, data):
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Пользователь с таким логином уже существует!")
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают!")
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password1'],
            full_name=validated_data['full_name'],
            department=Department.objects.get(id=validated_data['department']),
            role=UserRole.USER
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'full_name', 'email', 'department', 'role')

class UserDetailSerializer(serializers.ModelSerializer):
    department = serializers.StringRelatedField()
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'full_name', 'first_name', 'last_name', 'email', 'department', 'role', 'date_joined')

class CurrentUserSerializer(serializers.ModelSerializer):
    department = serializers.StringRelatedField()
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'full_name', 'first_name', 'last_name', 'email', 'department', 'role')

class ChangeRoleSerializer(serializers.Serializer):
    username = serializers.CharField()
    role = serializers.ChoiceField(choices=UserRole.choices)

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name')


class UserListSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'full_name', 'first_name', 'last_name', 'email', 'department', 'role')


class UserDetailSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'full_name', 'first_name', 'last_name',
            'email', 'department', 'role', 'date_joined', 'is_active'
        )


class CurrentUserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'full_name', 'first_name', 'last_name', 'email', 'department', 'role')


class ChangeRoleSerializer(serializers.Serializer):
    username = serializers.CharField()
    role = serializers.ChoiceField(choices=UserRole.choices)

    def validate_role(self, value):
        valid = [r for r, _ in UserRole.choices]
        if value not in valid:
            raise serializers.ValidationError("Недопустимая роль.")
        return value