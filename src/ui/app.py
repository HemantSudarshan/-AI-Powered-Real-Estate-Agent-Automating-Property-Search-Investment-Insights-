"""Streamlit UI for AI Real Estate Agent."""
import asyncio
import streamlit as st
from src.agents.search_agent import SearchAgent
from src.utils.config import get_settings


st.set_page_config(
    page_title="AI Real Estate Agent",
    page_icon="🏠",
    layout="wide"
)


def main():
    """Main Streamlit application."""
    settings = get_settings()
    
    # Sidebar for API configuration
    with st.sidebar:
        st.title("🔑 API Configuration")
        st.info("Enter your API keys or set them in `.env` file")
        
        gemini_key = st.text_input(
            "Gemini API Key",
            value=settings.gemini_api_key,
            type="password",
            help="Get your key from https://makersuite.google.com/app/apikey"
        )
        
        firecrawl_key = st.text_input(
            "Firecrawl API Key",
            value=settings.firecrawl_api_key,
            type="password",
            help="Get your key from https://firecrawl.dev"
        )
    
    # Main content
    st.title("🏠 AI Real Estate Agent")
    st.info(
        "Welcome to the AI-Powered Real Estate Agent! "
        "Enter your search criteria below to get property recommendations and insights."
    )
    
    # Search form
    col1, col2 = st.columns(2)
    
    with col1:
        city = st.text_input(
            "City",
            placeholder="Enter city name (e.g., Bangalore, Mumbai)"
        )
        property_type = st.selectbox(
            "Property Type",
            ["Flat", "Individual House"],
            help="Select the type of property you're looking for"
        )
    
    with col2:
        max_price = st.number_input(
            "Max Price (in Crores)",
            min_value=0.1,
            max_value=100.0,
            value=5.0,
            step=0.1,
            help="Maximum budget in Indian Crores (1 Crore = 10 Million)"
        )
    
    # Search button
    if st.button("🔍 Start Search", use_container_width=True):
        if not city:
            st.error("⚠️ Please enter a city name.")
            return
        
        if not gemini_key:
            st.error("⚠️ Please enter your Gemini API key in the sidebar.")
            return
        
        if not firecrawl_key:
            st.error("⚠️ Please enter your Firecrawl API key in the sidebar.")
            return
        
        # Initialize agent with API keys
        agent = SearchAgent(gemini_key=gemini_key, firecrawl_key=firecrawl_key)
        
        # Execute search
        with st.spinner("🔎 Fetching properties..."):
            try:
                result = asyncio.run(agent.execute({
                    'city': city,
                    'max_price': max_price,
                    'property_type': property_type
                }))
                
                # Display results
                st.subheader("🏘️ Property Recommendations")
                
                if result['properties']:
                    st.success(f"✅ Found {len(result['properties'])} properties!")
                else:
                    st.warning("⚠️ No properties found. Try adjusting your search criteria.")
                
                # Display AI analysis
                st.markdown(result['analysis'])
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.error("Please check your API keys and internet connection.")


if __name__ == "__main__":
    main()
