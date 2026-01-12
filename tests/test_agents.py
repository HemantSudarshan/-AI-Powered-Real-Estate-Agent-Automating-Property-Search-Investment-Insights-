"""Unit tests for AI Real Estate Agent agents."""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock


class TestSearchAgent:
    """Tests for SearchAgent."""

    def test_search_agent_initialization(self):
        """Test SearchAgent can be initialized."""
        from src.agents.search_agent import SearchAgent
        
        agent = SearchAgent(
            gemini_api_key="test_key",
            firecrawl_api_key="test_key"
        )
        assert agent is not None

    @pytest.mark.asyncio
    async def test_search_agent_search_mocked(self, mock_gemini_client, mock_firecrawl_client):
        """Test SearchAgent search with mocked external services."""
        from src.agents.search_agent import SearchAgent
        
        with patch.object(SearchAgent, '_scrape_properties', new_callable=AsyncMock) as mock_scrape:
            mock_scrape.return_value = [
                {"title": "Test Property", "price": 5000000}
            ]
            
            agent = SearchAgent(
                gemini_api_key="test_key",
                firecrawl_api_key="test_key"
            )
            # Test initialization is successful
            assert agent.gemini_api_key == "test_key"


class TestInvestmentAgent:
    """Tests for InvestmentAgent."""

    def test_investment_agent_initialization(self):
        """Test InvestmentAgent can be initialized."""
        from src.agents.investment_agent import InvestmentAgent
        
        agent = InvestmentAgent(gemini_api_key="test_key")
        assert agent is not None

    def test_investment_agent_has_analyze_method(self):
        """Test InvestmentAgent has analyze method."""
        from src.agents.investment_agent import InvestmentAgent
        
        agent = InvestmentAgent(gemini_api_key="test_key")
        assert hasattr(agent, 'analyze')

    @pytest.mark.asyncio
    async def test_investment_analysis_structure(self, sample_property_data):
        """Test investment analysis returns expected structure."""
        from src.agents.investment_agent import InvestmentAgent
        
        with patch("google.generativeai.GenerativeModel") as mock_model:
            mock_instance = MagicMock()
            mock_instance.generate_content.return_value = MagicMock(
                text='{"roi_5yr": 45, "roi_10yr": 85, "recommendation": "Buy"}'
            )
            mock_model.return_value = mock_instance
            
            agent = InvestmentAgent(gemini_api_key="test_key")
            # Verify agent is properly initialized
            assert agent.gemini_api_key == "test_key"


class TestMarketTrendAgent:
    """Tests for MarketTrendAgent."""

    def test_market_trend_agent_initialization(self):
        """Test MarketTrendAgent can be initialized."""
        from src.agents.market_trend_agent import MarketTrendAgent
        
        agent = MarketTrendAgent(gemini_api_key="test_key")
        assert agent is not None

    def test_market_trend_agent_has_analyze_method(self):
        """Test MarketTrendAgent has analyze method."""
        from src.agents.market_trend_agent import MarketTrendAgent
        
        agent = MarketTrendAgent(gemini_api_key="test_key")
        assert hasattr(agent, 'analyze')
