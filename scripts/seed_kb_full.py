"""Seed the chatbot knowledge directory with expanded intents, synonyms, and responses.

This script generates multiple JSON files under `chatbot/knowledge/` to expand
coverage across many technical and career-related topics. It is intended as a
bootstrap tool — the repository's `KnowledgeLoader` merges files matching the
patterns `responses_*.json`, `intents_*.json`, `synonyms_*.json`.

Run:
    python scripts/seed_kb_full.py

"""
from __future__ import annotations

import json
from pathlib import Path
from random import choice, randint

CATEGORIES = [
    "greetings",
    "general conversation",
    "resume writing",
    "cv building",
    "cover letters",
    "hr interview questions",
    "technical interview questions",
    "career guidance",
    "linkedin optimization",
    "python",
    "java",
    "c",
    "c++",
    "javascript",
    "typescript",
    "html",
    "css",
    "sql",
    "git",
    "github",
    "fastapi",
    "flask",
    "django",
    "react basics",
    "docker",
    "linux",
    "rest apis",
    "json",
    "oop",
    "data structures",
    "algorithms",
    "dbms",
    "operating systems",
    "computer networks",
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "nlp",
]

VERBS = [
    "what is",
    "how to",
    "how do I",
    "tips for",
    "best practices for",
    "examples of",
    "why use",
    "installation",
    "tutorial",
    "common mistakes in",
]

OUT_DIR = Path(__file__).resolve().parent.parent / "chatbot" / "knowledge"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_responses():
    responses = {}

    for cat in CATEGORIES:
        topic = cat
        for verb in VERBS:
            key = f"{verb} {topic}"
            response = (
                f"{topic.capitalize()} — {verb} {topic}: concise explanation and guidance. "
                f"Ask for a concrete example if you'd like more detail."
            )
            responses[key] = response

        # Add several question variations to increase count
        for i in range(3):
            key = f"{topic} {i}"
            responses[key] = f"Short note about {topic} (variation {i})."

    # Add generic conversational responses
    for g in ["hello", "hi", "hey", "thanks", "bye"]:
        responses[g] = {
            "hello": "Hello! How can I help you today?",
            "hi": "Hi! Nice to meet you.",
            "hey": "Hey! Hope you're having a wonderful day.",
            "thanks": "You're welcome!",
            "bye": "Goodbye! Have a great day.",
        }[g]

    out = OUT_DIR / "responses_expanded.json"
    with out.open("w", encoding="utf-8") as fh:
        json.dump(responses, fh, indent=2, ensure_ascii=False)

    print(f"Wrote {len(responses)} responses to {out}")


def generate_intents():
    intents = {}

    for cat in CATEGORIES:
        key = cat.lower().strip()
        keywords = []
        # generate keyword variations
        keywords.append(key)
        keywords.append(key.replace(" ", "-"))
        keywords.append(key.replace(" ", " "))
        if " " in key:
            keywords.append(key.split(" ")[0])
        # add common short forms
        keywords.append(key.split(" ")[-1])
        # add numbered variants
        for i in range(3):
            keywords.append(f"{key} {i}")

        # uniqueness
        intents[key] = list(dict.fromkeys([k for k in keywords if k]))

    out = OUT_DIR / "intents_expanded.json"
    with out.open("w", encoding="utf-8") as fh:
        json.dump(intents, fh, indent=2, ensure_ascii=False)

    print(f"Wrote {len(intents)} intents to {out}")


def generate_synonyms():
    synonyms = {}

    for cat in CATEGORIES:
        key = cat.split()[0]
        syns = [key]
        syns.append(key + "s")
        syns.append("learn " + key)
        syns.append("how to " + key)
        synonyms[key] = list(dict.fromkeys(syns))

    out = OUT_DIR / "synonyms_expanded.json"
    with out.open("w", encoding="utf-8") as fh:
        json.dump(synonyms, fh, indent=2, ensure_ascii=False)

    print(f"Wrote {len(synonyms)} synonym groups to {out}")


if __name__ == "__main__":
    generate_responses()
    generate_intents()
    generate_synonyms()
