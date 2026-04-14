# Project Structure - Reorganized

## Overview
The ReRoute 2 project has been reorganized into a clean, modular structure with separate folders for agents, core logic, APIs, and models.

## Directory Structure

```
ReRoute_2/
├── agents/                    # Individual AI agents
│   ├── __init__.py
│   ├── route_generator.py    # Fetches candidate routes
│   ├── weather_agent.py      # Analyzes weather risks
│   ├── news_agent.py         # Analyzes geopolitical risks (Google Gemini)
│   ├── traffic_agent.py      # Analyzes traffic conditions
│   ├── risk_aggregator.py    # Combines all risk scores
│   ├── decision_engine.py    # Selects optimal route
│   ├── explanation_agent.py  # Generates explanations (Google Gemini)
│   └── monitor_agent.py      # Monitors route viability
│
├── core/                      # Workflow orchestration
│   ├── __init__.py
│   └── workflow.py           # LangGraph workflow definition
│
├── api/                       # External API clients
│   ├── __init__.py
│   └── clients.py            # OpenRouteService, OpenWeather, etc.
│
├── models_pkg/               # Data models
│   ├── __init__.py
│   └── schemas.py            # Pydantic models
│
├── ui_pkg/                   # User interface
│   ├── __init__.py
│   └── map_ui.py             # Interactive map UI
│
├── main.py                   # FastAPI application entry point
├── config.py                 # Configuration & environment variables
├── requirements.txt          # Python dependencies
└── .env                      # Environment variables (API keys)
```

## Key Changes

### 1. Code Organization
- **Before**: All files mixed at root level
- **After**: Organized into logical packages (agents, core, api, models, ui)

### 2. AI Model Replacement: OpenAI → Google Gemini
- **Removed**: `langchain-openai` (OpenAI API with quota limits)
- **Added**: `google-generativeai` (Google's Gemini API)
- **Agents using Google Gemini**:
  - `news_agent.py` - Analyzes news for geopolitical risks
  - `explanation_agent.py` - Generates human-readable explanations

### 3. Dependencies Updated
```
- Removed: langchain-openai
- Added: google-generativeai>=0.3.0
- Updated config.py to use GOOGLE_API_KEY instead of OPENAI_API_KEY
```

### 4. Import Path Changes
```python
# Old
from models import OptimizationRequest
from workflow import app_workflow
from ui import get_map_ui
from clients import fetch_routes

# New
from models_pkg.schemas import OptimizationRequest
from core.workflow import app_workflow
from ui_pkg.map_ui import get_map_ui
from api.clients import fetch_routes
```

## Agent Functions

### Route Generator
- **File**: `agents/route_generator.py`
- **Purpose**: Fetches 3 alternative routes using OpenRouteService API
- **Output**: List of RouteInfo objects with geometry, distance, duration

### Weather Agent
- **File**: `agents/weather_agent.py`
- **Purpose**: Analyzes weather conditions and risks
- **API**: OpenWeatherMap
- **Output**: Weather risk score (0-100) and report

### News Intelligence Agent
- **File**: `agents/news_agent.py`
- **Purpose**: Analyzes geopolitical news and disruptions
- **LLM**: Google Gemini Pro
- **Output**: News risk score (0-100) and analysis

### Traffic Agent
- **File**: `agents/traffic_agent.py`
- **Purpose**: Predicts traffic congestion
- **Output**: Traffic risk score and report

### Risk Aggregator
- **File**: `agents/risk_aggregator.py`
- **Purpose**: Combines all risk scores into total score
- **Formula**: Cost + (Weather × 0.5) + (News × 3.0) + (Traffic × 0.5)

### Decision Engine
- **File**: `agents/decision_engine.py`
- **Purpose**: Selects the best route with lowest risk
- **Logic**: Penalizes dangerous routes heavily

### Explanation Agent
- **File**: `agents/explanation_agent.py`
- **Purpose**: Generates AI explanation for route selection
- **LLM**: Google Gemini Pro
- **Output**: Human-readable explanation

### Monitor Agent
- **File**: `agents/monitor_agent.py`
- **Purpose**: Determines if rerouting is needed
- **Logic**: Triggers reroute if best route is too dangerous

## API Endpoints

### GET /
- Returns interactive map UI

### GET /ui
- Alternate UI endpoint

### POST /optimize-route
- Request body:
  ```json
  {
    "source_coords": [longitude, latitude],
    "dest_coords": [longitude, latitude]
  }
  ```
- Response: Optimized routes with risk analysis

### GET /status
- Health check endpoint

## Environment Variables

```env
ORS_API_KEY=<OpenRouteService API key>
OPENWEATHER_API_KEY=<OpenWeather API key>
GOOGLE_API_KEY=<Google API key for Gemini>
```

## Running the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python -m uvicorn main:app --reload

# Access the UI
http://127.0.0.1:8000/
```

## Benefits of Reorganization

✅ **Modular Structure** - Each agent is independent and maintainable
✅ **Scalability** - Easy to add new agents or modify existing ones
✅ **Separation of Concerns** - UI, API, models, and business logic are separated
✅ **Google Gemini** - Replaced OpenAI with Google's free/cheaper tier API
✅ **Type Safety** - Clear import paths and dependencies
✅ **Documentation** - Self-documenting code with docstrings

