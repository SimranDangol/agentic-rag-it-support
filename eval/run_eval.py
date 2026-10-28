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
judge = big.with_structured_output(ClaimCheck)


def load(n: int) -> list[dict]:
    with open("eval/dataset.jsonl", encoding="utf-8") as f:
        rows = [json.loads(line) for line in f if line.strip()]
    return rows[:n] if n else rows


def routing_acc(rows: list[dict]) -> float:
    ok = 0
    for r in rows:
        pred = route({"question": r["q"]})["route"]
        gold = "small_talk" if r["type"] == "small_talk" else "it_question"
        ok += pred == gold
        time.sleep(1)  # stay within Groq free-tier rate limits
    return ok / len(rows)


def hit_rate(rows: list[dict]) -> float:
    rows = [r for r in rows if r["expected_source"]]
    hits = sum(
        r["expected_source"] in [d["source"] for d in retrieve(r["q"])]
        for r in rows
    )
    return hits / len(rows)


def answer_quality(rows: list[dict]) -> dict:
    lat, total, bad = [], 0, 0
    for r in rows:
        if r["type"] != "it":
            continue
        t = time.time()
        out = graph.invoke(
            {"question": r["q"], "retries": 0, "steps": []},
            config={"recursion_limit": 15},
        )
        lat.append(time.time() - t)
        if out.get("context"):
            c = judge.invoke(
                f"Context:\n{out['context']}\n\nAnswer:\n{out['answer']}\n\n"
                "Count the factual claims in the answer and how many are NOT "
                "supported by the context."
            )
            total += c.total_claims
            bad += c.unsupported_claims
        time.sleep(2)
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
