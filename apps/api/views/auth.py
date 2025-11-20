from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.middleware.csrf import get_token
from django.http import JsonResponse

from apps.users.models import UserRole
from apps.api.core.get_permissions import get_permissions
from apps.api.serializers.users import UserRegistrationSerializer, UserDetailSerializer
from apps.api.cache_tools.helper import CacheHelper

user_cache = CacheHelper("users:user")

def csrf_token_view(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

def role_representation(role_value):
    return {
        'id': dict((choice.value, choice.label) for choice in UserRole).get(role_value, ''),
        'name': role_value
    }

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        return redirect('dashboard')

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        next_url = request.data.get('next')
        print("+"*1231, request.data)
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            if next_url: return redirect(next_url)
            else: return redirect('dashboard')
                
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return redirect('/')

class CurrentUserAPIView(APIView):
    def get(self, request):
        user_instance = request.user
        cached = user_cache.get(user_instance.pk)
        if cached is not None:
            return Response(cached)
        serialized = UserDetailSerializer(user_instance).data
        serialized['permissions'] = get_permissions(user_instance)
        serialized['role'] = role_representation(user_instance.role)
        user_cache.set(serialized, user_instance.pk)
        return Response(serialized, status=status.HTTP_200_OK)
