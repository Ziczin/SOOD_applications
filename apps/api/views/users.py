from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect

from apps.users.models import CustomUser, UserRole

from apps.api.core.conditions.query_check import is_from_form
from apps.api.core.errors.ErrorStorage import ErrorStorage
from apps.api.core.decorators.protected_view import reqall, reqany, protected_api_view
from apps.api.core.decorators.checks import is_authenticated, role_admin, role_moderator, status_proxy

from apps.api.serializers.users import (
    ChangeRoleSerializer, CurrentUserSerializer, UserDetailSerializer,
    UserListSerializer, UserRegistrationSerializer, UserLoginSerializer
)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            if is_from_form(request):
                return redirect('dashboard')
            else:
                redirect_url = request.build_absolute_uri(reverse('dashboard'))
                data = {
                    "message": "Пользователь успешно зарегистрирован.",
                    "redirect_url": redirect_url,
                    "user": {
                        "id": user.pk,
                        "username": user.username,
                        "fullname": getattr(user, "fullname", "")
                    }
                }
                headers = {'Location': request.build_absolute_uri(reverse('user-detail', args=[user.pk]))}
                return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        err = ErrorStorage()
        code = None
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                code = err.authenticate.login.unauthorized.include()
        else:
            code = err.authenticate.login.invalid_data.include()

        return Response(
            {"errorStorage": err.as_list()},
            status=code
        )

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return redirect('/')

@protected_api_view
class UsersAPIView(APIView):
    @reqall(is_authenticated)
    def get(self, request, *args, **kwargs):
        err = ErrorStorage()

        q_username = request.GET.get('username')
        department_q = request.GET.get('department')

        if q_username:
            try:
                user = CustomUser.objects.get(username=q_username)
                serializer = UserDetailSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                qs = CustomUser.objects.none()
        else:
            qs = CustomUser.objects.all()

        if department_q:
            qs = qs.filter(department=department_q)

        serializer = UserListSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@protected_api_view
class CurrentUserAPIView(APIView):
    @reqall(is_authenticated)
    def get(self, request, *args, **kwargs):
        serializer = CurrentUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

@protected_api_view
class CurrentUserRoleAPIView(APIView):
    @reqall(is_authenticated)
    def get(self, request, *args, **kwargs):
        role = request.user.role
        permissions = []
        if request.user.verified:
            permissions.append('user')
            if role == UserRole.ADMIN:
                permissions.append('admin')
                permissions.append('moderator')
            if role == UserRole.MODERATOR:
                permissions.append('moderator')
        if request.user.proxy:
            permissions.append('proxy')

        return Response({
            'role': role,
            'permissions': permissions,
            'verified': request.user.verified,
            'proxy': request.user.proxy,
            }, status=status.HTTP_200_OK)

@protected_api_view
class RolesAPIView(APIView):
    @reqall(is_authenticated)
    def get(self, request, *args, **kwargs):
        err = ErrorStorage()

        q_username = request.GET.get('username')
        q_role = request.GET.get('role')
        
        if not q_username and not q_role:
            roles = [{'value': v, 'label': l} for v, l in UserRole.choices]
            return Response(roles, status=status.HTTP_200_OK)

        if q_username:
            try:
                user = CustomUser.objects.get(username=q_username)
            except CustomUser.DoesNotExist:
                code = err.users.user_not_found.include()
                return Response({"errorStorage": err.as_list()}, status=code)

            if q_role:
                matches = (user.role == q_role)
                return Response({'matches': matches}, status=status.HTTP_200_OK)

            return Response({'role': user.role}, status=status.HTTP_200_OK)

        code = err.general.invalid_request.include() if hasattr(err, 'general') else status.HTTP_400_BAD_REQUEST
        return Response({"errorStorage": err.as_list()}, status=code)

    @reqany(status_proxy, role_admin)
    def patch(self, request, username, *args, **kwargs):
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Not found"}, status=405)
        serializer = ChangeRoleSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True}, status=204)
    
@protected_api_view
class DepartmentAPIView(APIView):
    @reqall(is_authenticated)
    def get(self, request, *args, **kwargs):
        err = ErrorStorage()

        q_username = request.GET.get('username')
        q_role = request.GET.get('role')
        
        if not q_username and not q_role:
            roles = [{'value': v, 'label': l} for v, l in UserRole.choices]
            return Response(roles, status=status.HTTP_200_OK)

        if q_username:
            try:
                user = CustomUser.objects.get(username=q_username)
            except CustomUser.DoesNotExist:
                code = err.users.user_not_found.include()
                return Response({"errorStorage": err.as_list()}, status=code)

            if q_role:
                matches = (user.role == q_role)
                return Response({'matches': matches}, status=status.HTTP_200_OK)

            return Response({'role': user.role}, status=status.HTTP_200_OK)

        code = err.general.invalid_request.include() if hasattr(err, 'general') else status.HTTP_400_BAD_REQUEST
        return Response({"errorStorage": err.as_list()}, status=code)

    @reqall(status_proxy)
    def patch(self, request, username, *args, **kwargs):
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Not found"}, status=405)
        serializer = ChangeRoleSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True}, status=204)