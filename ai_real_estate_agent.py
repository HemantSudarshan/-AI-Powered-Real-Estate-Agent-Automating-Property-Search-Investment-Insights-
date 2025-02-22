import asyncio
import logging
import os
from typing import Dict, List
from pydantic import BaseModel, Field
import google.generativeai as genai
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Secure API key handling
def get_api_key() -> str:
    return os.getenv("GEMINI_API_KEY") or st.session_state.get("gemini_api_key")

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
    
    def __init__(self, gemini_api_key: str):
        genai.configure(api_key=gemini_api_key)
    
    async def fetch_properties(self, city: str, max_price: float, property_type: str) -> List[Dict]:
        """Simulating property search - Replace with actual API calls"""
        logging.info(f"Fetching properties for {city}, max price: {max_price} crores, type: {property_type}")
        properties = [
            {"building_name": "Skyline Heights", "property_type": property_type, "location_address": f"{city} Central", "price": "4.5 Crores", "description": "Luxury apartment with city view."},
            {"building_name": "Green Residency", "property_type": property_type, "location_address": f"{city} West", "price": "3.8 Crores", "description": "Spacious 3BHK with amenities."}
        ]
        logging.info(f"Fetched properties: {properties}")
        return properties
    
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
            response = await asyncio.to_thread(lambda: genai.generate_text(prompt=prompt))
            return response.result if response and hasattr(response, 'result') else "Analysis could not be generated. Please try again."
        except Exception as e:
            logging.error(f"Error analyzing properties: {e}")
            return "Error analyzing properties. Please check API configuration."

# Streamlit UI
st.set_page_config(page_title="AI Real Estate Agent", page_icon="🏠", layout="wide")

def main():
    with st.sidebar:
        st.title("🔑 API Configuration")
        st.session_state['gemini_api_key'] = st.text_input("Gemini API Key", type="password")
    
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
        
        agent = PropertyFindingAgent(gemini_api_key=get_api_key())
        
        with st.spinner("Fetching properties..."):
            properties = asyncio.run(agent.fetch_properties(city, max_price, property_type))
        
        with st.spinner("Analyzing properties..."):
            analysis = asyncio.run(agent.analyze_properties(properties, max_price))
        
        st.subheader("🏘️ Property Recommendations")
        st.markdown(analysis)

if __name__ == "__main__":
    main()
