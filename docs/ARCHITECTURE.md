# Architecture Documentation

## Overview
AI-Powered Real Estate Agent with modular, production-ready architecture.

## System Design

### Architecture Diagram
```
┌─────────────────────────────────────────┐
│        Streamlit UI (src/ui/app.py)     │
└──────────────┬──────────────────────────┘
               │
        ┌──────▼──────┐
        │ SearchAgent │
        │ (Orchestrator)│
        └──────┬──────┘
               │
       ┌───────┴────────┐
       │                │
┌──────▼──────┐  ┌─────▼─────┐
│  Scraping   │  │    AI     │
│  Service    │  │  Service  │
│ (Firecrawl) │  │ (Gemini)  │
└─────────────┘  └───────────┘
```

### Components

#### 1. **Agents Layer** (`src/agents/`)
- `base_agent.py` - Abstract base class for all agents
- `search_agent.py` - Orchestrates property search and analysis

#### 2. **Services Layer** (`src/services/`)
- `scraping_service.py` - Firecrawl integration for property data
- `ai_service.py` - Gemini AI for property analysis

#### 3. **Schemas** (`src/schemas/`)
- `property.py` - Pydantic models for data validation

#### 4. **Utilities** (`src/utils/`)
- `config.py` - Configuration management with Pydantic Settings
- `logger.py` - Structured logging

#### 5. **UI** (`src/ui/`)
- `app.py` - Streamlit web interface

## Design Patterns

### Separation of Concerns
Each layer has a specific responsibility:
- **Agents**: Orchestration and business logic
- **Services**: External API integrations
- **Schemas**: Data validation
- **Utils**: Cross-cutting concerns

### Dependency Injection
Services are injected into agents, making the code testable and maintainable.

### Configuration Management
All configuration through environment variables using Pydantic Settings.

## Running the Application

### New Modular Version
```bash
streamlit run src/ui/app.py
```

### Legacy Version (Backward Compatible)
```bash
streamlit run Ai_RealAgent.py
```

## Future Enhancements
- FastAPI REST endpoints
- Vector database for semantic search
- PostgreSQL for persistence
- Docker deployment
- CI/CD pipeline

See `Directions.md` for complete roadmap.
