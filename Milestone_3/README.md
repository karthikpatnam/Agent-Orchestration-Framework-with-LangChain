# Milestone 3 — Multi-Agent System with Memory

A console-based multi-agent collaboration system built with **Python**, **LangChain**, **LangGraph**, and **Google Gemini**.  
This milestone demonstrates two specialized agents — a **Research Agent** and a **Summarizer Agent** — working together through both individual short-term memory and a shared long-term vector memory (FAISS).

---

## Architecture Overview

```
User Input (topic)
       │
       ▼
┌─────────────────────────────────────┐
│         Research Agent              │
│  • Reads own ConversationBuffer     │
│  • Reads shared VectorStore (FAISS) │
│  • Calls Gemini LLM                 │
│  • Saves findings → shared memory   │
└────────────────┬────────────────────┘
                 │ findings
                 ▼
┌─────────────────────────────────────┐
│         Summarizer Agent            │
│  • Reads own ConversationBuffer     │
│  • Reads shared VectorStore (FAISS) │
│  • Calls Gemini LLM                 │
│  • Produces executive summary       │
│  • Saves summary → shared memory    │
└─────────────────────────────────────┘
```

### Memory Layers

| Layer | Class | Scope |
|---|---|---|
| Individual (short-term) | `ConversationBufferMemory` | Per-agent, current session |
| Shared (long-term) | `VectorStoreRetrieverMemory` + FAISS | Cross-agent, persists across topics |

On every subsequent query the shared FAISS index automatically surfaces relevant prior research, so agents build on each other's past work.

---

## Prerequisites

- **Python 3.9 or higher**
- A **Google Gemini API key** — get one free at [Google AI Studio](https://aistudio.google.com/)
- Internet access (for Gemini LLM calls)

---

## Setup Instructions

### 1. Clone / navigate to the project folder

```powershell
cd p:\Langchain_all_milestones\Milestone_3
```

### 2. Create and activate a virtual environment

```powershell
# Create
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Windows CMD)
.\venv\Scripts\activate.bat
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file inside the `Milestone_3` folder with the following content:

```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

> **Note:** A `WEATHER_API_KEY` is not required for this milestone.

---

## Running the System

With the virtual environment active, start the orchestrator:

```powershell
python orchestrator.py
```

You will see the startup banner and a prompt:

```
=================================================================
  Multi-Agent Collaboration System  —  Milestone 3
  Agents : Research Agent | Summarizer Agent
  Memory : ConversationBufferMemory + VectorStoreRetrieverMemory
=================================================================

Initialising shared vector memory (FAISS + Gemini embeddings)...
Shared memory ready.

All agents online. Type 'exit' to quit.

Enter a topic to research (or 'exit'):
```

### Example session

```
Enter a topic to research (or 'exit'): Large Language Models

[Research Agent] Investigating topic: Large Language Models
[Research Agent] Findings saved to shared memory.

--- RESEARCH AGENT OUTPUT ---
• Definition and Core Concept: ...
• Transformer Architecture: ...
...

[Summarizer Agent] Summarizing findings for topic: Large Language Models
[Summarizer Agent] Retrieved shared knowledge — enriching summary.
[Summarizer Agent] Summary saved to shared memory.

--- SUMMARIZER AGENT OUTPUT ---
TL;DR: ...
Key Takeaways: ...
Conclusion: ...

Enter a topic to research (or 'exit'): AI Ethics and Bias

[Research Agent] Investigating topic: AI Ethics and Bias
[Research Agent] Found relevant shared context — incorporating it.   ← memory at work
...
```

Type `exit` or `quit` at any prompt to cleanly terminate.

---

## Project Structure

```
Milestone_3/
├── venv/                 # Virtual environment (not committed to git)
├── .env                  # API keys (not committed to git)
├── requirements.txt      # Python dependencies
├── memory_setup.py       # Individual + shared memory factories
├── agents.py             # ResearchAgent and SummarizerAgent classes
├── orchestrator.py       # Main entry point — chains agents together
└── README.md             # This file
```

---

## Embedding Strategy

The shared FAISS vector store tries embedding providers in this order:

1. **Gemini `gemini-embedding-exp-03-07`** *(preferred)*
2. **Gemini `text-embedding-004`**
3. **Gemini `embedding-001`**
4. **HuggingFace `all-MiniLM-L6-v2`** *(local, no additional API key needed)*
5. **FakeEmbeddings** *(fallback — architecture still runs, similarity is random)*

If Gemini embedding endpoints are unavailable due to API version restrictions, the system automatically falls back without crashing.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `GOOGLE_API_KEY is not set` | Create/check your `.env` file in `Milestone_3/` |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` inside the activated venv |
| `LangChainDeprecationWarning` | Informational only — does not affect functionality |
| Gemini embedding `404 NOT_FOUND` | Expected — system auto-falls back to FakeEmbeddings |
