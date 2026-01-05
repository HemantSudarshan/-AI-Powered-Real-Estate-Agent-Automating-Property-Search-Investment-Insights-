"""Property search agent."""
from typing import Dict, Any
from src.agents.base_agent import BaseAgent
from src.services.scraping_service import ScrapingService
from src.services.ai_service import AIService
from src.utils.config import get_settings


class SearchAgent(BaseAgent):
    """Agent for intelligent property search and analysis."""
    
    def __init__(self, gemini_key: str = None, firecrawl_key: str = None):
        """
        Initialize search agent.
        
        Args:
            gemini_key: Optional Gemini API key (falls back to settings)
            firecrawl_key: Optional Firecrawl API key (falls back to settings)
        """
        super().__init__("search_agent")
        
        settings = get_settings()
        
        # Use provided keys or fall back to settings
        gemini_api_key = gemini_key or settings.gemini_api_key
        firecrawl_api_key = firecrawl_key or settings.firecrawl_api_key
        
        if not gemini_api_key:
            self.logger.warning("Gemini API key not configured")
        
        if not firecrawl_api_key:
            self.logger.warning("Firecrawl API key not configured")
        
        self.scraping_service = ScrapingService(firecrawl_api_key)
        self.ai_service = AIService(gemini_api_key)
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute property search and analysis.
        
        Args:
            input_data: Dictionary containing:
                - city: str
                - max_price: float
                - property_type: str
        
        Returns:
            Dictionary containing:
                - properties: List of property dictionaries
                - analysis: AI-generated analysis text
        """
        city = input_data['city']
        max_price = input_data['max_price']
        property_type = input_data['property_type']
        
        self.logger.info(f"Executing search for {property_type} in {city} under {max_price} crores")
        
        # Fetch properties
        properties = await self.scraping_service.fetch_properties(
            city=city,
            max_price=max_price,
            property_type=property_type
        )
        
        # Analyze with AI
        analysis = await self.ai_service.analyze_properties(
            properties=properties,
            max_price=max_price
        )
        
        result = {
            'properties': properties,
            'analysis': analysis
        }
        
        self.log_execution(input_data, result)
        
        return result
