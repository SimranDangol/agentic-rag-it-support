"use client";

import { useEffect, useRef, useState } from "react";
import type { FormEvent, KeyboardEvent } from "react";
import Link from "next/link";

type Path = "KNOWLEDGE BASE" | "WEB" | "FALLBACK" | "DIRECT";
type Step = { node: string; sec: number };
type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  path?: Path;
  sources?: string[];
  steps?: Step[];
  latency?: number;
  error?: boolean;
};
type ChatResponse = {
  answer: string;
  path: Path;
  sources?: string[];
  steps?: Step[];
  latency?: number;
};

const suggestions = [
  { icon: "↻", label: "Reset my password", question: "How do I reset my password?" },
  { icon: "⌁", label: "Fix my VPN connection", question: "VPN keeps disconnecting" },
  { icon: "▣", label: "Set up MFA", question: "How do I set up MFA on my phone?" },
  { icon: "⌑", label: "Troubleshoot an error", question: "How do I fix Error 0x80070005?" },
];

const pathLabels: Record<Path, string> = {
  "KNOWLEDGE BASE": "Knowledge base",
  WEB: "Web search",
  FALLBACK: "Best effort",
  DIRECT: "Quick reply",
};

function isChatResponse(value: unknown): value is ChatResponse {
  if (typeof value !== "object" || value === null) return false;
  const data = value as Record<string, unknown>;
  return (
    typeof data.answer === "string" &&
    typeof data.path === "string" &&
    data.path in pathLabels
  );
}

