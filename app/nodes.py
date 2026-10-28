import time
from typing import TypedDict

from tavily import TavilyClient

from app import config
from app.llm import require_llm
from app.retrieval import retrieve

tavily = TavilyClient(api_key=config.TAVILY_API_KEY) if config.TAVILY_API_KEY else None


class State(TypedDict, total=False):
    question: str
    route: str
    docs: list
    kb_ok: bool
    web_results: list
    answer: str
    sources: list
    path: str
    grounded: bool
    retries: int
    feedback: str
    context: str
    steps: list


def timed(name: str):
    """Decorator that records per-node latency into state['steps']."""
    def deco(fn):
        def wrap(state):
            t = time.time()
            out = fn(state)
            out["steps"] = state.get("steps", []) + [
                {"node": name, "sec": round(time.time() - t, 2)}
            ]
            return out
        return wrap
    return deco


@timed("router")
def route(state: State) -> dict:
    llm = require_llm("router")
    r = llm.invoke(
        "Classify the message. 'it_question' = any technical/IT support problem or request. "
        "'small_talk' = greetings, thanks, chit-chat.\nMessage: " + state["question"]
    )
    return {"route": r.route}


@timed("direct")
def direct(state: State) -> dict:
    llm = require_llm("fast")
    msg = llm.invoke(
        "You are a friendly IT helpdesk bot. Reply in one short sentence and "
        "offer help with IT issues.\nUser: " + state["question"]
    )
    return {"answer": msg.content, "path": "DIRECT", "sources": [], "grounded": True}


@timed("retrieve")
def retrieve_node(state: State) -> dict:
    return {"docs": retrieve(state["question"])}


@timed("grade_evidence")
def grade_evidence(state: State) -> dict:
    llm = require_llm("evidence")
    ctx = "\n\n".join(d["text"] for d in state["docs"])
    g = llm.invoke(
        f"Question: {state['question']}\n\nContext:\n{ctx}\n\n"
        "Does the context contain enough information to answer the question? Be strict."
    )
    return {"kb_ok": g.sufficient == "yes"}


@timed("web_search")
def web_search(state: State) -> dict:
    if tavily is None:
        return {"web_results": []}
    try:
        res = tavily.search(state["question"], max_results=4)["results"]
    except Exception:
        res = []  # never crash the agent because a tool failed
    return {"web_results": res}


GEN_PROMPT = (
    "You are an IT support assistant. Answer ONLY from the context below. "
    "Give clear numbered steps. Cite sources in square brackets like [vpn_guide.md]. "
    "If the context lacks something, say so instead of guessing.\n"
    "{feedback}\nContext:\n{ctx}\n\nQuestion: {q}"
)


@timed("generate")
def generate(state: State) -> dict:
    llm = require_llm("big")
    if state.get("kb_ok"):
        ctx = "\n\n".join(f"[{d['source']}] {d['text']}" for d in state["docs"])
        sources = sorted({d["source"] for d in state["docs"]})
        path = "KNOWLEDGE BASE"
    else:
        ctx = "\n\n".join(f"[{r['url']}] {r['content']}" for r in state["web_results"])
        sources = [r["url"] for r in state["web_results"]]
        path = "WEB"

    fb = state.get("feedback", "")
    out = llm.invoke(GEN_PROMPT.format(feedback=fb, ctx=ctx, q=state["question"]))
    return {"answer": out.content, "sources": sources, "path": path, "context": ctx}


@timed("check_grounding")
def check_grounding(state: State) -> dict:
    if not config.USE_GROUNDING:
        return {"grounded": True}

    llm = require_llm("grounding")
    g = llm.invoke(
        f"Context:\n{state['context']}\n\nAnswer:\n{state['answer']}\n\n"
        "Is every factual claim in the answer supported by the context? "
        "List unsupported claims, if any."
    )

    if g.grounded == "yes":
        return {"grounded": True}

    fb = (
        "Your previous answer contained unsupported claims: "
        + "; ".join(g.unsupported_claims)
        + ". Remove them and use only the context."
    )
    return {"grounded": False, "retries": state.get("retries", 0) + 1, "feedback": fb}


@timed("fallback")
def fallback(state: State) -> dict:
    llm = require_llm("big")
    out = llm.invoke(
        "Give a short, careful best-effort answer to this IT question, and state "
        "clearly that you could not verify it against company documents.\n"
        + state["question"]
    )
    note = (
        "\n\nNote: I could not confirm this from our knowledge base or trusted web sources. "
        "Please contact the helpdesk (ext. 4357)."
    )
    return {"answer": out.content + note, "path": "FALLBACK", "sources": [], "grounded": False}
