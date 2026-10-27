# Enterprise IT Support Agentic RAG Copilot

An agentic RAG system that routes employee IT questions across a private knowledge base, live web search, and an honest fallback — built with LangGraph, Groq, Pinecone, and Streamlit.

## Architecture

```
User Question
     │
     ▼
 [Router] ──small_talk──► [Direct Reply]
     │
  it_question
     │
     ▼
 [Retrieve] → hybrid BM25 + vector + RRF + cross-encoder rerank
     │
     ▼
[Grade Evidence]
     │
   kb_ok? ──no──► [Web Search] ──no results──► [Fallback]
     │                  │
    yes               yes
     │                  │
     └────────┬─────────┘
              ▼
          [Generate]
              │
              ▼
      [Check Grounding] ──not grounded (retry)──► [Generate]
              │                                        │
           grounded                          not grounded (2nd time)
              │                                        │
              ▼                                        ▼
           [END]                                  [Fallback]
```

## Stack

| Component | Tool |
|---|---|
| LLM | Groq (Llama 3.1 8B + 3.3 70B) |
| Vector DB | Pinecone Starter |
| Embeddings | all-MiniLM-L6-v2 (local) |
| Reranker | ms-marco cross-encoder (local) |
| BM25 | rank-bm25 |
| Web search | Tavily |
| Agent graph | LangGraph |
| API | FastAPI |
| UI | Streamlit |
| Tracing | LangSmith |
| Evaluation | RAGAS + custom harness |
| CI | GitHub Actions |
| Deployment | HuggingFace Spaces / Render |

## Setup

### 1. Clone and install

```bash
git clone https://github.com/YOUR_USERNAME/agentic-rag-it-support.git
cd agentic-rag-it-support
uv venv .venv --python 3.11
.venv\Scripts\activate          # Windows
uv pip install torch --index-url https://download.pytorch.org/whl/cpu
uv pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Fill in your API keys in .env
```

### 3. Ingest the knowledge base

```bash
python -m app.ingest
```

### 4. Run the API

```bash
uvicorn app.api:app --reload
# Open http://localhost:8000/docs
```

### 5. Run the UI

```bash
streamlit run ui/streamlit_app.py
```

## Evaluation

```bash
# Baseline (no hybrid, no rerank, no grounding)
$env:USE_HYBRID='0'; $env:USE_RERANK='0'; $env:USE_GROUNDING='0'
python -m eval.run_eval --tag baseline

# Final (everything on)
python -m eval.run_eval --tag final
```

## Results

| Metric | Baseline | Final | Sample size |
|---|---|---|---|
| Retrieval hit rate@4 | — | — | n = 50 |
| Unsupported claims % | — | — | n = — claims |
| Routing accuracy | — | — | 50 questions |
| Avg latency (s) | — | — | n = — |

> Numbers will be filled in after Phase 9 evaluation runs.

## Limitations

- Small synthetic knowledge base (24 documents, fictional company)
- Free-tier rate limits on Groq and Tavily
- LLM judge bias — spot-check manually
- Cold start latency on free hosting (~60s first request)

## License

MIT
