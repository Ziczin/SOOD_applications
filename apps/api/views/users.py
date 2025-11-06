from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.api.cache_tools.helper import CacheHelper

from apps.users.models import CustomUser, UserRole
from apps.api.core.get_permissions import get_permissions
from apps.api.core.permissions import permissions
from apps.api.serializers.users import (
    UserDetailSerializer,
    ChangeRoleSerializer,
    ChangeDepartmentSerializer
)


user_cache = CacheHelper("users:user")
users_list_cache = CacheHelper("users:list")


def role_representation(role_value):
    return {
        'id': dict((choice.value, choice.label) for choice in UserRole).get(role_value, ''),
        'name': role_value
    }


@permissions("pppd : admin, proxy")
class UsersViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin
):
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'pk'

    def enrich_user_data(self, user_instance, serialized_data):
        serialized_data['permissions'] = get_permissions(user_instance)
        serialized_data['role'] = role_representation(user_instance.role)
        return serialized_data

    def get_queryset(self):
        base_queryset = super().get_queryset()
        department_param = self.request.GET.get('department')
        if department_param:
            return base_queryset.filter(department__pk=int(department_param)) if department_param.isdigit() else base_queryset.none()
        return base_queryset

    def list(self, request, *args, **kwargs):
        department_param = request.GET.get('department')
        cache_key_part = department_param if department_param is not None else "all"
        cached_response = users_list_cache.get(cache_key_part)
        if cached_response is not None:
            return Response(cached_response)

        response = super().list(request, *args, **kwargs)
        queryset_list = list(self.get_queryset())
        for index, user_instance in enumerate(queryset_list):
            response.data[index] = self.enrich_user_data(user_instance, response.data[index])

        users_list_cache.set(response.data, cache_key_part)
        return response

    def retrieve(self, request, *args, **kwargs):
        user_instance = self.get_object()
        cached_response = user_cache.get(user_instance.pk)
        if cached_response is not None:
            return Response(cached_response)

        enriched_data = self.enrich_user_data(user_instance, self.get_serializer(user_instance).data)
        user_cache.set(enriched_data, user_instance.pk)
        return Response(enriched_data)

    def save_and_refresh_cache(self, user_instance, serializer_instance):
        serializer_instance.is_valid(raise_exception=True)
        serializer_instance.save()
        serialized_data = self.get_serializer(user_instance).data
        enriched_data = self.enrich_user_data(user_instance, serialized_data)
        user_cache.set(enriched_data, user_instance.pk)
        users_list_cache.delete(getattr(user_instance, "department_id", "all"))
        users_list_cache.delete("all")
        return Response(enriched_data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        user_instance = self.get_object()
        serializer_instance = self.get_serializer(user_instance, data=request.data, partial=True)
        return self.save_and_refresh_cache(user_instance, serializer_instance)

    def perform_custom_action(self, request, serializer_class):
        user_instance = self.get_object()
        serializer_instance = serializer_class(user_instance, data=request.data, partial=True)
        return self.save_and_refresh_cache(user_instance, serializer_instance)

    @action(detail=True, methods=['patch'], url_path='change_role')
    def change_role(self, request, pk=None):
        return self.perform_custom_action(request, ChangeRoleSerializer)

    @action(detail=True, methods=['patch'], url_path='change_department')
    def change_department(self, request, pk=None):
        return self.perform_custom_action(request, ChangeDepartmentSerializer)
