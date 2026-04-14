# Milestone 1 — Foundational LangChain Agent

This milestone explores the core building blocks of the LangChain framework: **LLMs**, **Prompts**, **Chains**, and **Agents**. It provides a simple, educational console interface to interact with each component individually.

---

## Core Building Blocks

### 1. LLM (Language Model)
Connects to **Google Gemini** (`gemini-2.5-flash`) via the `langchain-google-genai` package. It is configured with `temperature=0` to ensure deterministic, factual responses.

### 2. Prompts
Demonstrates two types of templates:
- `PromptTemplate`: For standard string-based prompts with input variables.
- `ChatPromptTemplate`: For structured chat-based prompts with distinct `System` and `Human` roles.

### 3. Chains (LCEL)
Uses the **LangChain Expression Language (LCEL)** pipe operator (`|`) to connect prompts and LLMs:
- **Simple Q&A Chain**: Quick factual responses.
- **Tutor Chain**: Explains topics using analogies.
- **ReAct Chain**: Demonstrates step-by-step reasoning logic.

### 4. Agents
Implements a **Zero-shot ReAct** agent architecture. 
- If `langgraph` is installed, it uses a functional agent with tools (`word_count`, `reverse_text`).
- If not, it falls back to a simulated reasoning chain to illustrate the "ReAct" concept.

---

## Setup Instructions

### 1. Navigate to Milestone 1
```powershell
cd p:\Langchain_all_milestones\Milestone_1
```

### 2. Virtual Environment
The environment has already been initialized. To activate it:
```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Dependencies
Install the required packages:
```powershell
pip install -r requirements.txt
```

### 4. API Configuration
Ensure a `.env` file exists in this directory (or the parent directory) with your Gemini key:
```env
GOOGLE_API_KEY=your_key_here
```

---

## How to Test

Start the interactive console:
```powershell
python agent.py
```

### Modes to Explore:
1. **Simple Q&A**: Test basic prompt-to-LLM flow.
2. **Tutor/Explain**: See how `System` messages influence the AI's persona.
3. **ReAct Reasoning**: Observe how the agent breaks down complex thoughts.
4. **Agent Tools**: Use custom tools like counting words or reversing text strings.

Type `0` to exit the application.
