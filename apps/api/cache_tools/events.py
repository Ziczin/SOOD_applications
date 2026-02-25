from datetime import timezone
import json
from django.core.cache import cache

from apps.users.models import EventSubscriber


def clear_event_related_cache(user_id, event):
    """Очистить кеш, связанный с событием"""
    cache_keys = [
        f"event_subscriber_{user_id}_{event}",
        f"event_check_{user_id}_{event}",
    ]
    for key in cache_keys:
        cache.delete(key)


def set_event_response(event, other, response):
    now = timezone.now()
    if response is None:
        response_text = None
    else:
        response_text = json.dumps(response, ensure_ascii=False)

    EventSubscriber.objects.filter(event=event, other=other).update(
        response=response_text, last_check=now
    )
