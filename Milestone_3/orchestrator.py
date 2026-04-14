"""
orchestrator.py — Milestone 3
==============================
Orchestrates a full multi-agent collaboration scenario:

  1. Research Agent   → Researches a user-supplied topic.
                        Saves findings to the shared VectorStore.
  2. Summarizer Agent → Reads shared VectorStore findings, enriches
                        with its own context, produces executive summary.

Memory layers:
  - Individual : ConversationBufferMemory per agent (short-term context).
  - Shared     : VectorStoreRetrieverMemory / FAISS (long-term cross-agent KB).

Follow-up queries demonstrate that shared memory guides future responses.
"""

import os
import sys

# Ensure the Milestone_3 directory is on the path
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv

# ── Load .env: check same dir first, then parent ────────────────────────────
_here = os.path.dirname(os.path.abspath(__file__))
for _candidate in [os.path.join(_here, '.env'), os.path.join(_here, '..', '.env')]:
    if os.path.exists(_candidate):
        load_dotenv(_candidate)
        break

from memory_setup import get_shared_memory, get_individual_memory
from agents import ResearchAgent, SummarizerAgent

# ─────────────────────────────────────────────
# Pretty print helper
# ─────────────────────────────────────────────
DIVIDER = "=" * 65

def banner(title: str):
    print(f"\n{DIVIDER}")
    print(f"  {title}")
    print(DIVIDER)

def section(label: str, content: str):
    print(f"\n--- {label} ---")
    print(content)


# ─────────────────────────────────────────────
# Orchestration logic
# ─────────────────────────────────────────────
def run_pipeline(topic: str, research_agent: ResearchAgent, summarizer_agent: SummarizerAgent):
    """Run the full Research → Summarize pipeline for a given topic."""
    banner(f"PIPELINE: {topic}")

    # Step 1 — Research
    research_output = research_agent.run(topic)
    section("RESEARCH AGENT OUTPUT", research_output)

    # Step 2 — Summarize (reads shared memory automatically)
    summary_output = summarizer_agent.run(topic, research_output)
    section("SUMMARIZER AGENT OUTPUT", summary_output)

    return research_output, summary_output


# ─────────────────────────────────────────────
# Main entry point
# ─────────────────────────────────────────────
def main():
    print(DIVIDER)
    print("  Multi-Agent Collaboration System  —  Milestone 3")
    print("  Agents : Research Agent | Summarizer Agent")
    print("  Memory : ConversationBufferMemory + VectorStoreRetrieverMemory")
    print(DIVIDER)

    # ── Validate API key ─────────────────────────────────────────────────────
    if not os.getenv("GOOGLE_API_KEY"):
        print("ERROR: GOOGLE_API_KEY is not set. Please add it to your .env file.")
        return

    # ── Initialise shared memory (FAISS vector store) ────────────────────────
    print("\nInitialising shared vector memory (FAISS + Gemini embeddings)...")
    try:
        shared_memory = get_shared_memory()
        print("Shared memory ready.")
    except Exception as e:
        print(f"ERROR: Could not initialise shared memory: {e}")
        return

    # ── Initialise individual memories ───────────────────────────────────────
    research_mem   = get_individual_memory("research")
    summarizer_mem = get_individual_memory("summarizer")

    # ── Wire up agents ───────────────────────────────────────────────────────
    research_agent   = ResearchAgent(research_mem, shared_memory)
    summarizer_agent = SummarizerAgent(summarizer_mem, shared_memory)

    print("\nAll agents online. Type 'exit' to quit.\n")

    # ── Interactive console loop ─────────────────────────────────────────────
    session_count = 0
    while True:
        try:
            user_topic = input("Enter a topic to research (or 'exit'): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Goodbye!")
            break

        if not user_topic:
            continue
        if user_topic.lower() in ("exit", "quit"):
            print("Exiting. Goodbye!")
            break

        session_count += 1
        try:
            run_pipeline(user_topic, research_agent, summarizer_agent)

            if session_count > 1:
                print(
                    "\n[Orchestrator] NOTE: The shared VectorStore now contains "
                    "context from previous topics. Both agents automatically "
                    "leveraged this cross-session memory in the responses above."
                )
        except Exception as e:
            print(f"\n[Orchestrator ERROR]: {e}")


if __name__ == "__main__":
    main()
