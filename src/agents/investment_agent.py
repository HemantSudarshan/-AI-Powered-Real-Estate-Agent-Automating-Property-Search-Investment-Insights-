"""Investment Analyzer Agent - Analyzes investment potential of properties."""
from typing import Dict, Any
import google.generativeai as genai
from src.agents.base_agent import BaseAgent
from src.utils.config import get_settings
import asyncio
import json


class InvestmentAgent(BaseAgent):
    """Agent for analyzing investment potential of properties."""
    
    def __init__(self, gemini_key: str = None):
        """
        Initialize investment agent.
        
        Args:
            gemini_key: Optional Gemini API key (falls back to settings)
        """
        super().__init__("investment_agent")
        
        settings = get_settings()
        gemini_api_key = gemini_key or settings.gemini_api_key
        
        if not gemini_api_key:
            self.logger.warning("Gemini API key not configured")
        
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel("gemini-pro")
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze investment potential of a property.
        
        Args:
            input_data: Dictionary containing:
                - property: Dict with property details
                - market_data: Optional market context
        
        Returns:
            Dictionary containing:
                - roi_5year: float
                - roi_10year: float
                - appreciation_rate: float
                - rental_yield: float
                - risk_score: float (0-100)
                - recommendation: str ('buy', 'hold', 'avoid')
                - analysis: str (detailed analysis)
        """
        property_data = input_data.get('property', {})
        market_data = input_data.get('market_data', {})
        
        self.logger.info(f"Analyzing investment potential for {property_data.get('building_name', 'Unknown')}")
        
        prompt = f"""As an experienced real estate investment analyst in India, provide a detailed investment analysis for this property:

Property Details:
- Name: {property_data.get('building_name', 'N/A')}
- Type: {property_data.get('property_type', 'N/A')}
- Location: {property_data.get('location_address', 'N/A')}
- City: {property_data.get('city', 'N/A')}
- Price: {property_data.get('price', 'N/A')}
- Description: {property_data.get('description', 'N/A')}

Provide your analysis in the following JSON format:
{{
    "roi_5year": <float: expected 5-year ROI percentage>,
    "roi_10year": <float: expected 10-year ROI percentage>,
    "appreciation_rate": <float: annual appreciation rate percentage>,
    "rental_yield": <float: expected rental yield percentage>,
    "risk_score": <int: risk score from 0-100, where 0 is lowest risk>,
    "recommendation": "<string: 'buy', 'hold', or 'avoid'>",
    "analysis": "<string: detailed 3-4 sentence investment analysis covering location factors, price trends, rental potential, and key considerations>"
}}

Consider factors like:
- Location desirability and infrastructure
- Historical price trends in the area
- Rental demand and yield potential
- Future development plans
- Price per square foot compared to market average

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
                
                self.logger.info(f"Investment analysis complete: {result.get('recommendation', 'N/A')}")
                self.log_execution(input_data, result)
                
                return result
            else:
                self.logger.warning("No valid response from Gemini")
                return self._get_default_analysis()
                
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {e}")
            return self._get_default_analysis()
        except Exception as e:
            self.logger.error(f"Investment analysis failed: {e}", exc_info=True)
            return self._get_default_analysis()
    
    def _get_default_analysis(self) -> Dict[str, Any]:
        """Return default analysis when AI fails."""
        return {
            'roi_5year': 0.0,
            'roi_10year': 0.0,
            'appreciation_rate': 0.0,
            'rental_yield': 0.0,
            'risk_score': 50,
            'recommendation': 'hold',
            'analysis': 'Unable to generate investment analysis. Please try again or consult with a real estate expert.'
        }
