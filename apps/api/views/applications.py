from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_date
from django.db.models import DateField
from django.db.models.functions import Cast

from apps.api.serializers.applications import (
    ApplicationCreateSerializer,
    ApplicationSerializer,
    ApplicationStatusListSerializer,
    ApplicationStatusUpdateSerializer,
    ApplicationUpdateSerializer
)
from apps.application.models import Application, ApplicationStatus
from apps.users.models import CustomUser
from apps.api.cache_tools.application_cache import (
    get_cached_application_list, 
    cache_application_list,
    invalidate_application_caches,
    application_cache
)

class ApplicationAPIView(APIView):
    def get(self, request, *args, **kwargs):
        dept = request.query_params.get('department')
        user = request.query_params.get('user')
        created_after = request.query_params.get('created_after')
        created_before = request.query_params.get('created_before')
        
        # Пробуем получить из кеша
        cached_data = get_cached_application_list(dept, created_after, created_before, user)
        if cached_data is not None:
            return Response(cached_data)

        # Если нет в кеше, выполняем запрос
        qs = Application.objects.all().order_by('-date')
        
        if dept is not None:
            qs = qs.filter(form__department_id=dept)
        if user is not None:
            qs = qs.filter(user_id=user)
            
        after_date = parse_date(created_after) if created_after else None
        before_date = parse_date(created_before) if created_before else None
        
        if after_date:
            qs = qs.annotate(date_only=Cast('date', DateField())).filter(date_only__gte=after_date)
        if before_date:
            qs = qs.annotate(date_only=Cast('date', DateField())).filter(date_only__lte=before_date)
            
        out = ApplicationSerializer(qs, many=True)
        
        # Сохраняем в кеш
        cache_application_list(out.data, dept, created_after, created_before, user)
        
        return Response(out.data)

    def post(self, request, *args, **kwargs):
        serializer = ApplicationCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            app = serializer.save()
            
            # Инвалидируем весь кеш заявок при создании новой
            invalidate_application_caches(app)
            
            out = ApplicationSerializer(app)
            return Response(out.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApplicationRetrieveUpdateAPIView(APIView):
    def get(self, request, id, *args, **kwargs):
        # Кешируем отдельные заявки
        cache_key = ['detail', id]
        cached_data = application_cache.get(*cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
            
        app = get_object_or_404(Application, pk=id)
        out = ApplicationSerializer(app)
        
        # Сохраняем в кеш
        application_cache.set(out.data, *cache_key)
        
        return Response(out.data)

    def patch(self, request, id, *args, **kwargs):
        app = get_object_or_404(Application, pk=id)
        serializer = ApplicationUpdateSerializer(app, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            
            # Инвалидируем весь кеш при изменении заявки
            invalidate_application_caches(app)
            
            out = ApplicationSerializer(app)
            return Response(out.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApplicationStatusListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        items = [{'key': c.name, 'label': c.label} for c in ApplicationStatus]
        out = ApplicationStatusListSerializer(items, many=True)
        return Response(out.data)

class ApplicationStatusUpdateAPIView(APIView):
    def patch(self, request, id, *args, **kwargs):
        app = get_object_or_404(Application, pk=id)
        serializer = ApplicationStatusUpdateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        app.status = serializer.validated_data['status']
        app.save(update_fields=['status'])
        
        # Инвалидируем весь кеш при смене статуса
        invalidate_application_caches(app)
        
        out = ApplicationSerializer(app)
        return Response(out.data)