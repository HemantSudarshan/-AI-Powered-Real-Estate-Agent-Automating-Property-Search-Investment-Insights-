"""CRUD operations for database models."""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime

from src.database.models import Property, SearchHistory, InvestmentAnalysis
from src.utils.logger import setup_logger

logger = setup_logger("database.crud")


class PropertyCRUD:
    """CRUD operations for Property model."""
    
    @staticmethod
    def create(db: Session, property_data: Dict[str, Any]) -> Property:
        """Create a new property."""
        property_obj = Property(**property_data)
        db.add(property_obj)
        db.commit()
        db.refresh(property_obj)
        logger.info(f"Created property: {property_obj.id}")
        return property_obj
    
    @staticmethod
    def get_by_id(db: Session, property_id: int) -> Optional[Property]:
        """Get property by ID."""
        return db.query(Property).filter(Property.id == property_id).first()
    
    @staticmethod
    def get_by_city(db: Session, city: str, limit: int = 100) -> List[Property]:
        """Get properties by city."""
        return db.query(Property).filter(Property.city == city).limit(limit).all()
    
    @staticmethod
    def search(
        db: Session,
        city: Optional[str] = None,
        property_type: Optional[str] = None,
        max_price: Optional[float] = None,
        limit: int = 100
    ) -> List[Property]:
        """Search properties with filters."""
        query = db.query(Property)
        
        if city:
            query = query.filter(Property.city == city)
        if property_type:
            query = query.filter(Property.property_type == property_type)
        if max_price:
            query = query.filter(Property.price <= max_price)
        
        return query.order_by(desc(Property.created_at)).limit(limit).all()
    
    @staticmethod
    def update(db: Session, property_id: int, updates: Dict[str, Any]) -> Optional[Property]:
        """Update property."""
        property_obj = PropertyCRUD.get_by_id(db, property_id)
        if property_obj:
            for key, value in updates.items():
                setattr(property_obj, key, value)
            db.commit()
            db.refresh(property_obj)
            logger.info(f"Updated property: {property_id}")
        return property_obj
    
    @staticmethod
    def delete(db: Session, property_id: int) -> bool:
        """Delete property."""
        property_obj = PropertyCRUD.get_by_id(db, property_id)
        if property_obj:
            db.delete(property_obj)
            db.commit()
            logger.info(f"Deleted property: {property_id}")
            return True
        return False


class SearchHistoryCRUD:
    """CRUD operations for SearchHistory model."""
    
    @staticmethod
    def create(
        db: Session,
        city: str,
        property_type: str,
        max_price: float,
        results_count: int
    ) -> SearchHistory:
        """Create search history entry."""
        search = SearchHistory(
            city=city,
            property_type=property_type,
            max_price=max_price,
            results_count=results_count
        )
        db.add(search)
        db.commit()
        db.refresh(search)
        logger.info(f"Created search history: {search.id}")
        return search
    
    @staticmethod
    def get_recent(db: Session, limit: int = 10) -> List[SearchHistory]:
        """Get recent searches."""
        return db.query(SearchHistory).order_by(desc(SearchHistory.timestamp)).limit(limit).all()
    
    @staticmethod
    def get_by_city(db: Session, city: str, limit: int = 10) -> List[SearchHistory]:
        """Get search history for a city."""
        return (
            db.query(SearchHistory)
            .filter(SearchHistory.city == city)
            .order_by(desc(SearchHistory.timestamp))
            .limit(limit)
            .all()
        )


class InvestmentAnalysisCRUD:
    """CRUD operations for InvestmentAnalysis model."""
    
    @staticmethod
    def create(db: Session, analysis_data: Dict[str, Any]) -> InvestmentAnalysis:
        """Create investment analysis."""
        analysis = InvestmentAnalysis(**analysis_data)
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        logger.info(f"Created investment analysis: {analysis.id} for property: {analysis.property_id}")
        return analysis
    
    @staticmethod
    def get_by_property_id(db: Session, property_id: int) -> Optional[InvestmentAnalysis]:
        """Get latest investment analysis for a property."""
        return (
            db.query(InvestmentAnalysis)
            .filter(InvestmentAnalysis.property_id == property_id)
            .order_by(desc(InvestmentAnalysis.created_at))
            .first()
        )
    
    @staticmethod
    def get_all_for_property(db: Session, property_id: int) -> List[InvestmentAnalysis]:
        """Get all investment analyses for a property."""
        return (
            db.query(InvestmentAnalysis)
            .filter(InvestmentAnalysis.property_id == property_id)
            .order_by(desc(InvestmentAnalysis.created_at))
            .all()
        )
