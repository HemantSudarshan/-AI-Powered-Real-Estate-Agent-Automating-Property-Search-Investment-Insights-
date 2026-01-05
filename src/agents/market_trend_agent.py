"""Market Trend Analyzer Agent - Analyzes real estate market trends."""
from typing import Dict, Any, List
import google.generativeai as genai
from src.agents.base_agent import BaseAgent
from src.utils.config import get_settings
import asyncio
import json


class MarketTrendAgent(BaseAgent):
    """Agent for analyzing real estate market trends."""
    
    def __init__(self, gemini_key: str = None):
        """
        Initialize market trend agent.
        
        Args:
            gemini_key: Optional Gemini API key (falls back to settings)
        """
        super().__init__("market_trend_agent")
        
        settings = get_settings()
        gemini_api_key = gemini_key or settings.gemini_api_key
        
        if not gemini_api_key:
            self.logger.warning("Gemini API key not configured")
        
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel("gemini-pro")
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze market trends for a city/region.
        
        Args:
            input_data: Dictionary containing:
                - city: str
                - property_type: str
                - timeframe: str ('6months', '1year', '3years')
        
        Returns:
            Dictionary containing:
                - price_trend: str ('rising', 'stable', 'declining')
                - demand_level: str ('high', 'medium', 'low')
                - growth_prediction: float (percentage)
                - hot_areas: List[str]
                - insights: str (detailed analysis)
        """
        city = input_data.get('city', '')
        property_type = input_data.get('property_type', 'all')
        timeframe = input_data.get('timeframe', '1year')
        
        self.logger.info(f"Analyzing market trends for {city}, type: {property_type}, timeframe: {timeframe}")
        
        prompt = f"""As a real estate market analyst specializing in Indian property markets, analyze the market trends for:

City: {city}
Property Type: {property_type}
Analysis Timeframe: {timeframe}

Provide a comprehensive market analysis in the following JSON format:
{{
    "price_trend": "<string: 'rising', 'stable', or 'declining'>",
    "demand_level": "<string: 'high', 'medium', or 'low'>",
    "growth_prediction": <float: expected growth percentage over the timeframe>,
    "hot_areas": ["<area1>", "<area2>", "<area3>"],
    "insights": "<string: detailed 4-5 sentence analysis covering current market conditions, supply-demand dynamics, infrastructure developments, price trends, and investment outlook>"
}}

Consider:
- Recent price movements and historical trends
- Supply vs demand dynamics
- New infrastructure projects (metro, IT parks, airports)
- Job market and migration patterns
- Government policies and regulations
- Upcoming developments

Respond ONLY with valid JSON, no additional text."""

        try:
            response = await asyncio.to_thread(
                lambda: self.model.generate_content(prompt)
            )
            
            if response and hasattr(response, 'text'):
                # Parse JSON response
                result_text = response.text.strip()
                
                # Remove markdown code blocks if present
                if result_text.startswith('```'):
                    result_text = result_text.split('```')[1]
                    if result_text.startswith('json'):
                        result_text = result_text[4:]
                    result_text = result_text.strip()
                
                result = json.loads(result_text)
                
                self.logger.info(f"Market trend analysis complete: {result.get('price_trend', 'N/A')}")
                self.log_execution(input_data, result)
                
                return result
            else:
                self.logger.warning("No valid response from Gemini")
                return self._get_default_trends()
                
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {e}")
            return self._get_default_trends()
        except Exception as e:
            self.logger.error(f"Market trend analysis failed: {e}", exc_info=True)
            return self._get_default_trends()
    
    def _get_default_trends(self) -> Dict[str, Any]:
        """Return default trends when AI fails."""
        return {
            'price_trend': 'stable',
            'demand_level': 'medium',
            'growth_prediction': 0.0,
            'hot_areas': [],
            'insights': 'Unable to generate market trend analysis. Please try again or consult with a real estate market analyst.'
        }
