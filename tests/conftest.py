"""Pytest configuration and fixtures for AI Real Estate Agent tests."""
import os
import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set test environment variables before importing app modules
os.environ["GEMINI_API_KEY"] = "test_api_key"
os.environ["FIRECRAWL_API_KEY"] = "test_api_key"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["ENABLE_CACHE"] = "false"

from src.database.models import Base
from src.database.session import get_session


@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(test_engine):
    """Create a new database session for each test."""
    Session = sessionmaker(bind=test_engine)
    session = Session()
    
    # Start a transaction
    connection = test_engine.connect()
    transaction = connection.begin()
    
    yield session
    
    # Rollback the transaction after test
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def mock_gemini_client():
    """Mock the Gemini AI client."""
    with patch("google.generativeai.GenerativeModel") as mock:
        mock_instance = MagicMock()
        mock_instance.generate_content.return_value = MagicMock(
            text="Mock AI response for property analysis"
        )
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_firecrawl_client():
    """Mock the Firecrawl scraping client."""
    with patch("firecrawl.FirecrawlApp") as mock:
        mock_instance = MagicMock()
        mock_instance.scrape_url.return_value = {
            "content": "Sample property listing content",
            "metadata": {"title": "Test Property"}
        }
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_redis():
    """Mock Redis client for cache testing."""
    with patch("redis.Redis") as mock:
        mock_instance = MagicMock()
        mock_instance.get.return_value = None
        mock_instance.set.return_value = True
        mock_instance.ping.return_value = True
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def sample_property_data():
    """Sample property data for testing."""
    return {
        "title": "3 BHK Apartment in Bangalore",
        "price": 8500000.0,
        "location": "Whitefield, Bangalore",
        "property_type": "Flat",
        "bedrooms": 3,
        "bathrooms": 2,
        "area_sqft": 1500.0,
        "amenities": ["Gym", "Swimming Pool", "Parking"],
        "description": "Beautiful apartment with modern amenities",
        "source_url": "https://example.com/property/123",
        "city": "Bangalore"
    }


@pytest.fixture
def sample_search_params():
    """Sample search parameters for testing."""
    return {
        "city": "Bangalore",
        "property_type": "Flat",
        "max_price": 10000000.0
    }
