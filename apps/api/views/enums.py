from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Q

from apps.forms.models import EnumTag, Enum
from apps.api.serializers.enums import EnumTagSerializer, EnumSerializer, EnumTagHistorySerializer
from apps.api.core.permissions import permissions

@permissions(
    'ppp : admin, proxy',
    'get : user'
)
class EnumTagViewSet(viewsets.ModelViewSet):
    queryset = EnumTag.objects.all()
    serializer_class = EnumTagSerializer

    def get_queryset(self):
        user = self.request.user
        dept = getattr(user, "department", None)
        qs = EnumTag.objects.filter(available=True)
        if dept is not None:
            return qs.filter(Q(department=dept) | Q(shared=True))
        return qs.filter(shared=True)

    def perform_create(self, serializer):
        user = self.request.user
        dept = getattr(user, "department", None)
        with transaction.atomic():
            if dept is not None:
                serializer.save(department=dept)
            else:
                serializer.save()

    @action(detail=True, methods=['get'], url_path='items')
    def items(self, request, pk=None):
        tag = self.get_object()
        qs = Enum.objects.filter(available=True, enum_tag=tag)
        serializer = EnumSerializer(qs, many=True)
        return Response(serializer.data)
    
    def history_list(self, request, *args, **kwargs):
        qs = EnumTag.objects.all()
        page = self.paginate_queryset(qs)
        serializer_class = EnumTagHistorySerializer
        if page is not None:
            serializer = serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = serializer_class(qs, many=True, context={'request': request})
        return Response(serializer.data)

    def history_detail(self, request, pk=None, *args, **kwargs):
        tag = EnumTag.objects.get(pk=pk)
        serializer = EnumTagHistorySerializer(tag, context={'request': request})
        return Response(serializer.data)

@permissions(
"""
ppp : admin, proxy;
get : user;
""")
class EnumViewSet(viewsets.ModelViewSet):
    queryset = Enum.objects.all()
    serializer_class = EnumSerializer
