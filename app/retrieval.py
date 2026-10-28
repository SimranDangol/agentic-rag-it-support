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

embedder = SentenceTransformer(config.EMBED_MODEL) if SentenceTransformer is not None else None
reranker = CrossEncoder(config.RERANK_MODEL) if CrossEncoder is not None else None
index = None
if Pinecone is not None and config.PINECONE_API_KEY:
    index = Pinecone(api_key=config.PINECONE_API_KEY).Index(config.INDEX_NAME)


def vector_search(q: str, n: int = 20) -> list[str]:
    if embedder is None or index is None:
        return []
    v = embedder.encode(q).tolist()
    res = index.query(vector=v, top_k=n, include_metadata=True)
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


def retrieve(q: str, k: int = config.TOP_K) -> list[dict]:
    vec = vector_search(q)
    ids = rrf([vec, bm25_search(q)])[:20] if config.USE_HYBRID and vec else vec or bm25_search(q)
    cands = [BY_ID[i] for i in ids if i in BY_ID]

    if config.USE_RERANK and cands and reranker is not None:
        scores = reranker.predict([(q, c["text"]) for c in cands])
        ranked = sorted(zip(scores, cands), key=lambda x: x[0], reverse=True)
        cands = [c for _, c in ranked]

    return cands[:k]
