from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms.fake import FakeListLLM
import random

#Static Knowledge Base
static_knowledge = {
    "langchain": "LangChain is a framework for building LLM-powered applications with chains, agents, and memory.",
    "python": "Python is a high-level, interpreted programming language known for simplicity and readability.",
    "ai": "Artificial Intelligence refers to the simulation of human intelligence by machines, particularly computer systems.",
    "agent": "An AI agent is a software program that can perceive its environment and take actions to achieve specific goals.",
    "llm": "A Large Language Model (LLM) is a neural network trained on vast amounts of text to understand and generate human language.",
    "langchain features": "LangChain features include: chains, agents, memory, tools integration, multiple LLM support, and prompt management.",
    "prompt": "A prompt is the input text given to an LLM to guide it in generating relevant responses.",
    "chain": "A chain in LangChain is a sequence of components (prompts, LLMs, output parsers) connected in a pipeline.",
    "default": "I'm a static query agent. I can answer questions about LangChain, Python, AI, and related topics."
}

def search_knowledge_base(query: str) -> str:
    """Search the static knowledge base with varied responses."""
    query_lower = query.lower()
    answer = None
    
    if query_lower in static_knowledge:
        answer = static_knowledge[query_lower]
    else:
        for key, value in static_knowledge.items():
            if query_lower in key or key in query_lower:
                answer = value
                break
    if not answer:
        answer = static_knowledge["default"]
    
    prefixes = [
        f"Based on my knowledge base: {answer}",
        f"Here's what I found: {answer}",
        f"According to my database: {answer}",
        f"The answer is: {answer}",
    ]
    
    return random.choice(prefixes)


def count_words(text: str) -> str:
    """Count words with varied response formats."""
    word_count = len(text.split())
    responses = [
        f"The text contains {word_count} words.",
        f"I counted {word_count} words in that text.",
        f"Word count: {word_count}",
        f"Your text has exactly {word_count} words."
    ]
    return random.choice(responses)


def answer_math_question(question: str) -> str:
    """Answer math questions with varied responses."""
    try:
        if 'bigger' in question.lower() or 'larger' in question.lower():
            parts = question.replace('?', '').split(',')
            if len(parts) >= 2:
                try:
                    num1 = float(parts[0].replace('Which number is', '').strip())
                    num2 = float(parts[1].strip())
                    bigger = max(num1, num2)
                    responses = [
                        f"{bigger} is the bigger number.",
                        f"The answer is {bigger} - that's the larger number.",
                        f"Comparing {num1} and {num2}: {bigger} wins!",
                        f"Between the two, {bigger} is bigger."
                    ]
                    return random.choice(responses)
                except:
                    return "I couldn't parse those numbers. Format: 'Which number is bigger, 9.11 or 9.8?'"
        return "I can help with math questions. Try: 'Which number is bigger, 9.11 or 9.8?'"
    except Exception as e:
        return f"Error processing question: {str(e)}"


def process_query(user_input: str) -> str:
    """
    Intelligently route queries to appropriate tools and generate varied responses.
    """
    query_lower = user_input.lower()
    
    if "word" in query_lower and "count" in query_lower:
        if "in" in query_lower:
            text = query_lower.split("in", 1)[1].strip().strip("'\"")
            if text:
                return count_words(text)
        return "Please ask: 'count words in <your text>'"
    
    elif "bigger" in query_lower or "larger" in query_lower or "which" in query_lower and "number" in query_lower:
        return answer_math_question(user_input)
    
    else:
        return search_knowledge_base(user_input)

#Console Interface
print("=" * 60)
print("Welcome to the LangChain Static Query Agent!")
print("=" * 60)
print("Ask questions about: LangChain, Python, AI, Agents, LLMs")
print("You can also ask: 'count words in <text>'")
print("Or math questions: 'which number is bigger, X or Y?'")
print("Type 'exit' to quit\n")

while True:
    try:
        user_input = input("\nYou: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() == "exit":
            print("\nAgent: Thank you for using the Static Query Agent. Goodbye!")
            break
        response = process_query(user_input)
        print(f"\nAgent: {response}")
        
    except KeyboardInterrupt:
        print("\n\nAgent: Session interrupted. Goodbye!")
        break
    except Exception as e:
        print(f"Error: {str(e)}")
