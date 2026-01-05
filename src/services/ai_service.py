"""Google Gemini AI service."""
import asyncio
from typing import List, Dict
import google.generativeai as genai
from src.utils.logger import setup_logger


class AIService:
    """Service for AI-powered property analysis using Google Gemini."""
    
    def __init__(self, api_key: str):
        """
        Initialize AI service.
        
        Args:
            api_key: Google Gemini API key
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")
        self.logger = setup_logger("services.ai")
    
    async def analyze_properties(
        self,
        properties: List[Dict],
        max_price: float
    ) -> str:
        """
        Analyze property listings using Gemini AI.
        
        Args:
            properties: List of property dictionaries
            max_price: Maximum price budget in crores
        
        Returns:
            Formatted analysis text
        """
        if not properties:
            return "No properties found. Please try searching with different criteria."
        
        prompt = f"""As a real estate expert, analyze these properties and market trends:

Properties Found:
{properties}

**Instructions:**
- Identify the best properties close to {max_price} crores.
- Compare properties based on location, price per sq ft, and amenities.
- Provide investment insights and negotiation tips.

Format your response in a structured way."""
        
        try:
            self.logger.info("Sending request to Gemini AI for property analysis")
            
            response = await asyncio.to_thread(
                lambda: self.model.generate_content(prompt)
            )
            
            self.logger.info(f"Gemini AI Response received: {hasattr(response, 'text')}")
            
            if response and hasattr(response, 'text'):
                return response.text
            else:
                self.logger.warning("No valid text in Gemini response")
                return "Analysis could not be generated. Please try again."
                
        except Exception as e:
            self.logger.error(f"Error analyzing properties: {e}", exc_info=True)
            return "Error analyzing properties. Please check API configuration."
