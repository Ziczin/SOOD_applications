from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import EventSubscriber, CustomUser
from apps.api.serializers.events import EventSubscriberCreateSerializer, EventCheckSerializer
from datetime import timedelta
import json

class SubscribeView(APIView):
    def post(self, request):
        serializer = EventSubscriberCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        try:
            user = CustomUser.objects.get(pk=data['user_id'])
        except CustomUser.DoesNotExist:
            return Response({'detail': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        
        now = timezone.now()
        response_text = None
        
        if 'response' in data and data['response'] is not None:
            response_text = json.dumps(data['response'], ensure_ascii=False)
        
        if response_text is None:
            # Используем atomic для предотвращения race condition
            with transaction.atomic():
                existing = EventSubscriber.objects.select_for_update().filter(
                    user=user, 
                    event=data['event'], 
                    response__isnull=True
                ).first()
                
                if existing:
                    existing.last_check = now
                    existing.save(update_fields=['last_check'])
                    return Response({'id': existing.id}, status=status.HTTP_200_OK)
                
                es = EventSubscriber.objects.create(
                    user=user,
                    event=data['event'],
                    response=None,
                    last_check=now
                )
                return Response({'id': es.id}, status=status.HTTP_201_CREATED)
        else:
            es = EventSubscriber.objects.create(
                user=user,
                event=data['event'],
                response=response_text,
                last_check=now
            )
            return Response({'id': es.id}, status=status.HTTP_201_CREATED)

class UnsubscribeView(APIView):
    def post(self, request):
        serializer = EventSubscriberCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        # Удаляем только целевые подписки
        deleted_count, _ = EventSubscriber.objects.filter(
            user_id=data['user_id'],
            event=data['event']
        ).delete()
        
        # Очистку старых записей лучше вынести в отдельную задачу (celery/cron)
        # cutoff = timezone.now() - timedelta(minutes=10)
        # EventSubscriber.objects.filter(last_check__lt=cutoff).delete()
        
        return Response({'deleted': True, 'count': deleted_count}, status=status.HTTP_200_OK)

class CheckView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        event = request.query_params.get('event')
        
        if not user_id or not event:
            return Response(
                {'detail': 'user_id and event required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

        now = timezone.now()
        
        with transaction.atomic():
            # Более эффективный запрос
            obj = EventSubscriber.objects.select_for_update().filter(
                user=user, 
                event=event
            ).order_by('last_check').first()
            
            if not obj:
                EventSubscriber.objects.create(
                    user=user,
                    event=event,
                    response=None,
                    last_check=now
                )
                return Response({'response': None}, status=status.HTTP_200_OK)
            
            if not obj.response:
                obj.last_check = now
                obj.save(update_fields=['last_check'])
                return Response({'response': None}, status=status.HTTP_200_OK)
            
            try:
                payload = json.loads(obj.response)
            except Exception as e:
                # Логируем ошибку для отладки
                print(f"Error parsing JSON response: {e}")
                payload = None
            
            obj.delete()
            return Response({'response': payload}, status=status.HTTP_200_OK)