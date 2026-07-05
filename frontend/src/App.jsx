import React, { useEffect, useRef, useState } from "react";
import { apiGet, apiPost } from "./api";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [typing, setTyping] = useState(false);
  const [settings, setSettings] = useState(null);
  const [mode, setMode] = useState(localStorage.getItem("rulebot-mode") || "rule");
  const [provider, setProvider] = useState(localStorage.getItem("rulebot-provider") || "");
  const messagesRef = useRef(null);

  useEffect(() => {
    (async function load() {
      try {
        const s = await apiGet("/settings");
        setSettings(s);
        const history = await apiGet("/history");
        if (history.history && history.history.length) {
          setMessages(history.history.map((h, i) => ({ ...h, id: i + 1 })));
        } else {
          setMessages([{ id: 1, sender: "bot", message: "Hello. I am RuleBot AI, ready." }]);
        }
      } catch (err) {
        console.error(err);
      }
    })();
  }, []);

  useEffect(() => {
    if (messagesRef.current) {
      messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
    }
  }, [messages, typing]);

  async function handleSend(e) {
    if (e) e.preventDefault();
    const text = input.trim();
    if (!text) return;
    const user = { id: Date.now(), sender: "user", message: text, mode, provider };
    setMessages((m) => [...m, user]);
    setInput("");
    setTyping(true);

    try {
      const data = await apiPost("/chat", { message: text, mode, provider: provider || null });
      setTyping(false);
      const bot = { id: Date.now() + 1, sender: "bot", message: data.response, mode: data.mode, provider: data.provider };
      setMessages((m) => [...m, bot]);
    } catch (err) {
      setTyping(false);
      setMessages((m) => [...m, { id: Date.now() + 2, sender: "bot", message: err.message || "Request failed." }]);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  function setModeLocal(m) {
    setMode(m);
    localStorage.setItem("rulebot-mode", m);
  }

  return (
    <div className="rb-root">
      <aside className="rb-sidebar">
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <img src="/static/icons/logo.svg" alt="RuleBot" style={{ width: 40, height: 40 }} />
          <div>
            <div style={{ fontWeight: 800 }}>RuleBot AI</div>
            <div style={{ color: "#9aa6bd", fontSize: 12 }}>Hybrid assistant</div>
          </div>
        </div>
        <div style={{ marginTop: 18 }}>
          <div style={{ marginBottom: 8, fontSize: 12, fontWeight: 700 }}>Mode</div>
          <div style={{ display: "flex", gap: 8 }}>
            <button onClick={() => setModeLocal("rule")} className={mode === "rule" ? "segment is-active" : "segment"}>Rule</button>
            <button onClick={() => setModeLocal("auto")} className={mode === "auto" ? "segment is-active" : "segment"}>Auto</button>
            <button onClick={() => setModeLocal("ai")} className={mode === "ai" ? "segment is-active" : "segment"}>AI</button>
          </div>
        </div>
      </aside>

      <main className="rb-chat">
        <header className="rb-header">
          <div>
            <div style={{ fontSize: 18, fontWeight: 900 }}>RuleBot AI</div>
            <div style={{ color: "#9aa6bd", fontSize: 13 }}>A polished hybrid assistant</div>
          </div>
          <div style={{ display: "flex", gap: 8 }}>
            <button className="icon-button"><img src="/static/icons/theme.svg" alt="Theme" /></button>
          </div>
        </header>

        <section ref={messagesRef} className="rb-messages">
          {messages.map((m) => (
            <article key={m.id} className={`rb-message ${m.sender === "user" ? "user" : "bot"}`}>
              <div className="rb-content">{m.message}</div>
            </article>
          ))}
          {typing && (
            <div className="rb-message bot">
              <div className="rb-content">RuleBot is typing...</div>
            </div>
          )}
        </section>

        <form className="rb-composer" onSubmit={handleSend}>
          <textarea
            aria-label="Type your message"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            style={{ resize: "none", minHeight: 54 }}
          />
          <div style={{ display: "flex", gap: 8 }}>
            <button type="button" className="button button-secondary"><img src="/static/icons/mic.svg" alt="Voice"/></button>
            <button type="button" className="button button-secondary"><img src="/static/icons/attach.svg" alt="Attach"/></button>
            <button id="send" className="button button-primary" type="submit"><img src="/static/icons/send.svg" alt="Send"/></button>
          </div>
        </form>
      </main>
    </div>
  );
}
