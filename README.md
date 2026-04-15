# LangChain Milestones: From Foundations to Multi-Agent Route Optimization

This repository was created as part of the Infosys Virtual Internship 6.0 program.

This repository documents the progressive development of LangChain-based applications across four milestones, starting from basic concepts and building up to a sophisticated multi-agent route optimization system.

## Overview

The milestones demonstrate a learning journey through LangChain, LangGraph, and AI agent development:

1. **Milestone 1**: Core LangChain building blocks (LLMs, Prompts, Chains, Agents)
2. **Milestone 2**: Multi-agent system with tool integration
3. **Milestone 3**: Memory-enabled collaborative agents
4. **Milestone 4**: Production-ready route optimization backend with specialized agents

Each milestone builds upon the previous one, showcasing increasingly complex agent architectures and real-world applications.

---

## Milestone 1: Foundational LangChain Agent

**Location**: `Milestone_1/`

This milestone explores the core building blocks of the LangChain framework through a simple console interface.

### Key Components
- **LLM Integration**: Google Gemini 2.5-flash with deterministic responses
- **Prompt Templates**: Both string-based and chat-based prompt structures
- **Chains**: LCEL (LangChain Expression Language) for connecting components
- **Agents**: Zero-shot ReAct agent with basic tools (word count, text reversal)

### Features
- Simple Q&A Chain for factual responses
- Tutor Chain for educational explanations
- ReAct Chain demonstrating step-by-step reasoning
- Console-based interaction for testing each component

### Technologies
- LangChain, Google Generative AI, Python

---

## Milestone 2: LangChain Agent Console Environment

**Location**: `Milestone_2/`

A lightweight console-based multi-agent environment demonstrating dynamic tool calling.

### Key Components
- **Google Gemini Integration**: High-speed reasoning with gemini-2.5-flash
- **Calculator Tool**: Symbolic math solving using sympy
- **Weather Tool**: Real-time weather data via OpenWeather API
- **LangGraph React Agent**: Dynamic tool invocation and result combination

### Features
- Context-aware tool selection
- Mathematical expression solving
- Weather information retrieval
- Interactive console interface

### Technologies
- LangChain, LangGraph, Google Generative AI, SymPy, OpenWeather API

---

## Milestone 3: Multi-Agent System with Memory

**Location**: `Milestone_3/`

A console-based multi-agent collaboration system with both individual and shared memory.

### Architecture
```
User Input → Research Agent → Findings → Summarizer Agent → Executive Summary
                    ↑                        ↑
              Shared FAISS Vector Store Memory
```

### Key Components
- **Research Agent**: Gathers information on topics using Gemini LLM
- **Summarizer Agent**: Creates executive summaries from research findings
- **Memory Layers**:
  - Individual: ConversationBufferMemory (per-agent, short-term)
  - Shared: VectorStoreRetrieverMemory with FAISS (cross-agent, long-term)

### Features
- Collaborative agent workflow
- Persistent memory across sessions
- Knowledge accumulation and retrieval
- Topic-based research and summarization

### Technologies
- LangChain, LangGraph, Google Generative AI, FAISS

---

## Milestone 4: Smart Route Optimization Backend

**Location**: `Milestone_4/`

A production-ready FastAPI backend implementing a sophisticated multi-agent route optimization system.

### Architecture Overview

The system uses specialized agents working together through LangGraph workflows to optimize routes considering multiple risk factors.

### Agent Ecosystem

| Agent | Purpose | Key Technologies |
|-------|---------|------------------|
| **Route Generator** | Fetches alternative routes | OpenRouteService API |
| **Weather Agent** | Analyzes weather risks | OpenWeatherMap API |
| **News Agent** | Assesses geopolitical risks | Google Gemini LLM |
| **Traffic Agent** | Predicts congestion | Custom algorithms |
| **Risk Aggregator** | Combines risk scores | Weighted formula |
| **Decision Engine** | Selects optimal route | Risk-based logic |
| **Explanation Agent** | Generates human-readable explanations | Google Gemini LLM |
| **Monitor Agent** | Triggers rerouting when needed | Continuous monitoring |

### Key Features
- **Multi-Risk Analysis**: Weather, traffic, geopolitical news, and cost optimization
- **Real-time Data Integration**: Live weather and traffic data
- **AI-Powered Explanations**: Natural language route justifications
- **Modular Architecture**: Clean separation of agents, APIs, models, and UI
- **FastAPI Backend**: RESTful API with interactive map UI
- **LangGraph Orchestration**: Complex agent workflows and state management

### API Endpoints
- `GET /`: Interactive map interface
- `POST /optimize-route`: Route optimization with risk analysis
- `GET /status`: Health check

### Technologies
- FastAPI, LangGraph, Google Generative AI, OpenRouteService, OpenWeatherMap, Folium (maps)

---

## Technical Evolution

### From Milestone 1 to 4
- **Simple Chains** → **Complex Agent Workflows**
- **Single LLM Calls** → **Multi-Agent Collaboration**
- **Stateless Interactions** → **Memory-Persistent Systems**
- **Console Interfaces** → **Web APIs with UI**
- **Basic Tools** → **Specialized Domain Agents**
- **Educational Examples** → **Production Applications**

### Common Technologies Across Milestones
- **LangChain/LangGraph**: Core agent framework
- **Google Gemini**: Primary LLM for reasoning and generation
- **Python**: Implementation language
- **Virtual Environments**: Dependency management

### API Integrations
- **Google Gemini**: AI reasoning and text generation
- **OpenWeatherMap**: Weather data
- **OpenRouteService**: Routing and mapping
- **SymPy**: Mathematical computations

---

## Getting Started

Each milestone is self-contained with its own `requirements.txt` and setup instructions. Start with Milestone 1 for foundational concepts, then progress through each milestone.

### Prerequisites
- Python 3.9+
- API keys for Google Gemini, OpenWeatherMap, OpenRouteService
- Virtual environment setup

### Running Individual Milestones
Navigate to each milestone directory and follow the README instructions.

---

## Learning Outcomes

By the end of these milestones, you'll understand:
- LangChain's core abstractions (LLMs, Prompts, Chains, Agents)
- Multi-agent system design and orchestration
- Memory management in agent systems
- Real-world API integration
- Building production-ready AI applications
- Risk analysis and decision-making with AI
- FastAPI backend development
- Interactive UI development with mapping

This repository serves as both a learning resource and a foundation for building advanced AI agent systems.