function getErrorMessage(value: unknown): string {
  if (typeof value === "string") return value;
  if (typeof value === "object" && value !== null && "detail" in value) {
    return getErrorMessage(value.detail);
  }
  return "The request failed. Please try again.";
}

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [draft, setDraft] = useState("");
  const [pending, setPending] = useState(false);
  const [showSources, setShowSources] = useState(true);
  const [showPath, setShowPath] = useState(true);
  const [showSteps, setShowSteps] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages, pending]);

  async function sendMessage(rawMessage: string) {
    const message = rawMessage.trim();
    if (!message || pending) return;

    setMessages((current) => [
      ...current,
      { id: crypto.randomUUID(), role: "user", content: message },
    ]);
    setDraft("");
    setPending(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      const result: unknown = await response.json();
      if (!response.ok) throw new Error(getErrorMessage(result));
      if (!isChatResponse(result)) {
        throw new Error("The API returned an invalid chat response.");
      }

      setMessages((current) => [
        ...current,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: result.answer,
          path: result.path,
          sources: result.sources ?? [],
          steps: result.steps ?? [],
          latency: result.latency,
        },
      ]);
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content:
            error instanceof Error
              ? error.message
              : "Something went wrong while contacting the assistant.",
          error: true,
        },
      ]);
    } finally {
      setPending(false);
    }
  }

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void sendMessage(draft);
  }

  function handleKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      void sendMessage(draft);
    }
  }

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <Link className="brand" href="/" aria-label="IT Support Copilot home">
          <span className="brand-mark">it</span>
          <span className="brand-name">helpdesk<span>copilot</span></span>
        </Link>

        <button
          className="new-chat"
          onClick={() => !pending && setMessages([])}
          disabled={pending}
        >
          <span aria-hidden="true">＋</span> New conversation
        </button>

        <div className="sidebar-section">
          <p className="section-label">YOUR WORKSPACE</p>
          <div className="workspace-card">
            <span className="workspace-icon">A</span>
            <span><strong>Acme Corporation</strong><small>IT Support</small></span>
            <span className="chevron">⌄</span>
          </div>
        </div>

        <div className="sidebar-section">
          <p className="section-label">SUGGESTED TOPICS</p>
          {suggestions.map((item) => (
            <button
              className="topic-link"
              key={item.label}
              onClick={() => void sendMessage(item.question)}
              disabled={pending}
            >
              <span className="topic-icon">{item.icon}</span>{item.label}
            </button>
          ))}
        </div>

        <div className="sidebar-bottom">
          <div className="status-card">
            <span className="status-dot" />
            <span><strong>Support assistant online</strong><small>Answers grounded in your IT guide</small></span>
          </div>
          <div className="profile">
            <div className="avatar user-avatar">S</div>
            <span><strong>Simran</strong><small>Employee</small></span>
          </div>
        </div>
      </aside>

      <section className="main-panel">
        <header className="topbar">
          <div className="breadcrumb"><span>Workspace</span><b>/</b><strong>IT Support</strong></div>
          <div className="topbar-right">
            <span className="secure-label"><span>◇</span> Private workspace</span>
            <span className="help-button" aria-label="Help">?</span>
          </div>
        </header>

        <div className={`conversation ${messages.length ? "has-messages" : ""}`}>
          {messages.length === 0 ? (
            <section className="welcome">
              <div className="welcome-art" aria-hidden="true">
                <div className="art-orbit orbit-one" />
                <div className="art-orbit orbit-two" />
                <div className="art-center"><span>✳</span></div>
                <span className="art-spark spark-one">✦</span>
                <span className="art-spark spark-two">✧</span>
                <span className="art-spark spark-three">·</span>
              </div>
              <p className="eyebrow"><span className="status-dot" /> YOUR IT ASSISTANT</p>
              <h1>How can I help<br />you <span>today?</span></h1>
              <p className="welcome-copy">
                Get clear, step-by-step help with your workplace tech.
                Ask a question to get started.
              </p>
              <div className="suggestion-grid">
                {suggestions.map((item) => (
                  <button
                    className="suggestion-card"
                    key={item.label}
                    onClick={() => void sendMessage(item.question)}
                    disabled={pending}
                  >
                    <span className="suggestion-icon">{item.icon}</span>
                    <span>{item.label}</span>
                    <span className="card-arrow">↗</span>
                  </button>
                ))}
              </div>
              <p className="privacy-note"><span>◇</span> Responses are based on your company IT resources</p>
            </section>
          ) : (
            <div className="message-list">
              {messages.map((message) => (
                <article className={`message-row ${message.role}`} key={message.id}>
                  <div className={`avatar ${message.role === "assistant" ? "assistant-avatar" : "user-avatar"}`}>
                    {message.role === "assistant" ? "✳" : "S"}
                  </div>
                  <div className="message-content">
                    <div className="message-heading">
                      <strong>{message.role === "assistant" ? "Support Copilot" : "You"}</strong>
                      {message.role === "assistant" && !message.error && message.latency !== undefined && (
                        <span>{message.latency}s</span>
                      )}
                    </div>
                    {message.role === "assistant" && message.path && showPath && (
                      <span className={`path-badge path-${message.path.toLowerCase().replace(" ", "-")}`}>
                        <span />{pathLabels[message.path]}
                      </span>
                    )}
                    <div className={`message-bubble ${message.error ? "error-bubble" : ""}`}>
                      {message.content}
                    </div>
                    {message.role === "assistant" && !message.error && (
                      <div className="message-meta">
                        {showSources && message.sources && message.sources.length > 0 && (
                          <span className="source-list">Sources: {message.sources.join(", ")}</span>
                        )}
                        {showSteps && message.steps && message.steps.length > 0 && (
                          <details className="steps-details">
                            <summary>Agent steps</summary>
                            <ul>
                              {message.steps.map((step, index) => (
                                <li key={`${step.node}-${index}`}>
                                  <span>{step.node.replaceAll("_", " ")}</span><small>{step.sec}s</small>
                                </li>
                              ))}
                            </ul>
                          </details>
                        )}
                        {message.path === "FALLBACK" && (
                          <a className="helpdesk-link" href="mailto:helpdesk@acme.example">
                            Contact helpdesk · ext. 4357
                          </a>
                        )}
                      </div>
                    )}
                  </div>
                </article>
              ))}
              {pending && (
                <div className="message-row assistant">
                  <div className="avatar assistant-avatar">✳</div>
                  <div className="message-content">
                    <div className="message-heading"><strong>Support Copilot</strong></div>
                    <div className="typing-indicator" aria-label="Assistant is responding"><i /><i /><i /></div>
                  </div>
                </div>
              )}
              <div ref={bottomRef} />
            </div>
          )}
        </div>

        <footer className="composer-wrap">
          <div className="composer-options">
            <label><input type="checkbox" checked={showSources} onChange={(event) => setShowSources(event.target.checked)} /> Sources</label>
            <label><input type="checkbox" checked={showPath} onChange={(event) => setShowPath(event.target.checked)} /> Agent path</label>
            <label><input type="checkbox" checked={showSteps} onChange={(event) => setShowSteps(event.target.checked)} /> Steps</label>
          </div>
          <form className="composer" onSubmit={submit}>
            <textarea
              aria-label="Describe your IT issue"
              placeholder="Describe your IT issue..."
              value={draft}
              onChange={(event) => setDraft(event.target.value)}
              onKeyDown={handleKeyDown}
              rows={1}
              disabled={pending}
            />
            <button className="send-button" type="submit" disabled={pending || !draft.trim()} aria-label="Send message">
              {pending ? <span className="send-spinner" /> : <span>↑</span>}
            </button>
          </form>
          <p className="disclaimer">AI can make mistakes. Check important information with your IT team.</p>
        </footer>
      </section>
    </main>
  );
}