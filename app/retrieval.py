import json
import re
from pathlib import Path

from rank_bm25 import BM25Okapi

from app import config

try:
    from pinecone import Pinecone
except ModuleNotFoundError:  # pragma: no cover - optional dependency in test env
    Pinecone = None

try:
    from sentence_transformers import CrossEncoder, SentenceTransformer
except ModuleNotFoundError:  # pragma: no cover - optional dependency in test env
    SentenceTransformer = None
    CrossEncoder = None


def tok(text: str) -> list[str]:
    """Tokenise, keeping tokens like 0x80070005."""
    return re.findall(r"[a-z0-9_.]+", text.lower())


def _load_chunks():
    chunks_path = Path(__file__).resolve().parents[1] / "data" / "chunks.json"
    if not chunks_path.exists():
        return []
    with chunks_path.open(encoding="utf-8") as fh:
        return json.load(fh)


CHUNKS = _load_chunks()
BY_ID = {c["id"]: c for c in CHUNKS}
bm25 = BM25Okapi([tok(c["text"]) for c in CHUNKS]) if CHUNKS else None

_embedder = None
_reranker = None
_index = None


def get_embedder():
    global _embedder
    if _embedder is None and SentenceTransformer is not None:
        _embedder = SentenceTransformer(config.EMBED_MODEL)
    return _embedder


def get_reranker():
    global _reranker
    if _reranker is None and CrossEncoder is not None:
        _reranker = CrossEncoder(config.RERANK_MODEL)
    return _reranker


def get_index():
    global _index
    key = config.PINECONE_API_KEY
    if _index is None and Pinecone is not None and key:
        try:
            _index = Pinecone(api_key=key).Index(config.INDEX_NAME)
        except Exception as e:
            print(f"Warning: Pinecone initialization skipped ({e}). Falling back to BM25 search.", flush=True)
            _index = None
    return _index


def vector_search(q: str, n: int = 20) -> list[str]:
    emb = get_embedder()
    idx = get_index()
    if emb is None or idx is None:
        return []
    v = emb.encode(q).tolist()
    res = idx.query(vector=v, top_k=n, include_metadata=True)
    return [m["id"] for m in res["matches"]]


def bm25_search(q: str, n: int = 20) -> list[str]:
    if not CHUNKS or bm25 is None:
        return []
    scores = bm25.get_scores(tok(q))
    top = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:n]
    return [CHUNKS[i]["id"] for i in top if scores[i] > 0]


def rrf(rank_lists: list[list[str]], k: int = 60) -> list[str]:
    """Reciprocal Rank Fusion — merges ranked lists without tuning score scales."""
    scores: dict[str, float] = {}
    for lst in rank_lists:
        for rank, cid in enumerate(lst):
            scores[cid] = scores.get(cid, 0) + 1.0 / (k + rank + 1)
    return sorted(scores, key=scores.get, reverse=True)


def expand_adjacent_chunks(docs: list[dict]) -> list[dict]:
    """Include neighboring chunks so retrieved procedures retain their surrounding steps."""
    source_order: list[str] = []
    chunk_numbers: dict[str, set[int]] = {}

    for doc in docs:
        source = doc.get("source")
        chunk_id = doc.get("id", "")
        prefix = f"{source}-" if source else ""
        if not prefix or not chunk_id.startswith(prefix):
            continue
        suffix = chunk_id[len(prefix) :]
        if not suffix.isdigit():
            continue
        if source not in chunk_numbers:
            source_order.append(source)
            chunk_numbers[source] = set()
        number = int(suffix)
        chunk_numbers[source].update((number - 1, number, number + 1))

    expanded = []
    for source in source_order:
        for number in sorted(chunk_numbers[source]):
            chunk = BY_ID.get(f"{source}-{number}")
            if chunk is not None and chunk["source"] == source:
                expanded.append(chunk)

    return expanded or docs


def retrieve(q: str, k: int = config.TOP_K) -> list[dict]:
    vec = vector_search(q)
    ids = rrf([vec, bm25_search(q)])[:20] if config.USE_HYBRID and vec else vec or bm25_search(q)
    cands = [BY_ID[i] for i in ids if i in BY_ID]

    if config.USE_RERANK and cands:
        rr = get_reranker()
        if rr is not None:
            scores = rr.predict([(q, c["text"]) for c in cands])
            ranked = sorted(zip(scores, cands), key=lambda x: x[0], reverse=True)
            cands = [c for _, c in ranked]

    return cands[:k]


def __getattr__(name):
    if name == "embedder":
        return get_embedder()
    if name == "reranker":
        return get_reranker()
    if name == "index":
        return get_index()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
