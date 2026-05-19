import time
from typing import Any, Optional, Dict, Tuple

class TTLCache:
    def __init__(self, default_ttl: int = 60):
        self.default_ttl = default_ttl
        self._store: Dict[str, Tuple[Any, float]] = {}

    def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if entry:
            value, expires_at = entry
            if time.time() < expires_at:
                return value
            del self._store[key]
        return None

    def set(self, key: str, value: Any, ttl: int = None):
        self._store[key] = (value, time.time() + (ttl or self.default_ttl))

    def delete(self, key: str):
        self._store.pop(key, None)

    def clear(self):
        self._store.clear()

# Sdílené instance
progress_cache = TTLCache(default_ttl=60)   # pokrok studenta: 60 s
