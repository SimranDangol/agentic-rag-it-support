import os
import requests
import streamlit as st

API = os.getenv("API_URL", "http://localhost:8000")
BADGE = {
    "KNOWLEDGE BASE": "green",
    "WEB": "orange",
    "FALLBACK": "red",
    "DIRECT": "blue",
}

st.set_page_config(page_title="IT Support Copilot", page_icon="🖥️")
st.title("🖥️ Enterprise IT Support Copilot")
st.caption("Ask about VPN, passwords, MFA, email, printers and more")

with st.sidebar:
    st.header("⚙️ Settings")
    show_sources = st.toggle("Show sources", True)
    show_path = st.toggle("Show agent path", True)
    show_steps = st.toggle("Show agent steps", False)
    if st.button("+ New chat"):
        st.session_state.clear()
        st.rerun()

    st.subheader("💡 Try asking:")
    examples = [
        "How do I reset my password?",
        "VPN keeps disconnecting",
        "Error 0x80070005 fix",
        "Set up MFA on my phone",
        "My printer is offline",
    ]
    for ex in examples:
        if st.button(ex, key=f"ex_{ex}"):
            st.session_state["pending"] = ex

if "msgs" not in st.session_state:
    st.session_state.msgs = []


def render(m: dict):
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m["role"] == "assistant":
            if show_path:
                color = BADGE.get(m["path"], "gray")
                st.badge(m["path"], color=color)
            st.caption(f"⏱ Latency: {m['latency']} s")
            if show_sources and m["sources"]:
                st.caption("📄 Sources: " + " | ".join(m["sources"]))
            if show_steps and m.get("steps"):
                with st.expander("Agent steps"):
                    for step in m["steps"]:
                        st.markdown(f"- **{step['node']}** — {step['sec']}s")
            if m["path"] == "FALLBACK":
                st.link_button("📞 Contact helpdesk", "mailto:helpdesk@acme.example")


for m in st.session_state.msgs:
    render(m)

q = st.chat_input("Describe your IT issue...") or st.session_state.pop("pending", None)

if q:
    st.session_state.msgs.append({"role": "user", "content": q})
    render(st.session_state.msgs[-1])

    with st.spinner("Thinking..."):
        try:
            r = requests.post(f"{API}/chat", json={"message": q}, timeout=120).json()
        except Exception as e:
            st.error(f"Could not reach the API: {e}")
            st.stop()

    st.session_state.msgs.append(
        {
            "role": "assistant",
            "content": r["answer"],
            "path": r["path"],
            "sources": r["sources"],
            "latency": r["latency"],
            "steps": r.get("steps", []),
        }
    )
    render(st.session_state.msgs[-1])
