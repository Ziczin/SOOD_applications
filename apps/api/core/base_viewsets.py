from rest_framework import viewsets, response
from django.db import transaction
from apps.api.core.set_event_response_for_all import set_event_response_for_all


class BaseModelViewSet(viewsets.ModelViewSet):
    """Базовый ViewSet с общими методами"""

    def perform_transaction(self, serializer, event_type, **kwargs):
        """Универсальный метод для операций с транзакцией"""
        with transaction.atomic():
            obj = serializer.save(**kwargs)

        self._clear_cache(obj)
        payload = self.get_serializer(obj).data
        set_event_response_for_all(event_type, payload)
        return obj

    def _clear_cache(self, obj):
        """Очистка кеша - переопределяется в наследниках"""
        pass

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_transaction(serializer, f"{self.basename}-post")
        return response.Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=kwargs.get("partial", False)
        )
        serializer.is_valid(raise_exception=True)
        self.perform_transaction(
            serializer, f"{self.basename}-{'patch' if kwargs.get('partial') else 'put'}"
        )
        return response.Response(serializer.data)

    def get_basename(self):
        """Получение basename для генерации event names"""
        return getattr(
            self, "basename", self.__class__.__name__.replace("ViewSet", "").lower()
        )
