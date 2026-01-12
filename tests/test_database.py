"""Unit tests for database models and CRUD operations."""
import pytest
from datetime import datetime


class TestPropertyModel:
    """Tests for Property model."""

    def test_property_creation(self, db_session, sample_property_data):
        """Test creating a property in the database."""
        from src.database.models import Property
        
        property_obj = Property(
            title=sample_property_data["title"],
            price=sample_property_data["price"],
            location=sample_property_data["location"],
            property_type=sample_property_data["property_type"],
            bedrooms=sample_property_data["bedrooms"],
            bathrooms=sample_property_data["bathrooms"],
            area_sqft=sample_property_data["area_sqft"],
            city=sample_property_data["city"],
            source_url=sample_property_data["source_url"]
        )
        
        db_session.add(property_obj)
        db_session.commit()
        
        assert property_obj.id is not None
        assert property_obj.title == sample_property_data["title"]

    def test_property_query_by_city(self, db_session, sample_property_data):
        """Test querying properties by city."""
        from src.database.models import Property
        
        # Create property
        property_obj = Property(
            title=sample_property_data["title"],
            price=sample_property_data["price"],
            location=sample_property_data["location"],
            property_type=sample_property_data["property_type"],
            city=sample_property_data["city"],
            source_url=sample_property_data["source_url"]
        )
        db_session.add(property_obj)
        db_session.commit()
        
        # Query by city
        results = db_session.query(Property).filter_by(city="Bangalore").all()
        assert len(results) >= 1


class TestSearchHistoryModel:
    """Tests for SearchHistory model."""

    def test_search_history_creation(self, db_session, sample_search_params):
        """Test creating a search history record."""
        from src.database.models import SearchHistory
        
        history = SearchHistory(
            city=sample_search_params["city"],
            property_type=sample_search_params["property_type"],
            max_price=sample_search_params["max_price"],
            results_count=10
        )
        
        db_session.add(history)
        db_session.commit()
        
        assert history.id is not None
        assert history.city == "Bangalore"


class TestInvestmentAnalysisModel:
    """Tests for InvestmentAnalysis model."""

    def test_investment_analysis_creation(self, db_session, sample_property_data):
        """Test creating an investment analysis."""
        from src.database.models import Property, InvestmentAnalysis
        
        # Create property first
        property_obj = Property(
            title=sample_property_data["title"],
            price=sample_property_data["price"],
            location=sample_property_data["location"],
            property_type=sample_property_data["property_type"],
            city=sample_property_data["city"],
            source_url=sample_property_data["source_url"]
        )
        db_session.add(property_obj)
        db_session.commit()
        
        # Create investment analysis
        analysis = InvestmentAnalysis(
            property_id=property_obj.id,
            roi_5yr=45.5,
            roi_10yr=85.0,
            recommendation="Buy",
            risk_score=25
        )
        db_session.add(analysis)
        db_session.commit()
        
        assert analysis.id is not None
        assert analysis.recommendation == "Buy"


class TestPropertyCRUD:
    """Tests for Property CRUD operations."""

    def test_create_property(self, db_session, sample_property_data):
        """Test CRUD create operation."""
        from src.database.crud import PropertyCRUD
        
        crud = PropertyCRUD(db_session)
        property_obj = crud.create(**sample_property_data)
        
        assert property_obj is not None
        assert property_obj.title == sample_property_data["title"]

    def test_get_properties_by_city(self, db_session, sample_property_data):
        """Test CRUD get by city operation."""
        from src.database.crud import PropertyCRUD
        
        crud = PropertyCRUD(db_session)
        crud.create(**sample_property_data)
        
        properties = crud.get_by_city("Bangalore")
        assert len(properties) >= 1


class TestSearchHistoryCRUD:
    """Tests for SearchHistory CRUD operations."""

    def test_create_search_history(self, db_session, sample_search_params):
        """Test creating search history via CRUD."""
        from src.database.crud import SearchHistoryCRUD
        
        crud = SearchHistoryCRUD(db_session)
        history = crud.create(
            city=sample_search_params["city"],
            property_type=sample_search_params["property_type"],
            max_price=sample_search_params["max_price"],
            results_count=5
        )
        
        assert history is not None
        assert history.city == "Bangalore"

    def test_get_recent_searches(self, db_session, sample_search_params):
        """Test getting recent search history."""
        from src.database.crud import SearchHistoryCRUD
        
        crud = SearchHistoryCRUD(db_session)
        crud.create(
            city=sample_search_params["city"],
            property_type=sample_search_params["property_type"],
            max_price=sample_search_params["max_price"],
            results_count=5
        )
        
        recent = crud.get_recent(limit=10)
        assert len(recent) >= 1
