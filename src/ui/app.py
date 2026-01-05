"""Enhanced Streamlit UI for AI Real Estate Agent with multiple tabs."""
import asyncio
import streamlit as st
from datetime import datetime

from src.agents.search_agent import SearchAgent
from src.agents.investment_agent import InvestmentAgent
from src.agents.market_trend_agent import MarketTrendAgent
from src.database.session import init_db, get_db_context
from src.database.crud import PropertyCRUD, SearchHistoryCRUD, InvestmentAnalysisCRUD
from src.utils.config import get_settings


st.set_page_config(
    page_title="AI Real Estate Agent",
    page_icon="🏠",
    layout="wide"
)


def init_database():
    """Initialize database on first run."""
    if 'db_initialized' not in st.session_state:
        try:
            init_db()
            st.session_state.db_initialized = True
        except Exception as e:
            st.error(f"Database initialization failed: {e}")


def main():
    """Main Streamlit application."""
    init_database()
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
        
        st.divider()
        st.caption(f"📊 Database: {settings.database_url.split(':///')[-1]}")
        st.caption(f"💾 Cache: {'✅ Enabled' if settings.enable_cache else '❌ Disabled'}")
    
    # Main content with tabs
    st.title("🏠 AI Real Estate Agent")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Search Properties", "💰 Investment Analysis", "📈 Market Trends", "🕒 Search History"])
    
    # Tab 1: Property Search
    with tab1:
        st.info("Search for properties and get AI-powered recommendations.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            city = st.text_input(
                "City",
                placeholder="Enter city name (e.g., Bangalore, Mumbai)",
                key="search_city"
            )
            property_type = st.selectbox(
                "Property Type",
                ["Flat", "Individual House"],
                key="search_type"
            )
        
        with col2:
            max_price = st.number_input(
                "Max Price (in Crores)",
                min_value=0.1,
                max_value=100.0,
                value=5.0,
                step=0.1,
                key="search_price"
            )
        
        if st.button("🔍 Start Search", use_container_width=True, key="search_btn"):
            if not city:
                st.error("⚠️ Please enter a city name.")
            elif not gemini_key or not firecrawl_key:
                st.error("⚠️ Please enter your API keys in the sidebar.")
            else:
                agent = SearchAgent(gemini_key=gemini_key, firecrawl_key=firecrawl_key)
                
                with st.spinner("🔎 Searching properties..."):
                    try:
                        result = asyncio.run(agent.execute({
                            'city': city,
                            'max_price': max_price,
                            'property_type': property_type
                        }))
                        
                        properties = result.get('properties', [])
                        
                        # Save to database
                        if properties:
                            with get_db_context() as db:
                                for prop in properties:
                                    try:
                                        PropertyCRUD.create(db, prop)
                                    except Exception as e:
                                        st.warning(f"Failed to save property: {e}")
                                
                                # Save search history
                                SearchHistoryCRUD.create(
                                    db, city, property_type, max_price, len(properties)
                                )
                        
                        st.subheader("🏘️ Property Recommendations")
                        
                        if properties:
                            st.success(f"✅ Found {len(properties)} properties!")
                        else:
                            st.warning("⚠️ No properties found. Try adjusting your criteria.")
                        
                        st.markdown(result.get('analysis', 'No analysis available.'))
                        
                    except Exception as e:
                        st.error(f"❌ An error occurred: {str(e)}")
    
    # Tab 2: Investment Analysis
    with tab2:
        st.info("Get detailed investment analysis for properties.")
        
        with get_db_context() as db:
            properties = PropertyCRUD.search(db, limit=50)
        
        if properties:
            property_options = {
                f"{p.building_name} - {p.city} (₹{p.price:,.0f})": p 
                for p in properties
            }
            
            selected_prop_name = st.selectbox(
                "Select Property",
                options=list(property_options.keys()),
                key="invest_select"
            )
            
            if st.button("💰 Analyze Investment", use_container_width=True, key="invest_btn"):
                if not gemini_key:
                    st.error("⚠️ Please enter your Gemini API key in the sidebar.")
                else:
                    selected_prop = property_options[selected_prop_name]
                    
                    agent = InvestmentAgent(gemini_key=gemini_key)
                    
                    with st.spinner("📊 Analyzing investment potential..."):
                        try:
                            property_dict = {
                                'building_name': selected_prop.building_name,
                                'property_type': selected_prop.property_type,
                                'location_address': selected_prop.location_address,
                                'city': selected_prop.city,
                                'price': selected_prop.price,
                                'description': selected_prop.description
                            }
                            
                            result = asyncio.run(agent.execute({'property': property_dict}))
                            
                            # Save analysis
                            with get_db_context() as db:
                                analysis_data = {
                                    'property_id': selected_prop.id,
                                    **{k: v for k, v in result.items() if k != 'analysis'}
                                }
                                analysis_data['analysis_text'] = result.get('analysis', '')
                                InvestmentAnalysisCRUD.create(db, analysis_data)
                            
                            # Display results
                            st.subheader("📊 Investment Analysis Results")
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("5-Year ROI", f"{result.get('roi_5year', 0):.1f}%")
                                st.metric("Annual Appreciation", f"{result.get('appreciation_rate', 0):.1f}%")
                            with col2:
                                st.metric("10-Year ROI", f"{result.get('roi_10year', 0):.1f}%")
                                st.metric("Rental Yield", f"{result.get('rental_yield', 0):.1f}%")
                            with col3:
                                st.metric("Risk Score", f"{result.get('risk_score', 50)}/100")
                                recommendation = result.get('recommendation', 'hold').upper()
                                emoji = "🟢" if recommendation == "BUY" else "🔴" if recommendation == "AVOID" else "🟡"
                                st.metric("Recommendation", f"{emoji} {recommendation}")
                            
                            st.markdown("### 📝 Analysis")
                            st.markdown(result.get('analysis', 'No detailed analysis available.'))
                            
                        except Exception as e:
                            st.error(f"❌ Analysis failed: {str(e)}")
        else:
            st.warning("No properties in database. Search for properties first in the Search tab.")
    
    # Tab 3: Market Trends
    with tab3:
        st.info("Analyze market trends for different cities.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            trend_city = st.text_input(
                "City",
                placeholder="Enter city name",
                key="trend_city"
            )
            trend_type = st.selectbox(
                "Property Type",
                ["All", "Flat", "Individual House"],
                key="trend_type"
            )
        
        with col2:
            timeframe = st.selectbox(
                "Analysis Timeframe",
                ["6months", "1year", "3years"],
                index=1,
                key="trend_timeframe"
            )
        
        if st.button("📈 Analyze Market Trends", use_container_width=True, key="trend_btn"):
            if not trend_city:
                st.error("⚠️ Please enter a city name.")
            elif not gemini_key:
                st.error("⚠️ Please enter your Gemini API key in the sidebar.")
            else:
                agent = MarketTrendAgent(gemini_key=gemini_key)
                
                with st.spinner("📊 Analyzing market trends..."):
                    try:
                        result = asyncio.run(agent.execute({
                            'city': trend_city,
                            'property_type': trend_type,
                            'timeframe': timeframe
                        }))
                        
                        st.subheader(f"📈 Market Trends for {trend_city}")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            trend = result.get('price_trend', 'stable').upper()
                            emoji = "📈" if trend == "RISING" else "📉" if trend == "DECLINING" else "➡️"
                            st.metric("Price Trend", f"{emoji} {trend}")
                        with col2:
                            demand = result.get('demand_level', 'medium').upper ()
                            emoji = "🔥" if demand == "HIGH" else "❄️" if demand == "LOW" else "🌤️"
                            st.metric("Demand Level", f"{emoji} {demand}")
                        with col3:
                            growth = result.get('growth_prediction', 0)
                            st.metric("Growth Prediction", f"{growth:.1f}%")
                        
                        hot_areas = result.get('hot_areas', [])
                        if hot_areas:
                            st.markdown("### 🔥 Hot Areas")
                            st.write(", ".join(hot_areas))
                        
                        st.markdown("### 📝 Market Insights")
                        st.markdown(result.get('insights', 'No detailed insights available.'))
                        
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")
    
    # Tab 4: Search History
    with tab4:
        st.info("View your recent property searches.")
        
        with get_db_context() as db:
            history = SearchHistoryCRUD.get_recent(db, limit=20)
        
        if history:
            st.subheader(f"📜 Recent Searches ({len(history)})")
            
            for i, search in enumerate(history):
                with st.expander(
                    f"🔍 {search.city} - {search.property_type} (₹{search.max_price} Cr) - "
                    f"{search.timestamp.strftime('%Y-%m-%d %H:%M')} - {search.results_count} results"
                ):
                    col1, col2, col3, col4 = st.columns(4)
                    col1.write(f"**City:** {search.city}")
                    col2.write(f"**Type:** {search.property_type}")
                    col3.write(f"**Max Price:** ₹{search.max_price} Cr")
                    col4.write(f"**Results:** {search.results_count}")
                    
                    if st.button("🔄 Repeat Search", key=f"repeat_{search.id}"):
                        st.session_state.search_city = search.city
                        st.session_state.search_type = search.property_type
                        st.session_state.search_price = search.max_price
                        st.switch_page("pages/0_🔍_Search_Properties")
                        st.rerun()
        else:
            st.warning("No search history yet. Start searching for properties!")


if __name__ == "__main__":
    main()
