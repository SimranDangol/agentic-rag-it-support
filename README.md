# Enterprise IT Support Agentic RAG Copilot

[![CI](https://github.com/SimranDangol/agentic-rag-it-support/actions/workflows/ci.yml/badge.svg)](https://github.com/SimranDangol/agentic-rag-it-support/actions/workflows/ci.yml)

An agentic RAG system that routes employee IT questions across three paths — a private knowledge base, live web search, and an honest "I don't know" fallback — while grounding every answer against retrieved context before returning it. Built with LangGraph, Groq, Pinecone, FastAPI, and Next.js. All metrics are measured by an automated evaluation harness and gated in CI on every push.

---

## Architecture

The agent is a **LangGraph state machine** with conditional edges. Every question is classified first; IT questions enter the retrieval pipeline, small talk gets a direct reply. Retrieved evidence is graded before generation, and every generated answer is checked for grounding before it leaves the pipeline.

<p align="center">
  <img src="docs/architecture.svg" alt="System Architecture" width="550" />
</p>

### Answer paths

| Badge | Trigger | Description |
|---|---|---|
| `KB` | KB evidence grades as sufficient | Answer generated from private knowledge base |
| `WEB` | KB grades as insufficient → web search returns results | Answer generated from Tavily web search results |
| `FALLBACK` | KB + web both insufficient, or grounding fails twice | Honest "I don't know" — no hallucinated answer |
| `DIRECT` | Router classifies question as `small_talk` | Friendly reply, no retrieval |

---

## Stack

| Component | Tool |
|---|---|
| LLM (router / grader) | Groq — `openai/gpt-oss-20b` |
| LLM (generator / judge) | Groq — `openai/gpt-oss-120b` |
| Vector store | Pinecone Starter (384-dim, cosine) |
| Embeddings | `all-MiniLM-L6-v2` (local, sentence-transformers) |
| Reranker | `ms-marco-MiniLM-L-6-v2` cross-encoder (local) |
| BM25 | rank-bm25 |
| Fusion | Reciprocal Rank Fusion (RRF) |
| Web search | Tavily Search API |
| Agent graph | LangGraph |
| API | FastAPI |
| UI | Next.js 15 + React 19 + TypeScript |
| Tracing | LangSmith |
| Evaluation | Custom harness (`eval/run_eval.py`) |
| CI | GitHub Actions |

---

## Results

Measured by `eval/run_eval.py` over `eval/dataset.jsonl` (87 questions: 72 KB-mapped, 5 out-of-KB, 10 small-talk). The LLM judge for answer quality is the 120B model (`openai/gpt-oss-120b`) — a different model from the in-pipeline grader to avoid self-grading bias.

| Metric | Baseline | Full Pipeline | How measured |
|---|---|---|---|
| Retrieval hit rate@4 | 100% (72/72) | **97.2%** (70/72) | Expected source doc in top-4 retrieved chunks |
| Routing accuracy | 100% (87/87) | **98.9%** (86/87) | Predicted route matches ground-truth label |
| Avg answer latency | 7.74 s | **12.72 s** | Wall-clock `graph.invoke()` per IT question |
| Unsupported claims % | 10.6% | **0.8%** | 120B judge counts claims not backed by context |

> **Baseline** = `USE_HYBRID=0, USE_RERANK=0, USE_GROUNDING=0` (plain dense-vector search, no reranking, no grounding check).
>
> **Full pipeline** = `USE_HYBRID=1, USE_RERANK=1, USE_GROUNDING=1` — hybrid BM25+vector retrieval with Reciprocal Rank Fusion, Cross-Encoder reranking, and a grounding check that regenerates the answer if unsupported claims are detected. The latency increase is the cost of reranking and the extra grounding LLM call; the payoff is a **~92% reduction in unsupported claims** (10.6% → 0.8%).

---

## KPIs & Success Metrics

The following measurable thresholds define project success. They are enforced automatically in CI via `eval/thresholds.json`.

| KPI | Target | Actual (Full Pipeline) | Status |
|---|---|---|---|
| Retrieval hit rate@4 | ≥ 75% | **97.2%** | ✅ |
| Routing accuracy | ≥ 90% | **98.9%** | ✅ |
| Unsupported claims % | < 5% | **0.8%** | ✅ |
| KB answer latency | < 30 s | **12.72 s avg** | ✅ |
| CI unit test pass rate | 100% | **100%** (8/8) | ✅ |

**Failure indicators** to monitor in production:
- Hit rate@4 drops below 75% → KB has drifted; re-ingest documents.
- Routing accuracy drops below 90% → Router prompt needs tuning.
- Unsupported claims exceed 10% → Grounding model or generation prompt has regressed.
- Latency exceeds 30 s consistently → Consider caching embeddings or upgrading Groq tier.

---

## Design Decisions

### Why Python?
Python is the standard language for ML/AI pipelines. Every relevant library — LangChain, LangGraph, sentence-transformers, Pinecone, Tavily, FastAPI — has a mature, well-maintained Python SDK. Using anything else would mean writing adapter layers from scratch.

### Why LangGraph?
LangGraph models the agent as a **typed state machine with conditional edges**, which makes the control flow explicit and debuggable. The alternative (bare LangChain `AgentExecutor`) uses a black-box loop that is hard to trace, test, or constrain. LangGraph lets us:
- Define exactly when to retry (bounded `MAX_RETRIES = 1`).
- Add a grounding check as a first-class graph node rather than a prompt hack.
- Visualise the graph and trace every node's latency via `steps`.

### Why Groq?
Groq's inference hardware (LPUs) gives sub-second latency on large models with a simple OpenAI-compatible API. The project needs two model sizes — a fast 20B for classification/grading and a large 120B for generation — without managing GPU infrastructure. Groq covers both on a free tier with a single API key.

### Why Pinecone?
Pinecone is a managed vector database with a generous free Starter tier (100k vectors). Alternatives like Weaviate or Qdrant require self-hosting. Pinecone handles index sharding, replication, and approximate nearest-neighbour search transparently, letting the project focus on retrieval quality rather than infrastructure.

### Why local sentence-transformers (not an API)?
Running `all-MiniLM-L6-v2` locally means:
1. **Zero embedding cost** — no API call or token count.
2. **Deterministic** — the same text always produces the same vector, so the BM25 and Pinecone indices stay in sync.
3. **CI-friendly** — the smoke evaluation works without network access to an embedding API.

### Why Hybrid BM25 + Vector + RRF?
Dense vector search excels at semantic similarity; BM25 excels at exact keyword matches (error codes like `0x80070005`, product names). Combining both with Reciprocal Rank Fusion (RRF) is parameter-free and consistently outperforms either method alone on mixed IT queries.

### Why a Cross-Encoder reranker?
Bi-encoder embeddings (used by Pinecone) rank by cosine similarity of independent encodings. A Cross-Encoder reads query and document *together*, giving much better relevance scores at the cost of running N forward passes. Using it only on the top-20 candidates from RRF keeps latency reasonable while improving precision.

### Why FastAPI?
FastAPI provides automatic OpenAPI docs (`/docs`), Pydantic validation, and async support in ~40 lines. The API surface is small (health + chat), so a lightweight framework is the right choice. Django or Flask would add significant boilerplate with no benefit.

### Why Next.js 15 + TypeScript (not Streamlit)?
Streamlit is fast to prototype but produces apps that look and behave like developer tools. Next.js produces a production-quality, responsive UI that works on mobile. TypeScript catches API contract mismatches at compile time (e.g. if the backend changes the response shape). The App Router + React Server Components also allow the `/api/chat` proxy route to run server-side, keeping the FastAPI URL hidden from the browser.

---

## UML Diagrams

### Sequence Diagram — Query Flow

```mermaid
sequenceDiagram
    actor User
    participant UI as Next.js UI
    participant API as FastAPI
    participant Graph as LangGraph
    participant Router as route node
    participant Retriever as retrieve node
    participant Grader as grade_evidence node
    participant Web as web_search node
    participant Generator as generate node
    participant Grounder as check_grounding node

    User->>UI: Submit question
    UI->>API: POST /chat {message}
    API->>Graph: graph.invoke({question})
    Graph->>Router: classify question
    Router-->>Graph: route = "it_question"
    Graph->>Retriever: hybrid BM25+vector search
    Retriever-->>Graph: top-4 docs (expanded)
    Graph->>Grader: is evidence sufficient?
    alt KB evidence sufficient
        Grader-->>Graph: kb_ok = true
        Graph->>Generator: generate answer from KB docs
    else KB insufficient
        Grader-->>Graph: kb_ok = false
        Graph->>Web: Tavily web search
        alt Web results found
            Web-->>Graph: web_results
            Graph->>Generator: generate answer from web results
        else No web results
            Web-->>Graph: empty
            Graph-->>API: FALLBACK answer
        end
    end
    Generator-->>Graph: answer + context
    Graph->>Grounder: check every claim vs context
    alt Answer grounded
        Grounder-->>Graph: grounded = true
        Graph-->>API: answer + path + sources
    else Ungrounded, retries left
        Grounder-->>Graph: grounded = false, feedback
        Graph->>Generator: regenerate with feedback
    else Ungrounded, retries exhausted
        Grounder-->>Graph: grounded = false
        Graph-->>API: FALLBACK answer
    end
    API-->>UI: {answer, path, sources, latency}
    UI-->>User: Display answer with citations
```

### Class Diagram — Core Components

```mermaid
classDiagram
    class State {
        +str question
        +str route
        +list docs
        +bool kb_ok
        +list web_results
        +str answer
        +list sources
        +str path
        +bool grounded
        +int retries
        +str feedback
        +str context
        +list steps
    }

    class LangGraph {
        +StateGraph g
        +compile() graph
        +add_node(name, fn)
        +add_conditional_edges()
    }

    class Nodes {
        +route(state) dict
        +direct(state) dict
        +retrieve_node(state) dict
        +grade_evidence(state) dict
        +web_search(state) dict
        +generate(state) dict
        +check_grounding(state) dict
        +fallback(state) dict
    }

    class RetrievalPipeline {
        +BM25Okapi bm25
        +SentenceTransformer embedder
        +CrossEncoder reranker
        +Pinecone index
        +retrieve(q, k) list
        +rrf(rank_lists) list
        +expand_adjacent_chunks(docs) list
        +vector_search(q, n) list
        +bm25_search(q, n) list
    }

    class LLMSetup {
        +ChatGroq fast
        +ChatGroq big
        +router_llm
        +evidence_llm
        +grounding_llm
        +require_llm(name) ChatGroq
    }

    class FastAPIApp {
        +GET /health()
        +POST /chat(body)
    }

    class Schemas {
        +RouteDecision
        +EvidenceGrade
        +GroundingGrade
    }

    LangGraph --> State : manages
    LangGraph --> Nodes : executes
    Nodes --> RetrievalPipeline : calls retrieve()
    Nodes --> LLMSetup : calls require_llm()
    LLMSetup --> Schemas : structured output
    FastAPIApp --> LangGraph : graph.invoke()
```

---

## Reflection

### What I'd design differently

**1. Streaming responses instead of blocking HTTP**
The current `/chat` endpoint blocks until the full answer is generated (~12 s average). A streaming response (Server-Sent Events or WebSocket) would let the UI render the answer token-by-token, dramatically improving perceived performance. FastAPI supports `StreamingResponse` natively; LangGraph supports `astream_events`. This would be the first change in a production version.

**2. Persistent conversation history**
The agent treats every question as independent. A real IT copilot needs multi-turn memory — if a user says "I did step 3, now what?", the agent has no context. I would add a `thread_id`-based message store (Redis or a database) and pass conversation history into the router's context window.

**3. Separate embedding service**
Loading `all-MiniLM-L6-v2` and the Cross-Encoder at startup adds ~30 s cold-start time and ~800 MB RAM. In production I would run these as a dedicated microservice (e.g. a FastAPI sidecar) with a warm model, so the main API process starts instantly and scales independently of the ML models.

**4. Authentication before anything else**
The API has no auth. Any endpoint on a public host is open to anyone. Before deploying, I would add API-key middleware (a simple `X-API-Key` header check) or OAuth2 at the gateway level. This was consciously deferred to keep the prototype simple, but it is not optional for a real deployment.

**5. Structured KB with metadata filters**
All 24 KB documents are searched together. For a larger corpus (thousands of documents), queries about VPN should not search printer guides. I would add category metadata to each chunk at ingest time and pass a Pinecone namespace or metadata filter with every query so retrieval is scoped to the relevant topic area.

**6. Human-in-the-loop escalation**
Currently the FALLBACK node appends "contact the helpdesk (ext. 4357)" as plain text. A proper escalation path would open a ticket in a ticketing system (Jira Service Management, ServiceNow) via API, attach the conversation transcript, and return a ticket number to the user — turning a failed RAG lookup into a productive support interaction.

---

### 1. Clone and install

```bash
git clone https://github.com/SimranDangol/agentic-rag-it-support.git
cd agentic-rag-it-support
uv venv .venv --python 3.11
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

uv pip install torch --index-url https://download.pytorch.org/whl/cpu
uv pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and fill in your keys
```

On Windows PowerShell, use:

```powershell
Copy-Item .env.example .env
```

Required keys in `.env`:

```
GROQ_API_KEY=...        # https://console.groq.com
PINECONE_API_KEY=...    # https://app.pinecone.io
TAVILY_API_KEY=...      # https://app.tavily.com
LANGSMITH_API_KEY=...   # https://smith.langchain.com (optional — for tracing)
```

### 3. Ingest the knowledge base

```bash
python -m app.ingest
```

Embeds the 24 Markdown documents in `data/kb/`, uploads 127 chunks to Pinecone (`it-support-kb` index), and writes `data/chunks.json` for local BM25. Run once; commit `data/chunks.json` so Docker and CI can use the same KB without re-ingesting.

### 4. Run the API

```bash
uvicorn app.api:app --reload
```

Open http://localhost:8000/docs to explore the endpoints.

### 5. Run the UI

```bash
cd web
pnpm install
pnpm dev
```

Open http://localhost:3000. The Next.js dev server proxies `/api/chat` to the FastAPI backend at `http://127.0.0.1:8000`. To point at a hosted backend, set `API_URL` in `web/.env.local` and restart.

### 6. Run evaluation

```bash
# Full evaluation (all metrics, requires all API keys)
python -m eval.run_eval --tag full

# CI smoke test (retrieval only, no Groq API calls, ~60 s)
python -m eval.run_eval --limit 10 --tag ci --gate

# Baseline (no hybrid / rerank / grounding)
$env:USE_HYBRID='0'; $env:USE_RERANK='0'; $env:USE_GROUNDING='0'
python -m eval.run_eval --tag baseline

# Final (everything on)
python -m eval.run_eval --tag final
```

Results are appended to `eval/results.jsonl`. Pass `--gate` to fail with exit code 1 if any metric misses its threshold in `eval/thresholds.json`.

---

## Testing

Run these checks from the project root after installing the Python dependencies:

```powershell
# Unit tests (no external services required)
python -m pytest -q tests

# Python lint (install Ruff first if needed: uv pip install ruff)
ruff check .
```

The unit tests cover the API health/validation responses, Markdown chunking, and retrieval ranking. They do not send a real chat request to the LLM.

Check the frontend separately:

```powershell
cd web
pnpm install --frozen-lockfile
pnpm lint
pnpm build
```

For an end-to-end manual check, start the API and UI in separate terminals. First configure `.env`, ingest the knowledge base (Setup step 3), and start the API from the project root:

```powershell
uvicorn app.api:app --reload
```

Check API availability in another terminal:

```powershell
Invoke-RestMethod http://localhost:8000/health
# Expected: status = ok

Invoke-RestMethod -Method Post `
  -Uri http://localhost:8000/chat `
  -ContentType "application/json" `
  -Body '{"message":"How do I reset my password?"}'
```

The chat response should include an `answer`, a `path`, and a `sources` list. Then start the frontend from the `web/` directory with `pnpm dev`, open http://localhost:3000, and submit a suggested question. The UI should display the answer and its source/path metadata. Resize the browser to a phone-sized viewport to check that the header, new-conversation button, chat, and composer fit without horizontal scrolling. To check that multi-part procedures are returned completely, ask: `According to Acme IT, what should I do if GlobalProtect keeps disconnecting every few minutes?` The answer should use the knowledge base and preserve the troubleshooting steps in the VPN guide's order. If the API is hosted elsewhere, set `API_URL` in `web/.env.local` and restart the frontend.

The retrieval smoke evaluation uses the Pinecone index and downloads/loads the local embedding model, but makes no Groq calls:

```powershell
python -m eval.run_eval --limit 10 --tag ci --gate
```

Run the full evaluation only when the required services and API keys are configured; it makes live LLM/search calls, can be rate-limited, and appends results to `eval/results.jsonl`:

```powershell
python -m eval.run_eval --tag full
```

---

## CI

GitHub Actions runs on every push and pull request to `main`:

1. **Lint** — `ruff check .`
2. **Unit tests** — `pytest -q tests` (8 tests)
3. **Smoke eval** — `python -m eval.run_eval --limit 10 --tag ci --gate`
   - Runs retrieval hit rate@4 only (uses the local embedding model and configured retrieval pipeline; no Groq calls)
   - Gates: `hit_rate_at_4 ≥ 0.75`

The smoke evaluation needs `PINECONE_API_KEY`; it does not call Groq or Tavily. Configure `GROQ_API_KEY` and `TAVILY_API_KEY` for full live evaluations. `LANGSMITH_API_KEY` is optional and is only needed when tracing is enabled.

---

## Project structure

```
agentic-rag-it-support/
├── app/
│   ├── config.py        # env vars, feature flags (USE_HYBRID, USE_RERANK, USE_GROUNDING)
│   ├── graph.py         # LangGraph state machine
│   ├── nodes.py         # route, retrieve, grade_evidence, generate, check_grounding, fallback
│   ├── retrieval.py     # hybrid BM25 + vector + RRF + cross-encoder rerank
│   ├── llm.py           # Groq LLM setup
│   ├── ingest.py        # KB ingestion pipeline
│   └── api.py           # FastAPI endpoints
├── web/                 # Next.js 15 frontend
├── docs/                # Architecture and UML diagrams (SVG)
├── data/
│   ├── kb/              # 24 Markdown knowledge-base documents
│   └── chunks.json      # BM25 corpus (committed after ingestion)
├── eval/
│   ├── dataset.jsonl    # 87-question evaluation dataset
│   ├── run_eval.py      # evaluation harness
│   ├── thresholds.json  # quality gate thresholds
│   └── results.jsonl    # appended eval results
├── tests/               # pytest unit tests
├── .github/workflows/
│   └── ci.yml           # GitHub Actions CI
├── Dockerfile
└── requirements.txt
```

---

## Limitations

- **Small synthetic KB** — 24 documents covering a fictional company. Real-world accuracy requires a domain-specific corpus.
- **Free-tier rate limits** — Groq free tier (~6 000 TPM) throttles batch evaluation. The CI smoke test avoids LLM calls to stay within limits.
- **LLM-judge bias** — The 120B judge scores its own model family's outputs. Spot-check a sample of flagged answers manually.
- **Cold-start latency** — Free hosting tiers (Render, HF Spaces) sleep after inactivity; first request may take ~60 s to wake the container.
- **No auth / multi-tenancy** — The API has no authentication layer. Add an API-key middleware before any production use.
