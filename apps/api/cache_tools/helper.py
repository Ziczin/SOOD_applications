from django.core.cache import cache
from typing import Optional, List


class CacheHelper:
    def __init__(self, prefix: str, ttl: int = 3600):
        self.prefix = prefix
        self.ttl = ttl
        self._index_key = f"{self.prefix}:__keys__"

    def key(self, *parts):
        parts = [str(part) for part in parts if part is not None]
        return f"{self.prefix}:" + ":".join(parts) if parts else self.prefix

    def get(self, *parts):
        return cache.get(self.key(*parts))

    def set(self, value, *parts):
        k = self.key(*parts)
        cache.set(k, value, self.ttl)
        self._register_key(k)

    def delete(self, *parts):
        k = self.key(*parts)
        cache.delete(k)
        self._unregister_key(k)

    def keys(self) -> List[str]:
        keys = cache.get(self._index_key)
        return keys if isinstance(keys, list) else []

    def delete_pattern(self, starts_with: Optional[str] = None):
        all_keys = self.keys()
        if not all_keys:
            return
        if starts_with is None:
            to_delete = [k for k in all_keys if k.startswith(f"{self.prefix}:")]
        else:
            prefix = (
                f"{self.prefix}:{starts_with}"
                if not starts_with.startswith(":")
                else f"{self.prefix}{starts_with}"
            )
            to_delete = [k for k in all_keys if k.startswith(prefix)]
        for k in to_delete:
            cache.delete(k)
            self._unregister_key(k)

    def clear(self, key: Optional[str] = None):
        all_keys = self.keys()
        if not all_keys:
            return
        if key is None:
            to_delete = [
                k
                for k in all_keys
                if k.startswith(f"{self.prefix}:")
                or k == self.prefix
                or k == self._index_key
            ]
        else:
            candidate = (
                key
                if key.startswith(self.prefix)
                else (self.key(key) if ":" in str(key) else f"{self.prefix}:{key}")
            )
            to_delete = [
                k
                for k in all_keys
                if k == candidate
                or k.startswith(candidate + ":")
                or k.startswith(candidate)
            ]
        for k in to_delete:
            cache.delete(k)
            self._unregister_key(k)

    def _register_key(self, key: str):
        keys = self.keys()
        if key not in keys:
            keys.append(key)
            cache.set(self._index_key, keys, None)

    def _unregister_key(self, key: str):
        keys = self.keys()
        if key in keys:
            keys.remove(key)
            cache.set(self._index_key, keys, None)
