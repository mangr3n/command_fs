"""
Caching implementation for Command-FS.
"""
from typing import Any, Dict, Optional
import time
from threading import Lock


class Cache:
    """Simple in-memory cache with TTL."""
    
    def __init__(self, default_ttl: int = 60):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()
        self.default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache."""
        with self._lock:
            if key not in self._cache:
                return None
            
            entry = self._cache[key]
            if time.time() > entry['expires']:
                del self._cache[key]
                return None
            
            return entry['value']

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a value in the cache with TTL."""
        ttl = ttl if ttl is not None else self.default_ttl
        with self._lock:
            self._cache[key] = {
                'value': value,
                'expires': time.time() + ttl
            }

    def delete(self, key: str) -> None:
        """Delete a value from the cache."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]

    def clear(self) -> None:
        """Clear all entries from the cache."""
        with self._lock:
            self._cache.clear()

    def cleanup(self) -> None:
        """Remove expired entries from the cache."""
        with self._lock:
            now = time.time()
            expired = [
                key for key, entry in self._cache.items()
                if now > entry['expires']
            ]
            for key in expired:
                del self._cache[key]
