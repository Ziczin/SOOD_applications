from django.core.cache import cache

def clear_event_related_cache(user_id, event):
    """Очистить кеш, связанный с событием"""
    cache_keys = [
        f"event_subscriber_{user_id}_{event}",
        f"event_check_{user_id}_{event}",
    ]
    for key in cache_keys:
        cache.delete(key)