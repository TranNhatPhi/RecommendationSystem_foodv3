"""
Cache Manager for AI Agent System
Implements intelligent caching for improved performance
"""

import json
import time
import hashlib
from typing import Dict, Any, Optional
from functools import wraps
import os


class CacheManager:
    def __init__(self, cache_dir: str = "cache", max_cache_size: int = 1000):
        """Initialize cache manager"""
        self.cache_dir = cache_dir
        self.max_cache_size = max_cache_size
        self.cache = {}
        self.access_times = {}

        # Create cache directory
        os.makedirs(cache_dir, exist_ok=True)

        # Load existing cache
        self._load_cache()

    def _generate_key(self, data: Any) -> str:
        """Generate cache key from data"""
        if isinstance(data, dict):
            data_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
        else:
            data_str = str(data)

        return hashlib.md5(data_str.encode('utf-8')).hexdigest()

    def _load_cache(self):
        """Load cache from disk"""
        cache_file = os.path.join(self.cache_dir, "agent_cache.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                    self.cache = cached_data.get('cache', {})
                    self.access_times = cached_data.get('access_times', {})
                print(f"✅ Loaded {len(self.cache)} cached items")
            except Exception as e:
                print(f"⚠️ Could not load cache: {e}")

    def _save_cache(self):
        """Save cache to disk"""
        cache_file = os.path.join(self.cache_dir, "agent_cache.json")
        try:
            cache_data = {
                'cache': self.cache,
                'access_times': self.access_times,
                'timestamp': time.time()
            }
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save cache: {e}")

    def _cleanup_cache(self):
        """Remove least recently used items if cache is full"""
        if len(self.cache) >= self.max_cache_size:
            # Sort by access time, remove oldest
            sorted_items = sorted(
                self.access_times.items(), key=lambda x: x[1])
            items_to_remove = len(sorted_items) - self.max_cache_size + 10

            for key, _ in sorted_items[:items_to_remove]:
                if key in self.cache:
                    del self.cache[key]
                del self.access_times[key]

            print(f"🧹 Cleaned up {items_to_remove} old cache items")

    def get(self, key: str, default=None):
        """Get item from cache"""
        cache_key = self._generate_key(key)

        if cache_key in self.cache:
            self.access_times[cache_key] = time.time()
            return self.cache[cache_key]

        return default

    def set(self, key: str, value: Any, expire_hours: int = 24):
        """Set item in cache"""
        cache_key = self._generate_key(key)

        # Check if cache needs cleanup
        self._cleanup_cache()

        cache_item = {
            'value': value,
            'timestamp': time.time(),
            'expire_hours': expire_hours
        }

        self.cache[cache_key] = cache_item
        self.access_times[cache_key] = time.time()

        # Save cache periodically
        if len(self.cache) % 10 == 0:
            self._save_cache()

    def is_expired(self, cache_item: Dict) -> bool:
        """Check if cache item is expired"""
        expire_time = cache_item['timestamp'] + \
            (cache_item['expire_hours'] * 3600)
        return time.time() > expire_time

    def clear_expired(self):
        """Clear expired cache items"""
        expired_keys = []

        for key, item in self.cache.items():
            if self.is_expired(item):
                expired_keys.append(key)

        for key in expired_keys:
            del self.cache[key]
            if key in self.access_times:
                del self.access_times[key]

        if expired_keys:
            print(f"🧹 Cleared {len(expired_keys)} expired cache items")
            self._save_cache()

    def get_stats(self) -> Dict:
        """Get cache statistics"""
        return {
            'total_items': len(self.cache),
            'max_size': self.max_cache_size,
            'usage_percent': (len(self.cache) / self.max_cache_size) * 100,
            'last_cleanup': min(self.access_times.values()) if self.access_times else 0
        }


# Global cache instance
cache_manager = CacheManager()


def cached(expire_hours: int = 24):
    """Decorator for caching function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"

            # Try to get from cache
            cached_result = cache_manager.get(cache_key)
            if cached_result and not cache_manager.is_expired(cached_result):
                return cached_result['value']

            # Execute function and cache result
            result = func(*args, **kwargs)
            cache_manager.set(cache_key, result, expire_hours)

            return result
        return wrapper
    return decorator


def clear_cache():
    """Clear all cache"""
    cache_manager.cache = {}
    cache_manager.access_times = {}
    cache_manager._save_cache()
    print("🧹 Cache cleared")


if __name__ == "__main__":
    # Test cache manager
    cache = CacheManager()

    # Test basic operations
    cache.set("test_key", {"data": "test_value"})
    result = cache.get("test_key")
    print(f"Cache test: {result}")

    # Test stats
    stats = cache.get_stats()
    print(f"Cache stats: {stats}")
