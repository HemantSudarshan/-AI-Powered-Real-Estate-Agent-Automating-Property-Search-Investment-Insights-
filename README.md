# 🏠 AI-Powered Real Estate Agent

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

![1](https://github.com/user-attachments/assets/1afc3f87-57f7-4714-aff1-0b4cb83df776)

An intelligent real estate assistant that automates property discovery, analysis, and investment insights using AI.

## ✨ Features

- 🔍 **Smart Property Search** – Extracts real-time listings from 99acres, Housing.com, Square Yards
- 🤖 **AI-Powered Analysis** – Uses Gemini AI for property insights and recommendations
- 📊 **Investment Insights** – Analyzes properties based on location, price, and amenities
- 🎯 **Interactive UI** – Clean Streamlit interface for easy property searching

## 🛠️ Tech Stack

- **AI**: Google Gemini AI
- **Web Scraping**: Firecrawl API
- **Frontend**: Streamlit
- **Data Validation**: Pydantic

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))
- Firecrawl API Key ([Get one here](https://firecrawl.dev))

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

4. **Set up environment variables** (optional):
   ```bash
   copy .env.example .env
   # Edit .env with your API keys
   ```

5. **Run the application**:
   
   **Option 1: New Modular Version (Recommended)**
   ```bash
   streamlit run src/ui/app.py
   ```
   
   **Option 2: Legacy Version (Backward Compatible)**
   ```bash
   streamlit run Ai_RealAgent.py
   ```

6. **Access the app** at `http://localhost:8501`

## 📖 Usage

1. Enter your API keys in the sidebar (or set via environment variables)
2. Enter your search criteria:
   - City name
   - Property type (Flat/Individual House)
   - Maximum price (in Crores)
3. Click "Start Search" to get AI-powered property recommendations

## 📁 Project Structure

```
├── Ai_RealAgent.py     # Main application file
├── Directions.md       # Development roadmap & architecture guide
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore patterns
└── README.md           # This file
```

## 🔮 Future Roadmap

See [Directions.md](Directions.md) for a comprehensive guide on transforming this into a production-ready application with:
- Modular architecture with FastAPI backend
- Vector database for semantic search
- Investment analysis agents
- Docker deployment & CI/CD

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 📧 Contact

**Hemant Sudarshan** - [GitHub](https://github.com/HemantSudarshan)

---

⭐ If you found this project helpful, please give it a star!
