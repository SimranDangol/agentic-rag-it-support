import time

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.graph import graph

app = FastAPI(title="IT Support Copilot")


class ChatIn(BaseModel):
    message: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(body: ChatIn):
    t = time.time()
    try:
        out = graph.invoke(
            {"question": body.message, "retries": 0, "steps": []},
            config={"recursion_limit": 15},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "answer": out["answer"],
        "path": out["path"],
        "sources": out.get("sources", []),
        "grounded": out.get("grounded", False),
        "steps": out.get("steps", []),
        "latency": round(time.time() - t, 2),
    }
