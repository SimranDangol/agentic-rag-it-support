import argparse
import json
import sys
import time

from pydantic import BaseModel

from app import config
from app.graph import graph
from app.llm import big
from app.nodes import route
from app.retrieval import retrieve


class ClaimCheck(BaseModel):
    total_claims: int
    unsupported_claims: int


# 70B judge — different from the 8B in-pipeline grader to avoid self-grading bias
judge = (
    big.with_structured_output(ClaimCheck, method="json_schema", strict=True)
    if big is not None
    else None
)


def invoke_with_retry(fn, *args, max_retries=5, **kwargs):
    for attempt in range(max_retries):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            err_msg = str(e).lower()
            if "429" in err_msg or "rate_limit" in err_msg:
                wait = 10 * (attempt + 1)
                print(f"  [Rate limit hit, waiting {wait}s before retry {attempt + 1}/{max_retries}...]", flush=True)
                time.sleep(wait)
            elif attempt == max_retries - 1:
                raise
            else:
                time.sleep(2)
    raise RuntimeError(f"Exceeded {max_retries} retries due to persistent rate limiting.")


def load(n: int) -> list[dict]:
    with open("eval/dataset.jsonl", encoding="utf-8") as f:
        rows = [json.loads(line) for line in f if line.strip()]
    return rows[:n] if n else rows


def routing_acc(rows: list[dict]) -> float:
    ok = 0
    print(f"Evaluating routing accuracy across {len(rows)} samples...", flush=True)
    for i, r in enumerate(rows):
        pred = invoke_with_retry(route, {"question": r["q"]})["route"]
        gold = "small_talk" if r["type"] == "small_talk" else "it_question"
        ok += pred == gold
        time.sleep(0.5)  # stay within Groq free-tier rate limits
    acc = round(ok / len(rows), 4) if rows else 0.0
    print(f"Routing accuracy: {acc * 100:.1f}% ({ok}/{len(rows)})", flush=True)
    return acc


def hit_rate(rows: list[dict]) -> float:
    eval_rows = [r for r in rows if r.get("expected_source")]
    if not eval_rows:
        return 0.0
    print(f"Evaluating retrieval hit rate@4 across {len(eval_rows)} KB queries...", flush=True)
    hits = 0
    for i, r in enumerate(eval_rows):
        retrieved_docs = retrieve(r["q"])
        sources = [d["source"] for d in retrieved_docs]
        if r["expected_source"] in sources:
            hits += 1
    hr = round(hits / len(eval_rows), 4)
    print(f"Hit rate@4: {hr * 100:.1f}% ({hits}/{len(eval_rows)})", flush=True)
    return hr


def answer_quality(rows: list[dict]) -> dict:
    it_rows = [r for r in rows if r["type"] == "it"]
    print(f"Evaluating answer quality across {len(it_rows)} IT questions...", flush=True)
    lat, total, bad = [], 0, 0
    for i, r in enumerate(it_rows):
        t = time.time()
        try:
            out = invoke_with_retry(
                graph.invoke,
                {"question": r["q"], "retries": 0, "steps": []},
                config={"recursion_limit": 15},
            )
            elapsed = time.time() - t
            lat.append(elapsed)
            if out and out.get("context") and judge is not None:
                time.sleep(2)
                c = invoke_with_retry(
                    judge.invoke,
                    f"Context:\n{out['context']}\n\nAnswer:\n{out['answer']}\n\n"
                    "Count the factual claims in the answer and how many are NOT "
                    "supported by the context.",
                )
                if hasattr(c, "total_claims"):
                    total += c.total_claims
                    bad += c.unsupported_claims
                    print(
                        f"  [{i+1}/{len(it_rows)}] Path: {out.get('path', 'UNKNOWN')} | "
                        f"Latency: {elapsed:.2f}s | Claims: {c.total_claims} (Unsupported: {c.unsupported_claims})",
                        flush=True,
                    )
            elif out:
                print(
                    f"  [{i+1}/{len(it_rows)}] Path: {out.get('path', 'UNKNOWN')} | Latency: {elapsed:.2f}s",
                    flush=True,
                )
        except Exception as e:
            print(f"  [{i+1}/{len(it_rows)}] Warning for query '{r['q']}': {e}", flush=True)
        time.sleep(2.5)

    return {
        "avg_latency_s": round(sum(lat) / len(lat), 2) if lat else 0,
        "unsupported_pct": round(100 * bad / max(total, 1), 1),
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="run")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--gate", action="store_true")
    a = ap.parse_args()

    rows = load(a.limit)
    res = {
        "tag": a.tag,
        "hybrid": config.USE_HYBRID,
        "rerank": config.USE_RERANK,
        "grounding": config.USE_GROUNDING,
        "hit_rate_at_4": hit_rate(rows),
        "routing_acc": routing_acc(rows),
        **answer_quality(rows),
    }

    print(json.dumps(res, indent=2))

    with open("eval/results.jsonl", "a") as f:
        f.write(json.dumps(res) + "\n")

    if a.gate:
        with open("eval/thresholds.json", encoding="utf-8") as f:
            th = json.load(f)
        fails = [
            k
            for k, v in th.items()
            if (res[k] < v if not k.startswith("max_") else res[k[4:]] > v)
        ]
        if fails:
            print("QUALITY GATE FAILED:", fails)
            sys.exit(1)
        print("Quality gate passed ✓")
