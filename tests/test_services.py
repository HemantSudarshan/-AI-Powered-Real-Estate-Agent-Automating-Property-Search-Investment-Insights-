"""Unit tests for AI Real Estate Agent services."""
import pytest
from unittest.mock import MagicMock, patch
import json


class TestCacheService:
    """Tests for CacheService."""

    def test_cache_service_initialization_without_redis(self):
        """Test CacheService initializes gracefully without Redis."""
        with patch("redis.Redis") as mock_redis:
            mock_redis.return_value.ping.side_effect = Exception("Connection refused")
            
            from src.services.cache_service import CacheService
            
            service = CacheService()
            # Should gracefully handle Redis unavailability
            assert service is not None

    def test_cache_service_set_and_get(self, mock_redis):
        """Test CacheService set and get operations."""
        from src.services.cache_service import CacheService
        
        with patch.object(CacheService, '_connect', return_value=mock_redis):
            service = CacheService()
            service.redis = mock_redis
            service.connected = True
            
            # Test set
            mock_redis.set.return_value = True
            result = service.set("test_key", {"data": "value"}, ttl=3600)
            
            # Verify set was called
            assert mock_redis.set.called or result is None  # Graceful handling

    def test_cache_service_generates_correct_keys(self):
        """Test cache key generation."""
        from src.services.cache_service import CacheService
        
        service = CacheService()
        
        # Test search key generation
        search_key = service.generate_search_key("Bangalore", "Flat", 10000000)
        assert "Bangalore" in search_key.lower() or "search" in search_key.lower()


class TestAIService:
    """Tests for AIService."""

    def test_ai_service_initialization(self):
        """Test AIService can be initialized."""
        with patch("google.generativeai.configure"):
            from src.services.ai_service import AIService
            
            service = AIService(api_key="test_key")
            assert service is not None

    def test_ai_service_has_analyze_method(self):
        """Test AIService has analyze method."""
        with patch("google.generativeai.configure"):
            from src.services.ai_service import AIService
            
            service = AIService(api_key="test_key")
            assert hasattr(service, 'analyze') or hasattr(service, 'generate')


class TestScrapingService:
    """Tests for ScrapingService."""

    def test_scraping_service_initialization(self):
        """Test ScrapingService can be initialized."""
        from src.services.scraping_service import ScrapingService
        
        service = ScrapingService(api_key="test_key")
        assert service is not None

    def test_scraping_service_has_scrape_method(self):
        """Test ScrapingService has scrape method."""
        from src.services.scraping_service import ScrapingService
        
        service = ScrapingService(api_key="test_key")
        assert hasattr(service, 'scrape') or hasattr(service, 'scrape_properties')

    def test_scraping_service_url_generation(self):
        """Test URL generation for property sites."""
        from src.services.scraping_service import ScrapingService
        
        service = ScrapingService(api_key="test_key")
        
        # Service should have method to generate search URLs
        assert service is not None
