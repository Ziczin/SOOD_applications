from django.utils.dateparse import parse_date
from apps.application.models import Application
from .helper import CacheHelper

application_cache = CacheHelper('applications', ttl=3600)

def invalidate_application_caches(application: Application):
    """
    Инвалидирует все кеши заявок при изменении заявки
    """
    # Удаляем все кеши списков заявок
    application_cache.delete_pattern('list')
    
    # Удаляем кеш конкретной заявки
    application_cache.delete('detail', application.id)

def get_application_cache_key(dept: str = None, created_after: str = None, 
                            created_before: str = None, user: str = None) -> list:
    """
    Формирует ключ кеша для списка заявок на основе параметров фильтрации
    """
    return ['list', dept, created_after, created_before, user]

def cache_application_list(data, dept: str = None, created_after: str = None,
                          created_before: str = None, user: str = None):
    """
    Сохраняет список заявок в кеш
    """
    cache_key = get_application_cache_key(dept, created_after, created_before, user)
    application_cache.set(data, *cache_key)

def get_cached_application_list(dept: str = None, created_after: str = None,
                               created_before: str = None, user: str = None):
    """
    Получает список заявок из кеша
    """
    cache_key = get_application_cache_key(dept, created_after, created_before, user)
    return application_cache.get(*cache_key)