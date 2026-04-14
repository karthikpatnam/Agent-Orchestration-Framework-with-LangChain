"""
agent.py — Milestone 1: Foundational LangChain Agent
======================================================
Demonstrates LangChain's four core building blocks:

  1. LLM          — Connect to Google Gemini via ChatGoogleGenerativeAI
  2. Prompts      — PromptTemplate and ChatPromptTemplate
  3. Chains       — LCEL pipe operator (prompt | llm | parser)
  4. Agents       — Zero-shot ReAct agent with a built-in tool

Run:
    python agent.py
"""

import os
import sys
from dotenv import load_dotenv

# ── Load .env (checks this directory first, then parent) ────────────────────
_here = os.path.dirname(os.path.abspath(__file__))
for _cand in [os.path.join(_here, ".env"), os.path.join(_here, "..", ".env")]:
    if os.path.exists(_cand):
        load_dotenv(_cand)
        break

# ── LangChain imports ────────────────────────────────────────────────────────
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

DIVIDER = "=" * 60


# ════════════════════════════════════════════════════════════════
# BLOCK 1 — LLM
# ════════════════════════════════════════════════════════════════
def get_llm() -> ChatGoogleGenerativeAI:
    """
    Building Block #1: LLM
    Connects to Google Gemini using langchain-google-genai.
    temperature=0  → deterministic, factual answers.
    """
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
    )


# ════════════════════════════════════════════════════════════════
# BLOCK 2 — Prompt Templates
# ════════════════════════════════════════════════════════════════
# 2a. Simple PromptTemplate (single input variable)
SIMPLE_PROMPT = PromptTemplate(
    input_variables=["question"],
    template=(
        "You are a concise and knowledgeable assistant.\n"
        "Answer the following question in 2–3 sentences:\n\n"
        "Question: {question}\n\n"
        "Answer:"
    ),
)

# 2b. ChatPromptTemplate with system + user roles
CHAT_PROMPT = ChatPromptTemplate.from_messages([
    SystemMessage(content=(
        "You are an expert tutor explaining concepts to a curious student. "
        "Keep explanations clear and use a real-world analogy where possible."
    )),
    ("human", "Explain: {topic}"),
])

# 2c. Zero-shot ReAct style prompt template (agent reasoning)
REACT_SYSTEM_PROMPT = (
    "You are a smart assistant. Think step by step.\n"
    "When you know the answer, reply with:\n"
    "Final Answer: <your answer>\n\n"
    "Question: {question}"
)
REACT_PROMPT = PromptTemplate(
    input_variables=["question"],
    template=REACT_SYSTEM_PROMPT,
)


# ════════════════════════════════════════════════════════════════
# BLOCK 3 — Chains (LCEL / pipe operator)
# ════════════════════════════════════════════════════════════════
def build_chains(llm):
    """
    Building Block #3: Chains
    LCEL: chain = prompt | llm | output_parser
    """
    parser = StrOutputParser()

    # Chain A: Simple Q&A
    qa_chain = SIMPLE_PROMPT | llm | parser

    # Chain B: Tutor / Explain chain
    tutor_chain = CHAT_PROMPT | llm | parser

    # Chain C: Simulated zero-shot ReAct reasoning chain
    react_chain = REACT_PROMPT | llm | parser

    return qa_chain, tutor_chain, react_chain


# ════════════════════════════════════════════════════════════════
# BLOCK 4 — Agent (zero-shot-react style tool use)
# ════════════════════════════════════════════════════════════════
def build_agent(llm):
    """
    Building Block #4: Agent
    Uses LangGraph's create_react_agent when langgraph is available,
    otherwise falls back to a simulated ReAct reasoning chain so the
    milestone works even with the minimal requirements.txt.
    """
    try:
        from langgraph.prebuilt import create_react_agent
        from langchain_core.tools import tool

        @tool
        def word_count(text: str) -> str:
            """Count the number of words in a given text string."""
            count = len(text.split())
            return f"The text contains {count} word(s)."

        @tool
        def reverse_text(text: str) -> str:
            """Reverse the characters in a given string."""
            return f"Reversed: {text[::-1]}"

        agent = create_react_agent(llm, tools=[word_count, reverse_text])
        return agent, "langgraph"

    except ImportError:
        # Fallback: plain ReAct-style LCEL chain (no tool loop)
        parser = StrOutputParser()
        chain = REACT_PROMPT | llm | parser
        return chain, "lcel"


