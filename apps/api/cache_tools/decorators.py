from django.core.cache import cache
from functools import wraps
from rest_framework import response

def cache_method(key_pattern, timeout=900):
    def decorator(method):
        @wraps(method)
        def wrapper(self, request, *args, **kwargs):
            # Формируем ключ кеша
            cache_key = key_pattern.format(
                **kwargs,
                user_id=getattr(request.user, 'pk', None)
            )
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return response.Response(cached_data)
            
            result = method(self, request, *args, **kwargs)
            # Извлекаем данные из Response для кеширования
            if hasattr(result, 'data'):
                data_to_cache = result.data
            else:
                data_to_cache = result
                
            cache.set(cache_key, data_to_cache, timeout)
            return result
        return wrapper
    return decorator

def invalidate_cache(key_patterns):
    def decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            result = method(self, *args, **kwargs)
            
            # Получаем ID объекта если есть
            obj_id = None
            if hasattr(result, 'id'):
                obj_id = result.id
            elif 'pk' in kwargs:
                obj_id = kwargs['pk']
            elif len(args) > 0:
                obj_id = args[0]
            
            for pattern in key_patterns:
                if '{id}' in pattern and obj_id:
                    cache.delete(pattern.format(id=obj_id))
                else:
                    cache.delete(pattern)
            return result
        return wrapper
    return decorator