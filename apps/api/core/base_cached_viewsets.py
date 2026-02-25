from apps.api.cache_tools.mixins import (
    CacheListMixin,
    CacheRetrieveMixin,
    CacheInvalidationMixin,
    CacheActionMixin,
)
from apps.api.core.base_viewsets import BaseModelViewSet
from rest_framework import response
from django.core.cache import cache
import json


class BaseCachedViewSet(
    CacheListMixin,
    CacheRetrieveMixin,
    CacheInvalidationMixin,
    CacheActionMixin,
    BaseModelViewSet,
):
    """
    Базовый ViewSet со всеми миксинами кеширования.
    Кеширует только сериализованные JSON строки.
    """

    list_cache_key = None
    detail_cache_key = None
    cache_keys_to_clear = []
    cache_timeout = 60 * 15  # 15 минут по умолчанию

    def _clear_cache(self, obj):
        self.clear_cache(getattr(obj, "id", None))

    def list(self, request, *args, **kwargs):
        # Кешируем JSON строки
        if self.list_cache_key:
            cached_json = cache.get(self.list_cache_key)
            if cached_json is not None:
                try:
                    # Декодируем JSON обратно в данные
                    cached_data = json.loads(cached_json)
                    return response.Response(cached_data)
                except json.JSONDecodeError:
                    # Если кеш поврежден, игнорируем его
                    pass

        # Получаем свежий queryset
        qs = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(qs, many=True)
        response_data = serializer.data

        # Сохраняем в кеш как JSON строку
        if self.list_cache_key:
            cache.set(
                self.list_cache_key, json.dumps(response_data), self.cache_timeout
            )

        return response.Response(response_data)

    def retrieve(self, request, *args, **kwargs):
        # Кешируем JSON строки
        if self.detail_cache_key:
            cache_key = self.detail_cache_key.format(id=kwargs["pk"])
            cached_json = cache.get(cache_key)
            if cached_json is not None:
                try:
                    cached_data = json.loads(cached_json)
                    return response.Response(cached_data)
                except json.JSONDecodeError:
                    pass

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = serializer.data

        # Сохраняем в кеш как JSON строку
        if self.detail_cache_key:
            cache_key = self.detail_cache_key.format(id=instance.pk)
            cache.set(cache_key, json.dumps(response_data), self.cache_timeout)

        return response.Response(response_data)

    def destroy(self, request, *args, **kwargs):
        """Переопределяем destroy для очистки кеша"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response(status=204)
