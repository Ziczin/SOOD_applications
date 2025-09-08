from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.forms.models import EnumTag, Enum
from apps.api.serializers.enums import EnumTagSerializer, EnumSerializer

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Q

class EnumTagViewSet(viewsets.ModelViewSet):
    queryset = EnumTag.objects.all()
    serializer_class = EnumTagSerializer

    def get_queryset(self):
        user = self.request.user
        dept = user.department(user)
        qs = EnumTag.objects.filter(available=True)
        if dept is not None:
            return qs.filter(Q(department=dept) | Q(shared=True))
        return qs.filter(shared=True)

    def perform_create(self, serializer):
        user = self.request.user
        dept = user.department(user)
        with transaction.atomic():
            if dept is not None:
                serializer.save(department=dept)
            else:
                serializer.save()

    @action(detail=True, methods=['get'], url_path='items')
    def items_list(self, request, pk=None):
        tag = self.get_object()
        qs = tag.enums.filter(available=True)
        serializer = EnumSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='items')
    def items_create(self, request, pk=None):
        tag = self.get_object()
        data = request.data.copy()
        data['enum_tag'] = tag.id
        serializer = EnumSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        obj = serializer.save()
        return Response(EnumSerializer(obj).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'put', 'patch', 'delete'], url_path='items/(?P<item_pk>[^/.]+)', url_name='item-detail')
    def item_detail(self, request, pk=None, item_pk=None):
        tag = self.get_object()
        obj = get_object_or_404(Enum, pk=item_pk, enum_tag=tag)
        if request.method == 'GET':
            return Response(EnumSerializer(obj).data)
        if request.method in ('PUT', 'PATCH'):
            partial = request.method == 'PATCH'
            serializer = EnumSerializer(obj, data=request.data, partial=partial)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            obj = serializer.save()
            return Response(EnumSerializer(obj).data)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EnumViewSet(viewsets.ModelViewSet):
    queryset = Enum.objects.all()
    serializer_class = EnumSerializer
