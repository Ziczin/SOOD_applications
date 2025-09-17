from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect
from apps.users.models import CustomUser, UserRole, Department
from apps.api.serializers.users import (
    UserRegistrationSerializer, UserListSerializer, UserDetailSerializer,
    ChangeRoleSerializer, ChangeDepartmentSerializer,
    DepartmentSerializer, RoleChoiceSerializer
)
from apps.api.core.decorators.protected_view import protected_api_view, reqall, reqany
from apps.api.core.decorators.checks import is_authenticated, status_proxy, role_admin

def get_permissions(user):
    permissions = []
    if user.verified:
        permissions.append('user')
        if user.role == UserRole.ADMIN:
            permissions.append('admin')
            permissions.append('moderator')
        if user.role == UserRole.MODERATOR:
            permissions.append('moderator')
    if user.proxy:
        permissions.append('proxy')
    return permissions

class RegisterView(APIView):
    def post(self, request):
        s = UserRegistrationSerializer(data=request.data)
        if s.is_valid():
            u = s.save(); login(request,u)
            if request.POST.get('_from_form'): return redirect('dashboard')
            return Response({"user":{"id":u.pk,"username":u.username}}, status=201, headers={'Location': ''})
        return Response(s.errors, status=400)

class LoginView(APIView):
    def post(self, request):
        data = request.data
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user: login(request,user); return redirect('dashboard')
        return Response({"error":"invalid"}, status=400)

class LogoutView(APIView):
    def post(self, request):
        logout(request); return redirect('/')

@protected_api_view
class UsersViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = CustomUser.objects.all()
    lookup_field = 'username'

    def get_serializer_class(self):
        if self.action == 'list':
            # Для списка используем упрощенный сериализатор
            return UserListSerializer
        return UserDetailSerializer

    def list(self, request, *a, **k):
        q = request.GET.get('department')
        qs = self.queryset
        
        if q:
            qs = qs.filter(department=q)
        
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, username=None):
        user = get_object_or_404(CustomUser, username=username)
        serializer = UserDetailSerializer(user)
        data = serializer.data
        data['permissions'] = get_permissions(user)
        return Response(data, status=200)

@protected_api_view
class CurrentUserAPIView(APIView):
    @reqall(is_authenticated)
    def get(self, request, *args, **kwargs):
        serializer = UserDetailSerializer(request.user)
        to_ret = serializer.data
        to_ret['permissions'] = get_permissions(request.user)
        return Response(to_ret, status=status.HTTP_200_OK)

@protected_api_view
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'pk'

    def list(self, request, *args, **kwargs):
        qs = self.queryset
        return Response(self.get_serializer(qs, many=True).data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        obj = get_object_or_404(self.queryset, pk=pk)
        return Response(self.get_serializer(obj).data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, pk=None, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, pk=None, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, pk=None, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

@protected_api_view
class RoleListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Department.objects.none()
    serializer_class = RoleChoiceSerializer

    def list(self, request, *args, **kwargs):
        data = [{'value': r.value, 'label': r.label} for r in UserRole]
        return Response(data, status=status.HTTP_200_OK)
