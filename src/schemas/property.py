"""Pydantic schemas for property data validation."""
from pydantic import BaseModel, Field
from typing import List


class PropertyData(BaseModel):
    """Schema for individual property data."""
    
    building_name: str = Field(description="Name of the building/property")
    property_type: str = Field(description="Type of property (commercial, residential, etc)")
    location_address: str = Field(description="Complete address of the property")
    price: str = Field(description="Price of the property")
    description: str = Field(description="Detailed description of the property")


class PropertiesResponse(BaseModel):
    """Schema for multiple properties response."""
    
    properties: List[PropertyData]
