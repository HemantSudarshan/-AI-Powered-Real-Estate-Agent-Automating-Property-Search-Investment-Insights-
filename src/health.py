"""Health check endpoint for monitoring and container orchestration."""
import sys
from datetime import datetime
from typing import Any

from src.database.session import get_session
from src.utils.config import get_settings


def check_database() -> dict[str, Any]:
    """Check database connectivity."""
    try:
        session = get_session()
        session.execute("SELECT 1")
        session.close()
        return {"status": "healthy", "latency_ms": 0}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


def check_redis() -> dict[str, Any]:
    """Check Redis connectivity."""
    settings = get_settings()
    if not settings.enable_cache:
        return {"status": "disabled"}
    
    try:
        import redis
        client = redis.from_url(settings.redis_url)
        start = datetime.now()
        client.ping()
        latency = (datetime.now() - start).total_seconds() * 1000
        return {"status": "healthy", "latency_ms": round(latency, 2)}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


def get_health_status() -> dict[str, Any]:
    """Get overall health status of the application."""
    settings = get_settings()
    
    health = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "python_version": sys.version,
        "checks": {
            "database": check_database(),
            "redis": check_redis(),
        },
        "config": {
            "cache_enabled": settings.enable_cache,
            "log_level": settings.log_level,
        }
    }
    
    # Determine overall status
    for check_name, check_result in health["checks"].items():
        if check_result.get("status") == "unhealthy":
            health["status"] = "degraded"
            break
    
    return health


def run_health_check() -> bool:
    """Run health check and return True if healthy."""
    try:
        status = get_health_status()
        return status["status"] in ("healthy", "degraded")
    except Exception:
        return False


if __name__ == "__main__":
    # CLI health check
    status = get_health_status()
    print(f"Health Status: {status['status']}")
    for check_name, check_result in status["checks"].items():
        print(f"  {check_name}: {check_result['status']}")
    
    sys.exit(0 if status["status"] in ("healthy", "degraded") else 1)
