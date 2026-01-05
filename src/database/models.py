"""SQLAlchemy database models."""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class Property(Base):
    """Property model for storing property data."""
    
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    building_name = Column(String(200), nullable=False)
    property_type = Column(String(50), nullable=False, index=True)
    location_address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False, index=True)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    source_url = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    investment_analyses = relationship("InvestmentAnalysis", back_populates="property")
    
    def __repr__(self):
        return f"<Property(id={self.id}, name='{self.building_name}', city='{self.city}')>"


class SearchHistory(Base):
    """Search history model for tracking user searches."""
    
    __tablename__ = "search_history"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), nullable=False, index=True)
    property_type = Column(String(50), nullable=False)
    max_price = Column(Float, nullable=False)
    results_count = Column(Integer, default=0)
    timestamp = Column(DateTime, server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<SearchHistory(id={self.id}, city='{self.city}', type='{self.property_type}')>"


class InvestmentAnalysis(Base):
    """Investment analysis model for storing ROI calculations."""
    
    __tablename__ = "investment_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    
    # ROI metrics
    roi_5year = Column(Float, nullable=True)
    roi_10year = Column(Float, nullable=True)
    appreciation_rate = Column(Float, nullable=True)
    rental_yield = Column(Float, nullable=True)
    risk_score = Column(Float, nullable=True)  # 0-100
    
    # Analysis text
    recommendation = Column(String(50), nullable=True)  # 'buy', 'hold', 'avoid'
    analysis_text = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    property = relationship("Property", back_populates="investment_analyses")
    
    def __repr__(self):
        return f"<InvestmentAnalysis(id={self.id}, property_id={self.property_id}, roi_5year={self.roi_5year})>"
