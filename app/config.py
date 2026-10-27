import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

INDEX_NAME = "it-support-kb"
FAST_MODEL = "llama-3.1-8b-instant"   # router + graders
BIG_MODEL = "llama-3.3-70b-versatile"  # answers
EMBED_MODEL = "all-MiniLM-L6-v2"       # 384 dimensions
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
TOP_K = 4

# Feature flags: switch enhancements off to measure BASELINE in Phase 9
USE_HYBRID = os.getenv("USE_HYBRID", "1") == "1"
USE_RERANK = os.getenv("USE_RERANK", "1") == "1"
USE_GROUNDING = os.getenv("USE_GROUNDING", "1") == "1"
