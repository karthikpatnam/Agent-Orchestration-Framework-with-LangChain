import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

# ─────────────────────────────────────────────
# Helper: build LLM
# ─────────────────────────────────────────────
def get_llm(temperature: float = 0.3) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=temperature
    )


# ─────────────────────────────────────────────
# Research Agent
# Role: Deep-dive into a given topic, produce
#       detailed research bullet points.
# Memory: Own ConversationBufferMemory +
#         writes findings to shared VectorStore.
# ─────────────────────────────────────────────
class ResearchAgent:
    """Investigates a topic and stores findings in shared memory."""

    SYSTEM = (
        "You are an expert Research Agent. Your job is to produce "
        "thorough, factual bullet-point research on ANY topic given to you. "
        "Previous conversation context is provided so you can stay consistent. "
        "Always output 5-8 detailed, well-structured bullet points."
    )

    def __init__(self, individual_memory, shared_memory):
        self.individual_memory = individual_memory
        self.shared_memory = shared_memory
        self.llm = get_llm(temperature=0.3)

    def run(self, topic: str) -> str:
        print("\n[Research Agent] Investigating topic:", topic)

        # Pull this agent's own conversation history
        mem_vars = self.individual_memory.load_memory_variables({})
        history = mem_vars.get("research_chat_history", [])

        # Also pull any relevant prior findings from the shared VectorStore
        shared_ctx = ""
        try:
            shared_vars = self.shared_memory.load_memory_variables({"prompt": topic})
            shared_ctx = shared_vars.get("history", "")
            if shared_ctx:
                print("[Research Agent] Found relevant shared context — incorporating it.")
        except Exception:
            pass  # Shared store may be empty on the first call

        # Build the prompt
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=self.SYSTEM),
            MessagesPlaceholder(variable_name="history"),
            ("human",
             f"Shared knowledge base context:\n{shared_ctx}\n\n"
             f"Now research this topic thoroughly:\n{topic}")
        ])

        chain = prompt | self.llm
        response = chain.invoke({"history": history})
        findings = response.content

        # Save to individual buffer memory
        self.individual_memory.save_context(
            {"input": topic},
            {"output": findings}
        )

        # Save to shared VectorStore memory so other agents can retrieve it
        self.shared_memory.save_context(
            {"input": f"Research findings for: {topic}"},
            {"output": findings}
        )
        print("[Research Agent] Findings saved to shared memory.")

        return findings


# ─────────────────────────────────────────────
# Summarizer Agent
# Role: Take research findings and distil them
#       into a clean executive summary.
# Memory: Own ConversationBufferMemory +
#         reads from shared VectorStore.
# ─────────────────────────────────────────────
class SummarizerAgent:
    """Reads shared memory and synthesises a concise executive summary."""

    SYSTEM = (
        "You are a senior Summarizer Agent. Your job is to read raw research "
        "findings and produce a polished, professional executive summary. "
        "Structure the output with: "
        "1) A one-sentence TL;DR, "
        "2) 3-5 key takeaways, "
        "3) A one-paragraph conclusion."
    )

    def __init__(self, individual_memory, shared_memory):
        self.individual_memory = individual_memory
        self.shared_memory = shared_memory
        self.llm = get_llm(temperature=0.2)

    def run(self, topic: str, research_output: str) -> str:
        print("\n[Summarizer Agent] Summarizing findings for topic:", topic)

        # Pull own conversation history
        mem_vars = self.individual_memory.load_memory_variables({})
        history = mem_vars.get("summarizer_chat_history", [])

        # Query shared VectorStore for any older related work
        shared_ctx = ""
        try:
            shared_vars = self.shared_memory.load_memory_variables({"prompt": topic})
            shared_ctx = shared_vars.get("history", "")
            if shared_ctx:
                print("[Summarizer Agent] Retrieved shared knowledge — enriching summary.")
        except Exception:
            pass

        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=self.SYSTEM),
            MessagesPlaceholder(variable_name="history"),
            ("human",
             f"Shared knowledge base context (prior sessions):\n{shared_ctx}\n\n"
             f"Fresh research findings to summarise:\n{research_output}\n\n"
             f"Topic: {topic}")
        ])

        chain = prompt | self.llm
        response = chain.invoke({"history": history})
        summary = response.content

        # Save summary to individual memory
        self.individual_memory.save_context(
            {"input": f"Summarize: {topic}"},
            {"output": summary}
        )

        # Persist summary back to shared memory for future agents
        self.shared_memory.save_context(
            {"input": f"Executive summary for: {topic}"},
            {"output": summary}
        )
        print("[Summarizer Agent] Summary saved to shared memory.")

        return summary
