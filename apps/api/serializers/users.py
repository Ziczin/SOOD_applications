from rest_framework import serializers
from apps.users.models import CustomUser, Department, UserRole

class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    department = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['username','password1','password2','fullname','department']

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
            department=Department.objects.get(name=validated_data['department'])
        )

class UserListSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(read_only=True, slug_field='name')
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'fullname', 'department', 'role')

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'label')
        read_only_fields = ('id',)

    def validate_name(self, value):
        qs = Department.objects.filter(name=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Отдел с таким именем уже существует.")
        return value

class UserDetailSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    role = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'fullname', 'department', 'role', 'verified')

    def get_role(self, obj):
        return {
            'name': obj.role,
            'label': dict(UserRole.choices).get(obj.role, '')
        }
    
class RoleChoiceSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

class ChangeRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['role']

    def validate_role(self, value):
        valid = [c.value for c in UserRole]
        if value not in valid:
            raise serializers.ValidationError("Недопустимая роль.")
        return value

class ChangeDepartmentSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    class Meta:
        model = CustomUser
        fields = ['department']
