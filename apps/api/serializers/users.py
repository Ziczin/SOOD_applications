from rest_framework import serializers
from apps.users.models import CustomUser, Department, UserRole

class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    department = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'fullname', 'department']

    def validate(self, data):
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Пользователь с таким логином уже существует!")
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают!")
        return data

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password1'],
            fullname=validated_data.get('fullname',''),
            department=Department.objects.get(pk=int(validated_data['department']))
        )

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name')
        read_only_fields = ('id',)

class UserDetailSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    role = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'fullname', 'department', 'role', 'verified')

    def get_role(self, obj):
        return {'id': dict(UserRole.choices).get(obj.role, ''), 'name': obj.role}
    
class RoleChoiceSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()

class ChangeRoleSerializer(serializers.ModelSerializer):
    role = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['role']

    def validate_role(self, value):
        labels_map = {c.label: c.value for c in UserRole}
        ids_map = {c.value for c in UserRole}
        if value in labels_map:
            return labels_map[value]
        if value in ids_map:
            return value
        raise serializers.ValidationError("Недопустимая роль.")

    def update(self, instance, validated_data):
        instance.role = validated_data['role']
        instance.save()
        return instance

class ChangeDepartmentSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    class Meta:
        model = CustomUser
        fields = ['department']
