# Contributing to AI Real Estate Agent

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Git
- Redis (optional, for caching)

### Setup Development Environment

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/-AI-Powered-Real-Estate-Agent-Automating-Property-Search-Investment-Insights-.git
   cd -AI-Powered-Real-Estate-Agent-Automating-Property-Search-Investment-Insights-
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov pytest-asyncio ruff  # Dev dependencies
   ```

4. **Set up environment variables**
   ```bash
   copy .env.example .env
   # Edit .env with your API keys
   ```

## 📝 Code Style

We use **Ruff** for linting and code style enforcement.

### Running Linting
```bash
ruff check src/ tests/
ruff check src/ tests/ --fix  # Auto-fix issues
```

### Code Standards
- Follow PEP 8 guidelines
- Use type hints for function signatures
- Write docstrings for all public functions and classes
- Maximum line length: 100 characters

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/test_agents.py -v

# Run tests matching a pattern
pytest -k "test_search" -v
```

### Writing Tests
- Place tests in the `tests/` directory
- Use descriptive test names: `test_<function>_<scenario>_<expected_result>`
- Use fixtures from `conftest.py` for common setup
- Mock external APIs (Gemini, Firecrawl) in tests

## 🔀 Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation if needed

3. **Run checks before committing**
   ```bash
   ruff check src/ tests/
   pytest tests/ -v
   ```

4. **Commit with clear messages**
   ```bash
   git commit -m "feat: add new investment metric calculation"
   ```
   
   Commit message prefixes:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `test:` Test changes
   - `refactor:` Code refactoring
   - `chore:` Maintenance tasks

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub.

## 📁 Project Structure

```
├── src/
│   ├── agents/          # AI agents (Search, Investment, Market Trend)
│   ├── services/        # External services (AI, Scraping, Cache)
│   ├── database/        # SQLAlchemy models and CRUD
│   ├── schemas/         # Pydantic validation schemas
│   ├── ui/              # Streamlit interface
│   └── utils/           # Configuration and logging
├── tests/               # Unit and integration tests
├── alembic/             # Database migrations
├── docs/                # Documentation
└── .github/workflows/   # CI/CD pipelines
```

## 🐛 Reporting Issues

When reporting issues, please include:
- Python version
- OS and version
- Steps to reproduce
- Expected vs actual behavior
- Error messages/stack traces

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
