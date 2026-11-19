"use client";

import { useEffect, useRef, useState } from "react";
import type { FormEvent, KeyboardEvent } from "react";
import ReactMarkdown from "react-markdown";

export type UserProfile = {
  id: string;
  name: string;
  email: string;
  role: string;
  department: string;
  avatar: string;
};

function formatContent(raw: string): string {
  // Convert 【source.md】 or 【http...】 citations into cleaner inline markdown syntax
  return raw.replace(/【([^】]+)】/g, (_, source) => {
    const trimmed = String(source).trim();
    if (trimmed.startsWith("http://") || trimmed.startsWith("https://")) {
      try {
        const host = new URL(trimmed).hostname.replace(/^www\./, "");
        return ` [↗ ${host}](${trimmed})`;
      } catch {
        return ` [↗ link](${trimmed})`;
      }
    }
    return ` \`📄 ${trimmed}\``;
  });
}

function MarkdownRenderer({ content }: { content: string }) {
  const formatted = formatContent(content);

  return (
    <div className="markdown-body">
      <ReactMarkdown
        components={{
          code({ className, children, ...props }) {
            const text = String(children);
            if (text.startsWith("📄 ")) {
              return (
                <span className="citation-pill">
                  <span className="citation-pill-icon">📄</span>
                  <span>{text.slice(2)}</span>
                </span>
              );
            }
            return (
              <code className={`inline-code ${className ?? ""}`.trim()} {...props}>
                {children}
              </code>
            );
          },
          a({ href, children, ...props }) {
            return (
              <a
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                className="markdown-link"
                {...props}
              >
                {children}
              </a>
            );
          },
        }}
      >
        {formatted}
      </ReactMarkdown>
    </div>
  );
}

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
  const [user, setUser] = useState<UserProfile | null>(null);
  const [authLoading, setAuthLoading] = useState(true);
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [loginError, setLoginError] = useState("");
  const [loginSubmitting, setLoginSubmitting] = useState(false);

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [draft, setDraft] = useState("");
  const [pending, setPending] = useState(false);
  const [showSources, setShowSources] = useState(true);
  const [showPath, setShowPath] = useState(true);
  const [showSteps, setShowSteps] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    async function checkAuth() {
      try {
        const res = await fetch("/api/auth/me");
        if (res.ok) {
          const data = await res.json();
          if (data.authenticated && data.user) {
            setUser(data.user);
          }
        }
      } catch {
        // Fallback or unauthenticated
      } finally {
        setAuthLoading(false);
      }
    }
    void checkAuth();
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages, pending]);

  async function handleLogin(emailToUse?: string, passwordToUse?: string) {
    const targetEmail = (emailToUse ?? loginEmail).trim();
    const targetPassword = (passwordToUse ?? loginPassword).trim();
    if (!targetEmail) {
      setLoginError("Please enter your corporate email.");
      return;
    }
    setLoginError("");
    setLoginSubmitting(true);
    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: targetEmail, password: targetPassword }),
      });
      const data = await res.json();
      if (!res.ok) {
        setLoginError(data.error || "Login failed.");
      } else {
        setUser(data.user);
      }
    } catch {
      setLoginError("Network error. Please try again.");
    } finally {
      setLoginSubmitting(false);
    }
  }

  async function handleLogout() {
    try {
      await fetch("/api/auth/logout", { method: "POST" });
    } catch {}
    setUser(null);
    setMessages([]);
  }

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
          content: error instanceof Error ? error.message : "Something went wrong.",
          error: true,
        },
      ]);
    } finally {
      setPending(false);
    }
  }

  function handleKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      void sendMessage(draft);
    }
  }

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void sendMessage(draft);
  }

  if (authLoading) {
    return (
      <div className="auth-container">
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 14 }}>
          <div className="brand-mark" style={{ width: 44, height: 44, fontSize: 22 }}>it</div>
          <span className="send-spinner" style={{ width: 22, height: 22, borderTopColor: "#2e9b77" }} />
          <p style={{ color: "#7f8b84", fontSize: 12 }}>Loading workspace...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="auth-container">
        <div className="auth-card">
          <div className="auth-brand">
            <div className="brand-mark">it</div>
            <div className="brand-name">helpdesk<span>copilot</span></div>
          </div>
          <h2>Employee Sign In</h2>
          <p className="auth-subtitle">Sign in to your XYZ workspace to access IT support</p>

          {loginError && <div className="auth-error">{loginError}</div>}

          <div className="demo-section">
            <p className="demo-label">Demo Profiles (One-Click Sign In)</p>
            <div className="demo-grid">
              <button
                type="button"
                className="demo-btn"
                onClick={() => void handleLogin("simran@xyz.example", "password123")}
                disabled={loginSubmitting}
              >
                <div className="demo-avatar">S</div>
                <div className="demo-info">
                  <strong>Simran Dangol</strong>
                  <small>Employee · Engineering</small>
                </div>
                <span className="demo-arrow">→</span>
              </button>
              <button
                type="button"
                className="demo-btn"
                onClick={() => void handleLogin("alex@xyz.example", "password123")}
                disabled={loginSubmitting}
              >
                <div className="demo-avatar">A</div>
                <div className="demo-info">
                  <strong>Alex Chen</strong>
                  <small>Staff Engineer · Platform Infrastructure</small>
                </div>
                <span className="demo-arrow">→</span>
              </button>
              <button
                type="button"
                className="demo-btn"
                onClick={() => void handleLogin("admin@xyz.example", "admin123")}
                disabled={loginSubmitting}
              >
                <div className="demo-avatar">J</div>
                <div className="demo-info">
                  <strong>Jordan Lee</strong>
                  <small>IT Administrator · Corporate Security</small>
                </div>
                <span className="demo-arrow">→</span>
              </button>
            </div>
          </div>

          <div className="auth-divider">or use corporate email</div>

          <form onSubmit={(e) => { e.preventDefault(); void handleLogin(); }} className="auth-form">
            <div className="input-group">
              <label htmlFor="auth-email">Corporate Email</label>
              <input
                id="auth-email"
                type="email"
                placeholder="username@xyz.example"
                value={loginEmail}
                onChange={(e) => setLoginEmail(e.target.value)}
                required
              />
            </div>
            <div className="input-group">
              <label htmlFor="auth-password">Password</label>
              <input
                id="auth-password"
                type="password"
                placeholder="••••••••"
                value={loginPassword}
                onChange={(e) => setLoginPassword(e.target.value)}
                required
              />
            </div>
            <button type="submit" className="auth-submit" disabled={loginSubmitting}>
              {loginSubmitting ? "Authenticating..." : "Sign In to Copilot"}
            </button>
          </form>

          <div className="auth-footer">
            <span>◇</span> Protected by XYZ Zero-Trust SSO & MFA
          </div>
        </div>
      </div>
    );
  }

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">it</div>
          <div className="brand-name">helpdesk<span>copilot</span></div>
        </div>

        <button
          className="new-chat"
          onClick={() => setMessages([])}
          disabled={pending}
        >
          <span>+</span> New conversation
        </button>

        <div className="sidebar-section">
          <p className="section-label">YOUR WORKSPACE</p>
          <div className="workspace-card">
            <div className="workspace-icon">A</div>
            <div>
              <strong>XYZ</strong>
              <small>IT Support</small>
            </div>
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
            <div className="avatar user-avatar">{user.avatar}</div>
            <span><strong>{user.name}</strong><small>{user.role} · {user.department}</small></span>
            <button className="logout-btn" onClick={() => void handleLogout()} title="Sign out">
              Sign out
            </button>
          </div>
        </div>
      </aside>

      <section className="main-panel">
        <header className="topbar">
          <div className="breadcrumb"><span>Workspace</span><b>/</b><strong>IT Support</strong></div>
          <div className="topbar-right">
            <span className="secure-label"><span>◇</span> {user.email}</span>
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
              <p className="eyebrow"><span className="status-dot" /> WELCOME, {user.name.toUpperCase().split(" ")[0]}</p>
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
                    {message.role === "assistant" ? "✳" : user.avatar}
                  </div>
                  <div className="message-content">
                    <div className="message-heading">
                      <strong>{message.role === "assistant" ? "Support Copilot" : user.name}</strong>
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
                      {message.role === "assistant" && !message.error ? (
                        <MarkdownRenderer content={message.content} />
                      ) : (
                        message.content
                      )}
                    </div>
                    {message.role === "assistant" && !message.error && (
                      <div className="message-meta">
                        {showSources && message.sources && message.sources.length > 0 && (
                          <div className="source-chips">
                            <span className="sources-label">Sources:</span>
                            {message.sources.map((src, idx) => {
                              const isUrl = src.startsWith("http://") || src.startsWith("https://");
                              if (isUrl) {
                                let label = src;
                                try {
                                  label = new URL(src).hostname.replace(/^www\./, "");
                                } catch {}
                                return (
                                  <a
                                    key={idx}
                                    href={src}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="source-chip source-chip-link"
                                  >
                                    <span className="source-chip-icon">🌐</span> {label}
                                  </a>
                                );
                              }
                              return (
                                <span key={idx} className="source-chip">
                                  <span className="source-chip-icon">📄</span> {src}
                                </span>
                              );
                            })}
                          </div>
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
                          <a className="helpdesk-link" href="mailto:helpdesk@xyz.example">
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
