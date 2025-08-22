from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

from apps.users.models import CustomUser, UserRole
from apps.api.core.errors.ErrorStorage import ErrorStorage
from apps.api.core.decorators.protected_view import protected_api_view, role_required, login_required

from apps.api.serializers.users import UserRegistrationSerializer, UserLoginSerializer


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
