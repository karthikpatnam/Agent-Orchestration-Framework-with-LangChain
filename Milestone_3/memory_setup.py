import os
import faiss
from dotenv import load_dotenv
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_classic.memory import ConversationBufferMemory, VectorStoreRetrieverMemory

# Load the environment variables (check local dir first, then parent)
_here = os.path.dirname(os.path.abspath(__file__))
for _candidate in [os.path.join(_here, '.env'), os.path.join(_here, '..', '.env')]:
    if os.path.exists(_candidate):
        load_dotenv(_candidate)
        break

# ─────────────────────────────────────────────────────────────────────────────
# Embedding strategy
# We try GoogleGenerativeAIEmbeddings with the latest model names.
# If all fail (API version mismatch, quota, etc.), we fall back to a
# sentence-transformers local embedding so the milestone can still run.
# ─────────────────────────────────────────────────────────────────────────────
def _build_embeddings():
    """Try Gemini embeddings; fall back to local HuggingFace if unavailable."""
    # Try each known Gemini embedding model name in turn
    for model_name in [
        "models/gemini-embedding-exp-03-07",
        "models/text-embedding-004",
        "models/embedding-001",
    ]:
        try:
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            emb = GoogleGenerativeAIEmbeddings(model=model_name)
            # Quick smoke test — this is where 404s surface
            emb.embed_query("test")
            print(f"Using Gemini embeddings: {model_name}")
            return emb, 768
        except Exception as exc:
            print(f"  Gemini '{model_name}' unavailable: {exc.__class__.__name__}")

    # Fallback → HuggingFace sentence-transformers (all-MiniLM-L6-v2, dim=384)
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        emb = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        print("Using local HuggingFace embeddings (all-MiniLM-L6-v2).")
        return emb, 384
    except Exception:
        pass

    # Last resort → random FakeEmbeddings (dim 128) just to prove architecture
    from langchain_community.embeddings import FakeEmbeddings
    print("WARNING: Using FakeEmbeddings. Semantic similarity will be random.")
    return FakeEmbeddings(size=128), 128


# Shared memory initialization (VectorStoreRetrieverMemory)
def get_shared_memory():
    embeddings, embedding_size = _build_embeddings()

    # Initialize a clean, empty FAISS index
    index = faiss.IndexFlatL2(embedding_size)
    vectorstore = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore({}),
        index_to_docstore_id={}
    )

    # Retriever: top-2 most relevant past documents
    retriever = vectorstore.as_retriever(search_kwargs=dict(k=2))
    shared_memory = VectorStoreRetrieverMemory(retriever=retriever)
    return shared_memory


# Short-term / Individual memory initialization
def get_individual_memory(agent_name: str):
    return ConversationBufferMemory(
        memory_key=f"{agent_name}_chat_history",
        return_messages=True
    )
