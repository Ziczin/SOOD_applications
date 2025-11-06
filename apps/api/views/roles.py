from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from apps.users.models import UserRole

class RoleListView(APIView):
    def get(self, request):
        data = [{'id': role.label, 'name': role.value} for role in UserRole]
        return Response(data, status=status.HTTP_200_OK)