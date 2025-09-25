from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect
from apps.users.models import CustomUser, UserRole, Department
from apps.api.core.get_permissions import get_permissions
from apps.api.core.permissions import permissions
from apps.api.serializers.users import (
    UserRegistrationSerializer, UserDetailSerializer,
    ChangeRoleSerializer, ChangeDepartmentSerializer,
    DepartmentSerializer, RoleChoiceSerializer
)

def role_rep(role_value):
    choices = {c.value: c.label for c in UserRole}
    label = choices.get(role_value, '')
    return {'id': label, 'name': role_value}

class RegisterView(APIView):
    def post(self, request):
        s = UserRegistrationSerializer(data=request.data)
        if s.is_valid():
            u = s.save(); login(request, u)
            return redirect('dashboard')
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

@permissions("pppd : admin, proxy")
class UsersViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin
    ):
    queryset = CustomUser.objects.all()
    lookup_field = 'pk'

    def get_serializer_class(self):
        return UserDetailSerializer

    def list(self, request, *a, **k):
        q = request.GET.get('department')
        qs = self.queryset
        if q:
            try:
                qs = qs.filter(department__pk=int(q))
            except (ValueError, TypeError):
                qs = qs.none()
        serializer = self.get_serializer(qs, many=True)
        data = serializer.data
        for i, user_obj in enumerate(qs):
            data[i]['permissions'] = get_permissions(user_obj)
            data[i]['role'] = role_rep(user_obj.role)
        return Response(data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = UserDetailSerializer(user)
        data = serializer.data
        data['permissions'] = get_permissions(user)
        data['role'] = role_rep(user.role)
        return Response(data, status=200)
    
    def partial_update(self, request, pk=None):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = UserDetailSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        data['permissions'] = get_permissions(user)
        data['role'] = role_rep(user.role)
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['patch'], url_path='change_role')
    def change_role(self, request, pk=None):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = ChangeRoleSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        updated = UserDetailSerializer(user).data
        updated['permissions'] = get_permissions(user)
        updated['role'] = role_rep(user.role)
        return Response(updated, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='change_department')
    def change_department(self, request, pk=None):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = ChangeDepartmentSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        updated = UserDetailSerializer(user).data
        updated['permissions'] = get_permissions(user)
        updated['role'] = role_rep(user.role)
        return Response(updated, status=status.HTTP_200_OK)

class CurrentUserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = UserDetailSerializer(request.user)
        to_ret = serializer.data
        to_ret['permissions'] = get_permissions(request.user)
        to_ret['role'] = role_rep(request.user.role)
        return Response(to_ret, status=status.HTTP_200_OK)

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

class RoleListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Department.objects.none()
    serializer_class = RoleChoiceSerializer

    def list(self, request, *args, **kwargs):
        data = [{'id': r.label, 'name': r.value} for r in UserRole]
        return Response(data, status=status.HTTP_200_OK)
