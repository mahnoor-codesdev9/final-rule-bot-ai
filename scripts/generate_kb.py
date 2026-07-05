"""Generate expanded chatbot knowledge files.

Run this script to populate `chatbot/knowledge/responses_extra.json` with
many templated Q/A pairs. This is a helper to bootstrap a larger KB — the
project's loader supports merging these files automatically.
"""
from __future__ import annotations

import json
from pathlib import Path


def main():
    topics = [
        "python",
        "java",
        "javascript",
        "docker",
        "kubernetes",
        "git",
        "testing",
        "ci/cd",
        "rest api",
        "fastapi",
        "uvicorn",
        "sql",
        "postgresql",
        "sqlite",
        "linux",
        "windows",
        "macos",
        "regex",
        "asyncio",
        "http",
        "json",
        "xml",
        "html",
        "css",
        "react",
        "vue",
        "svelte",
        "docker-compose",
        "aws",
        "gcp",
        "azure",
        "security",
        "oauth",
        "jwt",
        "encryption",
        "performance",
        "profiling",
        "logging",
        "monitoring",
        "prometheus",
        "grafana",
        "error handling",
        "exceptions",
        "data structures",
        "algorithms",
        "threads",
        "processes",
        "concurrency",
        "multiprocessing",
        "deployment",
        "dockerfile",
        "package management",
        "pip",
        "poetry",
    ]

    verbs = [
        "what is",
        "how to use",
        "how to install",
        "tips for",
        "best practices for",
        "why use",
        "how does",
        "examples of",
    ]

    responses = {}

    for topic in topics:
        for verb in verbs:
            key = f"{verb} {topic}"
            resp = f"{topic.capitalize()} — brief explanation for: {verb} {topic}. For details, consult official docs or ask a specific question."
            responses[key] = resp

    out = Path(__file__).resolve().parent.parent / "chatbot" / "knowledge" / "responses_extra.json"
    out.parent.mkdir(parents=True, exist_ok=True)

    with out.open("w", encoding="utf-8") as fh:
        json.dump(responses, fh, indent=2, ensure_ascii=False)

    print(f"Generated {len(responses)} response entries -> {out}")


if __name__ == "__main__":
    main()
