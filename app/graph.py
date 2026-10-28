from langgraph.graph import END, StateGraph

from app.nodes import (
    State,
    check_grounding,
    direct,
    fallback,
    generate,
    grade_evidence,
    retrieve_node,
    route,
    web_search,
)

MAX_RETRIES = 1  # bounded retry: prevents infinite loops


def after_route(s: State) -> str:
    return "retrieve" if s["route"] == "it_question" else "direct"


def after_grade(s: State) -> str:
    return "generate" if s["kb_ok"] else "web_search"


def after_web(s: State) -> str:
    return "generate" if s.get("web_results") else "fallback"


def after_check(s: State) -> str:
    if s["grounded"]:
        return "end"
    # check_grounding already incremented retries: 1 = first failure -> retry once
    return "generate" if s.get("retries", 0) <= MAX_RETRIES else "fallback"


g = StateGraph(State)

for name, fn in [
    ("route", route),
    ("direct", direct),
    ("retrieve", retrieve_node),
    ("grade_evidence", grade_evidence),
    ("web_search", web_search),
    ("generate", generate),
    ("check_grounding", check_grounding),
    ("fallback", fallback),
]:
    g.add_node(name, fn)

g.set_entry_point("route")
g.add_conditional_edges("route", after_route, {"retrieve": "retrieve", "direct": "direct"})
g.add_edge("retrieve", "grade_evidence")
g.add_conditional_edges(
    "grade_evidence", after_grade, {"generate": "generate", "web_search": "web_search"}
)
g.add_conditional_edges(
    "web_search", after_web, {"generate": "generate", "fallback": "fallback"}
)
g.add_edge("generate", "check_grounding")
g.add_conditional_edges(
    "check_grounding",
    after_check,
    {"end": END, "generate": "generate", "fallback": "fallback"},
)
g.add_edge("direct", END)
g.add_edge("fallback", END)

graph = g.compile()
