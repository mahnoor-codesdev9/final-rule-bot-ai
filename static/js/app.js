const state = {
    mode: localStorage.getItem("rulebot-mode") || "rule",
    provider: localStorage.getItem("rulebot-provider") || "",
    voiceOutput: localStorage.getItem("rulebot-voice-output") === "true",
    compact: localStorage.getItem("rulebot-compact") === "true",
    messageWidth: localStorage.getItem("rulebot-message-width") || "76",
    settings: null,
};

const elements = {
    messages: document.getElementById("messages"),
    input: document.getElementById("message"),
    send: document.getElementById("send"),
    form: document.getElementById("chat-form"),
    newChat: document.getElementById("new-chat"),
    search: document.getElementById("search"),
    total: document.getElementById("total"),
    user: document.getElementById("user"),
    bot: document.getElementById("bot"),
    aiCount: document.getElementById("ai-count"),
    uptime: document.getElementById("uptime"),
    aiStatus: document.getElementById("ai-status"),
    provider: document.getElementById("provider"),
    providerStatus: document.getElementById("provider-status"),
    exportTxt: document.getElementById("export-txt"),
    exportMd: document.getElementById("export-md"),
    exportPdf: document.getElementById("export-pdf"),
    importChat: document.getElementById("import-chat"),
    importFile: document.getElementById("import-file"),
    attachButton: document.getElementById("attach-button"),
    clearChat: document.getElementById("clear-chat"),
    confirmDialog: document.getElementById("confirm-dialog"),
    confirmClose: document.getElementById("confirm-close"),
    cancelClear: document.getElementById("cancel-clear"),
    confirmClear: document.getElementById("confirm-clear"),
    voiceInput: document.getElementById("voice-input"),
    voiceToggle: document.getElementById("voice-toggle"),
    compactToggle: document.getElementById("compact-toggle"),
    widthRange: document.getElementById("width-range"),
    settingsPanel: document.getElementById("settings-panel"),
    settingsToggle: document.getElementById("settings-toggle"),
    settingsClose: document.getElementById("settings-close"),
    shortcutsToggle: document.getElementById("shortcuts-toggle"),
    shortcutsDialog: document.getElementById("shortcuts-dialog"),
    shortcutsClose: document.getElementById("shortcuts-close"),
    toastContainer: document.getElementById("toast-container"),
};

function formatSeconds(seconds) {
    if (seconds < 60) {
        return `${seconds}s`;
    }

    if (seconds < 3600) {
        return `${Math.floor(seconds / 60)}m`;
    }

    return `${Math.floor(seconds / 3600)}h`;
}

function timeLabel(timestamp) {
    const date = timestamp ? new Date(timestamp) : new Date();

    if (Number.isNaN(date.getTime())) {
        return new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
        });
    }

    return date.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
    });
}