# ════════════════════════════════════════════════════════════════
# Console Interface
# ════════════════════════════════════════════════════════════════
def run_demo(llm, qa_chain, tutor_chain, react_chain, agent, agent_type):
    """Interactive console demonstrating all four building blocks."""

    MODES = {
        "1": "Simple Q&A  (PromptTemplate + Chain)",
        "2": "Tutor/Explain  (ChatPromptTemplate + Chain)",
        "3": "ReAct Reasoning (zero-shot-react style Chain)",
        "4": "Agent  (tool-use: word_count / reverse_text)",
        "0": "Exit",
    }

    print(f"\n{DIVIDER}")
    print("  Milestone 1 — Foundational LangChain Agent")
    print("  Model : gemini-2.5-flash")
    print(f"  Agent type : {'LangGraph ReAct' if agent_type == 'langgraph' else 'LCEL ReAct chain'}")
    print(DIVIDER)
    print("\nBuilding blocks loaded:")
    print("  [1] LLM              — ChatGoogleGenerativeAI (Gemini)")
    print("  [2] Prompt Templates — PromptTemplate + ChatPromptTemplate")
    print("  [3] Chains           — LCEL pipe (prompt | llm | parser)")
    print("  [4] Agent            — Zero-shot ReAct with tools")

    while True:
        print(f"\n{'-' * 40}")
        print("Select mode:")
        for k, v in MODES.items():
            print(f"  [{k}] {v}")

        choice = input("\nChoice: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        elif choice == "1":
            question = input("Your question: ").strip()
            if not question:
                continue
            print("\nProcessing via Simple Q&A chain...")
            response = qa_chain.invoke({"question": question})
            print(f"\nAnswer:\n{response}")

        elif choice == "2":
            topic = input("Topic to explain: ").strip()
            if not topic:
                continue
            print("\nProcessing via Tutor chain...")
            response = tutor_chain.invoke({"topic": topic})
            print(f"\nExplanation:\n{response}")

        elif choice == "3":
            question = input("Question for ReAct reasoning: ").strip()
            if not question:
                continue
            print("\nProcessing via zero-shot ReAct chain...")
            response = react_chain.invoke({"question": question})
            print(f"\nReasoned Answer:\n{response}")

        elif choice == "4":
            if agent_type == "langgraph":
                print("\nAgent tools available:")
                print("  word_count(text)   — counts words in any text")
                print("  reverse_text(text) — reverses a string")
                query = input("Agent query (e.g. 'how many words in hello world?'): ").strip()
                if not query:
                    continue
                print("\nAgent is thinking...")
                result = agent.invoke({"messages": [("user", query)]})
                print(f"\nAgent Response:\n{result['messages'][-1].content}")
            else:
                query = input("Agent query: ").strip()
                if not query:
                    continue
                print("\nRunning ReAct chain (langgraph not installed)...")
                response = react_chain.invoke({"question": query})
                print(f"\nAnswer:\n{response}")

        else:
            print("Invalid choice. Please enter 0–4.")


# ════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════
def main():
    if not os.getenv("GOOGLE_API_KEY"):
        print("ERROR: GOOGLE_API_KEY is not set in .env")
        sys.exit(1)

    print("Initialising LangChain building blocks...")
    llm = get_llm()                                          # Block 1: LLM
    # Block 2: Prompts — defined as module-level templates above
    qa_chain, tutor_chain, react_chain = build_chains(llm)  # Block 3: Chains
    agent, agent_type = build_agent(llm)                     # Block 4: Agent

    run_demo(llm, qa_chain, tutor_chain, react_chain, agent, agent_type)


if __name__ == "__main__":
    main()
