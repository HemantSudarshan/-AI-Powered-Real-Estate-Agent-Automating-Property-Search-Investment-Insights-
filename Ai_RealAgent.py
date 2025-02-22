import asyncio
import logging
import os
from typing import Dict, List
from pydantic import BaseModel, Field
import google.generativeai as genai
from firecrawl import FirecrawlApp
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Secure API key handling
def get_api_key() -> str:
    key = os.getenv("GEMINI_API_KEY") or st.session_state.get("gemini_api_key")
    if not key:
        logging.error("Gemini API Key is missing!")
    return key

def get_firecrawl_key() -> str:
    key = os.getenv("FIRECRAWL_API_KEY") or st.session_state.get("firecrawl_api_key")
    if not key:
        logging.error("Firecrawl API Key is missing!")
    return key

class PropertyData(BaseModel):
    """Schema for property data extraction"""
    building_name: str = Field(description="Name of the building/property")
    property_type: str = Field(description="Type of property (commercial, residential, etc)")
    location_address: str = Field(description="Complete address of the property")
    price: str = Field(description="Price of the property")
    description: str = Field(description="Detailed description of the property")

class PropertiesResponse(BaseModel):
    """Schema for multiple properties response"""
    properties: List[PropertyData]

class PropertyFindingAgent:
    """Agent responsible for property recommendations"""
    
    def __init__(self, gemini_api_key: str, firecrawl_api_key: str):
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel("gemini-pro")
        self.firecrawl = FirecrawlApp(api_key=firecrawl_api_key)
    
    async def fetch_properties(self, city: str, max_price: float, property_type: str) -> List[Dict]:
        """Fetch property listings from Firecrawl"""
        urls = [
            f"https://www.squareyards.com/sale/property-for-sale-in-{city.lower()}/*",
            f"https://www.99acres.com/property-in-{city.lower()}-ffid/*",
            f"https://housing.com/in/buy/{city.lower()}/{city.lower()}"
        ]
        try:
            logging.info(f"Fetching properties for {city}...")
            response = await asyncio.to_thread(
                self.firecrawl.extract,
                urls,
                params={
                    'prompt': f"Extract up to 10 {property_type} properties under {max_price} crores in {city}.",
                    'schema': PropertiesResponse.model_json_schema()
                }
            )
            logging.info(f"Raw Firecrawl Response: {response}")
            if response.get('success'):
                return response['data'].get('properties', [])
        except Exception as e:
            logging.error(f"Error fetching properties: {e}")
        return []
    
    async def analyze_properties(self, properties: List[Dict], max_price: float) -> str:
        """Analyze property listings asynchronously using Gemini AI"""
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
            logging.info("Sending request to Gemini AI...")
            response = await asyncio.to_thread(lambda: self.model.generate_content(prompt))
            logging.info(f"Gemini AI Response: {response}")
            return response.text if response and hasattr(response, 'text') else "Analysis could not be generated. Please try again."
        except Exception as e:
            logging.error(f"Error analyzing properties: {e}")
            return "Error analyzing properties. Please check API configuration."

# Streamlit UI
st.set_page_config(page_title="AI Real Estate Agent", page_icon="🏠", layout="wide")

def main():
    with st.sidebar:
        st.title("🔑 API Configuration")
        st.session_state['gemini_api_key'] = st.text_input("Gemini API Key", type="password")
        st.session_state['firecrawl_api_key'] = st.text_input("Firecrawl API Key", type="password")
    
    st.title("🏠 AI Real Estate Agent")
    st.info("""Welcome to the AI Based Real Estate Agent!
    Enter your search criteria below to get property recommendations and insights.""")
    
    col1, col2 = st.columns(2)
    with col1:
        city = st.text_input("City", placeholder="Enter city name")
        property_type = st.selectbox("Property Type", ["Flat", "Individual House"])
    
    with col2:
        max_price = st.number_input("Max Price (in Crores)", min_value=0.1, max_value=100.0, value=5.0, step=0.1)
    
    if st.button("🔍 Start Search", use_container_width=True):
        if not city:
            st.error("Please enter a city.")
            return
        
        agent = PropertyFindingAgent(
            gemini_api_key=get_api_key(),
            firecrawl_api_key=get_firecrawl_key()
        )
        
        with st.spinner("Fetching properties..."):
            properties = asyncio.run(agent.fetch_properties(city, max_price, property_type))
        
        with st.spinner("Analyzing properties..."):
            analysis = asyncio.run(agent.analyze_properties(properties, max_price))
        
        st.subheader("🏘️ Property Recommendations")
        st.markdown(analysis)

if __name__ == "__main__":
    main()
