# 🏠 AI-Powered Real Estate Agent

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-green.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

![1](https://github.com/user-attachments/assets/1afc3f87-57f7-4714-aff1-0b4cb83df776)

An intelligent real estate assistant that automates property discovery, analysis, and investment insights using AI.

## ✨ Features

- 🔍 **Smart Property Search** – Extracts real-time listings from 99acres, Housing.com, Square Yards
- 🤖 **AI-Powered Analysis** – Uses Gemini AI for property insights and recommendations
- 📊 **Investment Insights** – ROI projections, rental yields, and risk scoring
- 📈 **Market Trends** – Price trends, demand analysis, and growth predictions
- 🕒 **Search History** – Track and repeat past searches
- ⚡ **Redis Caching** – 70% API cost reduction with intelligent caching
- 🎯 **Interactive UI** – Clean Streamlit interface with 4 tabs

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **AI** | Google Gemini AI |
| **Web Scraping** | Firecrawl API |
| **Frontend** | Streamlit |
| **Database** | SQLite / PostgreSQL |
| **Caching** | Redis |
| **Validation** | Pydantic |
| **Testing** | Pytest |
| **CI/CD** | GitHub Actions |

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))
- Firecrawl API Key ([Get one here](https://firecrawl.dev))
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/HemantSudarshan/-AI-Powered-Real-Estate-Agent-Automating-Property-Search-Investment-Insights-.git
   cd -AI-Powered-Real-Estate-Agent-Automating-Property-Search-Investment-Insights-
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   copy .env.example .env
   # Edit .env with your API keys
   ```

5. **Run the application**:
   ```bash
   streamlit run src/ui/app.py
   ```

6. **Access the app** at `http://localhost:8501`

## 🐳 Docker Deployment

### Quick Start with Docker Compose
```bash
# Build and run with Redis
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

### Build Docker Image Only
```bash
docker build -t real-estate-agent .
docker run -p 8501:8501 --env-file .env real-estate-agent
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Run linting
ruff check src/ tests/
```

## 🗄️ Database Migrations

```bash
# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"

# Downgrade
alembic downgrade -1
```

## 📁 Project Structure

```
├── src/
│   ├── agents/          # AI agents (Search, Investment, Market Trend)
│   ├── services/        # External services (AI, Scraping, Cache)
│   ├── database/        # SQLAlchemy models and CRUD
│   ├── schemas/         # Pydantic validation schemas
│   ├── ui/              # Streamlit interface
│   ├── utils/           # Configuration and logging
│   └── health.py        # Health check endpoint
├── tests/               # Unit and integration tests
├── alembic/             # Database migrations
├── docs/                # Documentation
├── .github/workflows/   # CI/CD pipelines
├── Dockerfile           # Container configuration
├── docker-compose.yml   # Multi-container setup
└── pyproject.toml       # Project configuration
```

## 📖 Usage

1. Enter your API keys in the sidebar (or set via environment variables)
2. Navigate between tabs:
   - **Search** – Find properties by city, type, and price
   - **Investment** – Get ROI analysis for properties
   - **Market Trends** – View market predictions
   - **History** – Access past searches
3. Click "Start Search" to get AI-powered property recommendations

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Setting up development environment
- Code style and linting
- Running tests
- Submitting pull requests

## 📄 License

This project is licensed under the MIT License.

## 📧 Contact

**Hemant Sudarshan** - [GitHub](https://github.com/HemantSudarshan)

---

⭐ If you found this project helpful, please give it a star!
