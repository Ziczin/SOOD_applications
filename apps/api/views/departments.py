from rest_framework import viewsets
from rest_framework.response import Response
from apps.users.models import Department
from apps.api.serializers.users import DepartmentSerializer
from apps.api.cache_tools.helper import CacheHelper

department_list_cache = CacheHelper("departments:list")
department_cache = CacheHelper("departments:item")

from apps.api.core.permissions import permissions

@permissions('r: user; 3p: admin')
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def list(self, request, *args, **kwargs):
        cached = department_list_cache.get("all")
        if cached is not None:
            return Response(cached)
        response = super().list(request, *args, **kwargs)
        department_list_cache.set(response.data, "all")
        return response

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        cached = department_cache.get(instance.pk)
        if cached is not None:
            return Response(cached)
        response = super().retrieve(request, *args, **kwargs)
        department_cache.set(response.data, instance.pk)
        return response

    def _save_and_refresh_cache(self, instance):
        department_list_cache.delete("all")
        department_cache.set(self.get_serializer(instance).data, instance.pk)

    def perform_create(self, serializer):
        instance = serializer.save()
        self._save_and_refresh_cache(instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        self._save_and_refresh_cache(instance)

    def perform_destroy(self, instance):
        pk = instance.pk
        instance.delete()
        department_list_cache.delete("all")
        department_cache.delete(pk)
