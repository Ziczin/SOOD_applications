from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect

from apps.users.models import CustomUser, UserRole
from apps.api.core.errors.ErrorStorage import ErrorStorage
from apps.api.core.decorators.protected_view import protected_api_view, role_required, login_required

from apps.api.serializers.users import ChangeRoleSerializer, CurrentUserSerializer, UserDetailSerializer, UserListSerializer, UserRegistrationSerializer, UserLoginSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Пользователь успешно зарегистрирован."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        err = ErrorStorage()
        code = None
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username = serializer.validated_data['username'],
                password = serializer.validated_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else: code = err.authenticate.login.unauthorized.include()
        else: code = err.authenticate.login.invalid_data.include()
            
        return Response(
            {"errorStorage": err.as_list()},
            status=code)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return redirect('/')

class ChangeRoleView(APIView):

    def post(self, request):
        err = ErrorStorage()
        
        username = request.data.get('username')
        new_role = request.data.get('role')
        
        user_exists = username and CustomUser.objects.filter(username=username).exists()
        role_exists = new_role and new_role in [role_value for role_value, _ in UserRole.choices]
        
        if not user_exists:
            code = err.users.user_not_found.include()
        elif not role_exists:
            code = err.users.role.role_not_found.include()
        else:
            user = CustomUser.objects.get(username=username)
            user.role = new_role
            user.save()
            return Response(status=status.HTTP_200_OK)
        
        return Response(
            {"errorStorage": err.as_list()},
            status=code
        )

@protected_api_view
class UsersAPIView(APIView):
    """
    GET  /api/users/               -> список пользователей (auth required)
    GET  /api/users/<username>/    -> детальная инфо о пользователе (auth required)
    POST /api/users/change-role/   -> смена роли пользователя (только ADMIN)
    GET  /api/me/                  -> инфа о текущем пользователе (auth required)
    GET  /api/roles/               -> список ролей (auth required)

    Все методы помечены вашими декораторами: login_required / role_required.
    """

    # --- список пользователей ---
    @login_required
    def get(self, request, username: str = None, *args, **kwargs):
        """
        Если передан username в kwargs, обрабатывает как detail view.
        Иначе возвращает список всех пользователей.
        """
        # Если вызван как /api/users/<username>/ — отдать detail
        username_param = kwargs.get('username') or username
        if username_param:
            user = get_object_or_404(CustomUser, username=username_param)
            serializer = UserDetailSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # иначе — список
        qs = CustomUser.objects.all()
        serializer = UserListSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # --- смена роли ---
    @role_required(role=UserRole.ADMIN)
    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST /api/users/change-role/ — payload: { "username": "...", "role": "ADMIN" }
        Только для админов (role_required).
        """
        err = ErrorStorage()
        serializer = ChangeRoleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errorStorage": err.as_list(), "detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        new_role = serializer.validated_data['role']

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            code = err.users.user_not_found.include()
            return Response({"errorStorage": err.as_list()}, status=code)

        if new_role not in [r for r, _ in UserRole.choices]:
            code = err.users.role.role_not_found.include()
            return Response({"errorStorage": err.as_list()}, status=code)

        user.role = new_role
        user.save()
        return Response(status=status.HTTP_200_OK)


@protected_api_view
class CurrentUserAPIView(APIView):
    """
    GET /api/me/ -> информация о текущем пользователе
    """
    @login_required
    def get(self, request, *args, **kwargs):
        serializer = CurrentUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@protected_api_view
class RolesAPIView(APIView):
    """
    GET /api/roles/ -> список ролей
    """
    @login_required
    def get(self, request, *args, **kwargs):
        roles = [{'value': v, 'label': l} for v, l in UserRole.choices]
        return Response(roles, status=status.HTTP_200_OK)