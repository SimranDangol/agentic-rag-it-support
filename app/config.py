import os

from dotenv import load_dotenv

load_dotenv()

# Set cache directories on F: drive to prevent C: drive exhaustion
if os.path.exists("F:/"):
    os.environ.setdefault("HF_HOME", "F:/hf_cache")
    os.environ.setdefault("TORCH_HOME", "F:/torch_cache")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

INDEX_NAME = "it-support-kb"
FAST_MODEL = "openai/gpt-oss-20b"  # router + graders
BIG_MODEL = "openai/gpt-oss-120b"  # answers
EMBED_MODEL = "all-MiniLM-L6-v2"       # 384 dimensions
EMBED_DIMENSION = 384
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
TOP_K = 4

# Feature flags: switch enhancements off to measure BASELINE in Phase 9
USE_HYBRID = os.getenv("USE_HYBRID", "1") == "1"
USE_RERANK = os.getenv("USE_RERANK", "1") == "1"
USE_GROUNDING = os.getenv("USE_GROUNDING", "1") == "1"
