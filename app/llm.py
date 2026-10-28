from langchain_groq import ChatGroq

from app import config
from app.schemas import EvidenceGrade, GroundingGrade, RouteDecision


def _make_llm(model_name: str, temperature: float):
    api_key = config.GROQ_API_KEY.strip()
    if not api_key:
        return None
    return ChatGroq(model=model_name, temperature=temperature, api_key=api_key)


fast = _make_llm(config.FAST_MODEL, 0)
big = _make_llm(config.BIG_MODEL, 0.1)

router_llm = (
    fast.with_structured_output(RouteDecision, method="json_schema", strict=True)
    if fast is not None
    else None
)
evidence_llm = (
    fast.with_structured_output(EvidenceGrade, method="json_schema", strict=True)
    if fast is not None
    else None
)
grounding_llm = (
    fast.with_structured_output(GroundingGrade, method="json_schema", strict=True)
    if fast is not None
    else None
)


def require_llm(llm_name: str):
    llm = {
        "fast": fast,
        "big": big,
        "router": router_llm,
        "evidence": evidence_llm,
        "grounding": grounding_llm,
    }.get(llm_name)
    if llm is None:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to your environment or .env file before running the app."
        )
    return llm
