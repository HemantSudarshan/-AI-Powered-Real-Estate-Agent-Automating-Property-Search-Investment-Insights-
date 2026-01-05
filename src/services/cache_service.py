"""Redis caching service for performance optimization."""
from typing import Optional, Any
import json
import redis
from src.utils.config import get_settings
from src.utils.logger import setup_logger


class CacheService:
    """Service for caching API responses and data using Redis."""
    
    def __init__(self, redis_url: str = None):
        """
        Initialize cache service.
        
        Args:
            redis_url: Optional Redis URL (falls back to settings)
        """
        settings = get_settings()
        self.redis_url = redis_url or settings.redis_url
        self.enabled = settings.enable_cache
        self.logger = setup_logger("services.cache")
        
        if self.enabled:
            try:
                self.redis_client = redis.from_url(
                    self.redis_url,
                    decode_responses=True,
                    socket_connect_timeout=2
                )
                # Test connection
                self.redis_client.ping()
                self.logger.info(f"Connected to Redis: {self.redis_url}")
            except (redis.ConnectionError, redis.TimeoutError) as e:
                self.logger.warning(f"Redis connection failed: {e}. Caching disabled.")
                self.enabled = False
                self.redis_client = None
        else:
            self.logger.info("Caching is disabled")
            self.redis_client = None
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None
        """
        if not self.enabled or not self.redis_client:
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                self.logger.debug(f"Cache HIT: {key}")
                return json.loads(value)
            else:
                self.logger.debug(f"Cache MISS: {key}")
                return None
        except Exception as e:
            self.logger.error(f"Cache get error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        """
        Set value in cache with TTL.
        
        Args:
            key: Cache key
            value: Value to cache (must be JSON serializable)
            ttl: Time to live in seconds
        """
        if not self.enabled or not self.redis_client:
            return
        
        try:
            serialized = json.dumps(value)
            self.redis_client.setex(key, ttl, serialized)
            self.logger.debug(f"Cache SET: {key} (TTL: {ttl}s)")
        except Exception as e:
            self.logger.error(f"Cache set error: {e}")
    
    def delete(self, key: str):
        """
        Delete key from cache.
        
        Args:
            key: Cache key to delete
        """
        if not self.enabled or not self.redis_client:
            return
        
        try:
            self.redis_client.delete(key)
            self.logger.debug(f"Cache DELETE: {key}")
        except Exception as e:
            self.logger.error(f"Cache delete error: {e}")
    
    def invalidate_pattern(self, pattern: str):
        """
        Invalidate all keys matching pattern.
        
        Args:
            pattern: Pattern to match (e.g., 'search:*')
        """
        if not self.enabled or not self.redis_client:
            return
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
                self.logger.info(f"Cache INVALIDATE: {len(keys)} keys matching '{pattern}'")
        except Exception as e:
            self.logger.error(f"Cache invalidate error: {e}")
    
    def clear_all(self):
        """Clear all cache entries."""
        if not self.enabled or not self.redis_client:
            return
        
        try:
            self.redis_client.flushdb()
            self.logger.warning("Cache CLEARED: All entries deleted")
        except Exception as e:
            self.logger.error(f"Cache clear error: {e}")
    
    @staticmethod
    def generate_key(prefix: str, **kwargs) -> str:
        """
        Generate cache key from prefix and parameters.
        
        Args:
            prefix: Key prefix (e.g., 'search', 'analysis')
            **kwargs: Parameters to include in key
        
        Returns:
            Generated cache key
        """
        parts = [prefix]
        for key, value in sorted(kwargs.items()):
            parts.append(f"{key}:{value}")
        return ":".join(parts)