function escapeHtml(value) {
    return value
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function highlightCode(code) {
    const escaped = escapeHtml(code);
    const keywords = [
        "async",
        "await",
        "class",
        "def",
        "return",
        "import",
        "from",
        "const",
        "let",
        "function",
        "if",
        "else",
        "for",
        "while",
        "try",
        "except",
    ];
    const pattern = new RegExp(`\\b(${keywords.join("|")})\\b`, "g");

    return escaped.replace(pattern, "<mark>$1</mark>");
}

function renderMarkdown(text) {
    const blocks = [];
    let html = escapeHtml(text).replace(
        /```([\s\S]*?)```/g,
        function (_match, code) {
            const index = blocks.length;
            blocks.push(`<pre><code>${highlightCode(code.trim())}</code></pre>`);
            return `@@CODE_BLOCK_${index}@@`;
        },
    );

    html = html
        .replace(/`([^`]+)`/g, "<code>$1</code>")
        .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
        .replace(/\*([^*]+)\*/g, "<em>$1</em>")
        .replace(/\n/g, "<br>");

    blocks.forEach(function (block, index) {
        html = html.replace(`@@CODE_BLOCK_${index}@@`, block);
    });

    return html;
}

function scrollBottom() {
    elements.messages.scrollTop = elements.messages.scrollHeight;
}

function avatar(type) {
    return type === "user" ? "You" : "AI";
}

function createMessage(item) {
    const type = item.sender === "user" ? "user" : "bot";
    const text = item.message || "";
    const box = document.createElement("article");
    box.className = `message ${type}`;
    box.dataset.mode = item.mode || "rule";

    const header = document.createElement("div");
    header.className = "message-header";

    const identity = document.createElement("span");
    identity.className = "avatar";
    identity.textContent = avatar(type);

    const meta = document.createElement("small");
    const provider = item.provider ? ` ${item.provider}` : "";
    meta.textContent = `${timeLabel(item.timestamp)} ${item.mode || "rule"}${provider}`;

    const content = document.createElement("div");
    content.className = "message-content";
    content.innerHTML = renderMarkdown(text);

    header.append(identity, meta);
    box.append(header, content);

    if (type === "bot") {
        const copy = document.createElement("button");
        copy.className = "copy-btn";
        copy.type = "button";
        copy.textContent = "Copy";
        copy.addEventListener("click", async function () {
            await navigator.clipboard.writeText(text);
            copy.textContent = "Copied";
            setTimeout(function () {
                copy.textContent = "Copy";
            }, 1000);
        });
        box.appendChild(copy);
    }

    elements.messages.appendChild(box);
    // Run syntax highlighting if Prism is loaded.
    if (window.Prism && typeof Prism.highlightAll === "function") {
        Prism.highlightAll();
    }

    scrollBottom();
}

function showWelcome() {
    createMessage({
        sender: "bot",
        message: "Hello. I am RuleBot AI, ready for rules-first answers with optional AI fallback.",
        mode: "rule",
    });
}

function showTyping() {
    const typing = document.createElement("div");
    typing.id = "typing";
    typing.className = "typing";
    typing.setAttribute("aria-label", "RuleBot is responding");

    for (let index = 0; index < 3; index += 1) {
        typing.appendChild(document.createElement("span"));
    }

    elements.messages.appendChild(typing);
    scrollBottom();
}

function hideTyping() {
    const typing = document.getElementById("typing");

    if (typing) {
        typing.remove();
    }
}

function showToast(message, type = "success") {
    if (!elements.toastContainer) {
        return;
    }

    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    elements.toastContainer.appendChild(toast);

    setTimeout(function () {
        toast.classList.add("toast-visible");
    }, 10);

    setTimeout(function () {
        toast.classList.remove("toast-visible");
        setTimeout(function () {
            toast.remove();
        }, 220);
    }, 4200);
}

async function api(path, options) {
    const response = await fetch(path, options);

    if (!response.ok) {
        const data = await response.json().catch(function () {
            return {};
        });
        throw new Error(data.detail || "Request failed.");
    }

    return response.json();
}

async function loadSettings() {
    state.settings = await api("/settings");
    elements.aiStatus.textContent = state.settings.ai_enabled ? "AI ready" : "Rule fallback";
    elements.providerStatus.textContent = Object.entries(state.settings.providers)
        .map(function ([name, enabled]) {
            return `${name}: ${enabled ? "ready" : "not configured"}`;
        })
        .join(" | ");
    elements.input.maxLength = state.settings.max_message_length;
}

async function loadStats() {
    const data = await api("/stats");
    elements.total.textContent = data.total_messages;
    elements.user.textContent = data.user_messages;
    elements.bot.textContent = data.bot_messages;
    elements.aiCount.textContent = data.ai_responses;
    elements.uptime.textContent = formatSeconds(data.session_seconds || 0);
}

async function loadHistory() {
    const data = await api("/history");
    elements.messages.textContent = "";

    if (data.history.length === 0) {
        showWelcome();
        return;
    }

    data.history.forEach(createMessage);
}

async function sendMessage() {
    const text = elements.input.value.trim();

    if (!text) {
        return;
    }

    createMessage({
        sender: "user",
        message: text,
        mode: state.mode,
        provider: state.provider,
    });

    elements.input.value = "";
    autoResizeInput();
    elements.send.disabled = true;
    elements.input.disabled = true;
    showTyping();

    try {
        const data = await api("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                message: text,
                mode: state.mode,
                provider: state.provider || null,
                voice_output: state.voiceOutput,
            }),
        });

        hideTyping();
        createMessage({
            sender: "bot",
            message: data.response,
            mode: data.mode,
            provider: data.provider,
        });

        if (state.voiceOutput) {
            speak(data.response);
        }

        await loadStats();
    } catch (error) {
        hideTyping();
        createMessage({
            sender: "bot",
            message: error.message || "Unable to connect to the server.",
            mode: "rule",
        });
    } finally {
        elements.send.disabled = false;
        elements.input.disabled = false;
        elements.input.focus();
    }
}

async function downloadHistory(format) {
    const data = await api("/history");
    const history = data.history;
    const content = history
        .map(function (item) {
            return `${item.sender.toUpperCase()}: ${item.message}`;
        })
        .join("\n\n");
    const blob = new Blob([content], {
        type: "text/plain",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "rulebot-chat.txt";
    link.click();
    URL.revokeObjectURL(url);
    showToast("Chat exported as TXT.");
}

async function exportMarkdown() {
    const data = await api("/history");
    const history = data.history;
    const content = history
        .map(function (item) {
            const role = item.sender === "user" ? "**User**" : "**RuleBot**";
            return `${role}: ${item.message}`;
        })
        .join("\n\n");
    const blob = new Blob([content], {
        type: "text/markdown",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "rulebot-chat.md";
    link.click();
    URL.revokeObjectURL(url);
    showToast("Chat exported as Markdown.");
}

async function exportPdf() {
    const data = await api("/history");
    const printWindow = window.open("", "_blank", "width=900,height=700");

    if (!printWindow) {
        showToast("Allow popups to export PDF.", "error");
        return;
    }

    const rows = data.history
        .map(function (item) {
            return `<p><strong>${escapeHtml(item.sender)}:</strong> ${escapeHtml(item.message)}</p>`;
        })
        .join("");

    printWindow.document.write(`
        <html>
            <head>
                <title>RuleBot AI Chat Export</title>
                <style>
                    body { font-family: Arial, sans-serif; padding: 32px; }
                    h1 { margin-bottom: 24px; }
                    p { line-height: 1.6; border-bottom: 1px solid #ddd; padding-bottom: 10px; }
                </style>
            </head>
            <body>
                <h1>RuleBot AI Chat Export</h1>
                ${rows || "<p>No chat history.</p>"}
            </body>
        </html>
    `);
    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
    showToast("Opened chat export in print preview.");
}

function speak(text) {
    if (!("speechSynthesis" in window)) {
        return;
    }

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1;
    window.speechSynthesis.speak(utterance);
}

function startVoiceInput() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        createMessage({
            sender: "bot",
            message: "Voice input is not supported in this browser.",
            mode: "rule",
        });
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    elements.voiceInput.classList.add("is-listening");
    recognition.start();

    recognition.onresult = function (event) {
        elements.input.value = event.results[0][0].transcript;
        autoResizeInput();
        elements.input.focus();
    };

    recognition.onend = function () {
        elements.voiceInput.classList.remove("is-listening");
    };
}

function autoResizeInput() {
    elements.input.style.height = "auto";
    elements.input.style.height = `${Math.min(elements.input.scrollHeight, 180)}px`;
}

function applyPreferences() {
    document.body.classList.toggle("compact", state.compact);
    document.documentElement.style.setProperty(
        "--message-width",
        `${state.messageWidth}%`,
    );
    elements.voiceToggle.checked = state.voiceOutput;
    elements.compactToggle.checked = state.compact;
    elements.widthRange.value = state.messageWidth;
    elements.provider.value = state.provider;

    document.querySelectorAll(".segment").forEach(function (button) {
        button.classList.toggle("is-active", button.dataset.mode === state.mode);
    });
}

function showConfirmDialog() {
    if (elements.confirmDialog && typeof elements.confirmDialog.showModal === "function") {
        elements.confirmDialog.showModal();
    }
}

function hideConfirmDialog() {
    if (elements.confirmDialog && typeof elements.confirmDialog.close === "function") {
        elements.confirmDialog.close();
    }
}

function importChatFile(file) {
    const reader = new FileReader();
    reader.onload = function () {
        try {
            const payload = JSON.parse(reader.result);

            if (Array.isArray(payload.history)) {
                elements.messages.textContent = "";
                payload.history.forEach(function (item) {
                    createMessage(item);
                });
                showToast("Chat history imported locally.");
                return;
            }

            if (Array.isArray(payload)) {
                elements.messages.textContent = "";
                payload.forEach(function (item) {
                    createMessage(item);
                });
                showToast("Chat history imported locally.");
                return;
            }

            throw new Error("Invalid chat file format.");
        } catch (error) {
            showToast("Unable to import chat file.", "error");
        }
    };

    reader.readAsText(file);
}

function setMode(mode) {
    state.mode = mode;
    localStorage.setItem("rulebot-mode", mode);
    applyPreferences();
}

function toggleSettings() {
    elements.settingsPanel.classList.toggle("is-open");
}

function filterMessages() {
    const value = elements.search.value.toLowerCase();

    document.querySelectorAll(".message").forEach(function (item) {
        item.classList.toggle(
            "is-hidden",
            !item.textContent.toLowerCase().includes(value),
        );
    });
}

elements.form.addEventListener("submit", function (event) {
    event.preventDefault();
    sendMessage();
});

elements.input.addEventListener("input", autoResizeInput);
elements.input.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

elements.newChat.addEventListener("click", async function () {
    await api("/history", {
        method: "DELETE",
    });
    elements.messages.textContent = "";
    showWelcome();
    await loadStats();
    elements.input.focus();
});

document.querySelectorAll(".segment").forEach(function (button) {
    button.addEventListener("click", function () {
        setMode(button.dataset.mode);
    });
});

elements.provider.addEventListener("change", function () {
    state.provider = elements.provider.value;
    localStorage.setItem("rulebot-provider", state.provider);
});

elements.exportTxt.addEventListener("click", function () {
    downloadHistory("txt");
});

elements.exportMd.addEventListener("click", function () {
    exportMarkdown();
});

elements.exportPdf.addEventListener("click", exportPdf);
elements.importChat.addEventListener("click", function () {
    if (elements.importFile) {
        elements.importFile.click();
    }
});
elements.importFile.addEventListener("change", function (event) {
    const file = event.target.files?.[0];

    if (file) {
        importChatFile(file);
    }
});
elements.attachButton.addEventListener("click", function () {
    if (elements.importFile) {
        elements.importFile.click();
    }
});
elements.clearChat.addEventListener("click", showConfirmDialog);
elements.confirmClose.addEventListener("click", hideConfirmDialog);
elements.cancelClear.addEventListener("click", hideConfirmDialog);
elements.confirmClear.addEventListener("click", async function () {
    await api("/history", {
        method: "DELETE",
    });
    elements.messages.textContent = "";
    showWelcome();
    await loadStats();
    hideConfirmDialog();
    showToast("Conversation cleared.");
});
elements.search.addEventListener("input", filterMessages);
elements.voiceInput.addEventListener("click", startVoiceInput);
elements.voiceToggle.addEventListener("change", function () {
    state.voiceOutput = elements.voiceToggle.checked;
    localStorage.setItem("rulebot-voice-output", String(state.voiceOutput));
    applyPreferences();
});
elements.compactToggle.addEventListener("change", function () {
    state.compact = elements.compactToggle.checked;
    localStorage.setItem("rulebot-compact", String(state.compact));
    applyPreferences();
});
elements.widthRange.addEventListener("input", function () {
    state.messageWidth = elements.widthRange.value;
    localStorage.setItem("rulebot-message-width", state.messageWidth);
    applyPreferences();
});
elements.settingsToggle.addEventListener("click", toggleSettings);
elements.settingsClose.addEventListener("click", toggleSettings);
elements.shortcutsToggle.addEventListener("click", function () {
    if (elements.shortcutsDialog && typeof elements.shortcutsDialog.showModal === "function") {
        elements.shortcutsDialog.showModal();
    }
});
elements.shortcutsClose.addEventListener("click", function () {
    if (elements.shortcutsDialog && typeof elements.shortcutsDialog.close === "function") {
        elements.shortcutsDialog.close();
    }
});

document.addEventListener("keydown", function (event) {
    if (event.key === "/" && document.activeElement !== elements.input) {
        event.preventDefault();
        elements.input.focus();
    }

    if (event.ctrlKey && event.key.toLowerCase() === "k") {
        event.preventDefault();
        elements.newChat.click();
    }

    if (event.ctrlKey && event.key.toLowerCase() === "j") {
        event.preventDefault();
        toggleTheme();
    }
});

window.addEventListener("load", async function () {
    applyPreferences();
    await loadSettings();
    await loadHistory();
    await loadStats();
    autoResizeInput();
    elements.input.focus();
});
