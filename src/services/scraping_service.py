"""Firecrawl web scraping service."""
import asyncio
from typing import List, Dict
from firecrawl import FirecrawlApp
from src.schemas.property import PropertiesResponse
from src.utils.logger import setup_logger


class ScrapingService:
    """Service for scraping property data using Firecrawl."""
    
    def __init__(self, api_key: str):
        """
        Initialize scraping service.
        
        Args:
            api_key: Firecrawl API key
        """
        self.firecrawl = FirecrawlApp(api_key=api_key)
        self.logger = setup_logger("services.scraping")
    
    async def fetch_properties(
        self,
        city: str,
        max_price: float,
        property_type: str
    ) -> List[Dict]:
        """
        Fetch property listings from multiple sources.
        
        Args:
            city: City name
            max_price: Maximum price in crores
            property_type: Type of property (Flat, Individual House, etc.)
        
        Returns:
            List of property dictionaries
        """
        urls = [
            f"https://www.squareyards.com/sale/property-for-sale-in-{city.lower()}/*",
            f"https://www.99acres.com/property-in-{city.lower()}-ffid/*",
            f"https://housing.com/in/buy/{city.lower()}/{city.lower()}"
        ]
        
        try:
            self.logger.info(f"Fetching properties for {city}, type: {property_type}, max price: {max_price} crores")
            
            response = await asyncio.to_thread(
                self.firecrawl.extract,
                urls,
                params={
                    'prompt': f"Extract up to 10 {property_type} properties under {max_price} crores in {city}.",
                    'schema': PropertiesResponse.model_json_schema()
                }
            )
            
            self.logger.info(f"Raw Firecrawl Response: {response}")
            
            if response.get('success'):
                properties = response['data'].get('properties', [])
                self.logger.info(f"Successfully fetched {len(properties)} properties")
                return properties
            else:
                self.logger.warning(f"Firecrawl response not successful: {response}")
                
        except Exception as e:
            self.logger.error(f"Error fetching properties: {e}", exc_info=True)
        
        return []
