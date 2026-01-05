"""Configuration management using Pydantic settings."""
from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # API Keys
    gemini_api_key: str = ""
    firecrawl_api_key: str = ""
    
    # Database
    database_url: str = "sqlite:///./real_estate.db"
    
    # Redis & Caching
    redis_url: str = "redis://localhost:6379/0"
    enable_cache: bool = True
    cache_ttl_search: int = 3600  # 1 hour
    cache_ttl_analysis: int = 86400  # 24 hours
    cache_ttl_trends: int = 43200  # 12 hours
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
