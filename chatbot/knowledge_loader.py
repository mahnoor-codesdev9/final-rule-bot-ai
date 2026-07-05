"""
Knowledge loader for RuleBot AI.
"""

from __future__ import annotations

from functools import cached_property
from pathlib import Path
from typing import Any
import json


class KnowledgeLoader:
    """
    Load and validate chatbot knowledge files.
    """

    def __init__(
        self,
        knowledge_dir: str | Path | None = None,
    ) -> None:
        if knowledge_dir:
            self._knowledge_dir = Path(knowledge_dir)
        else:
            self._knowledge_dir = Path(__file__).resolve().parent / "knowledge"

    def load_json(self, filename: str) -> dict[str, Any]:
        """
        Load a JSON object from the knowledge directory.
        """
        file_path = self._knowledge_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Knowledge file not found: {filename}")

        try:
            with file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"Knowledge file contains invalid JSON: {filename}"
            ) from error

        if not isinstance(data, dict):
            raise ValueError(
                f"Knowledge file must contain a JSON object: {filename}"
            )

        return data

    def _load_all_matching(self, pattern: str) -> dict[str, Any]:
        """
        Load and merge all JSON files in the knowledge directory matching a glob pattern.
        Later files override earlier ones for the same keys.
        """
        merged: dict[str, Any] = {}

        for path in sorted(self._knowledge_dir.glob(pattern)):
            try:
                with path.open("r", encoding="utf-8") as fh:
                    data = json.load(fh)
            except Exception:
                continue

            if not isinstance(data, dict):
                continue

            merged.update(data)

        return merged

    @cached_property
    def responses(self) -> dict[str, str]:
        """
        Load normalized chatbot responses.
        """
        # Support multiple response files (responses.json, responses_*.json)
        merged = self.load_json("responses.json") if (self._knowledge_dir / "responses.json").exists() else {}
        merged.update(self._load_all_matching("responses_*.json"))

        return {
            str(key).lower().strip(): str(value).strip()
            for key, value in merged.items()
            if str(key).strip() and str(value).strip()
        }

    @cached_property
    def synonyms(self) -> dict[str, list[str]]:
        """
        Load normalized synonym groups.
        """
        merged = {}

        if (self._knowledge_dir / "synonyms.json").exists():
            merged.update(self.load_json("synonyms.json"))

        merged.update(self._load_all_matching("synonyms_*.json"))

        # reuse _load_word_groups logic by processing merged dict
        groups: dict[str, list[str]] = {}
        for key, value in merged.items():
            if not isinstance(value, list):
                continue

            groups[str(key).lower().strip()] = [
                str(item).lower().strip()
                for item in value
                if str(item).strip()
            ]

        return groups

    @cached_property
    def intents(self) -> dict[str, list[str]]:
        """
        Load normalized intent groups.
        """
        merged = {}

        if (self._knowledge_dir / "intents.json").exists():
            merged.update(self.load_json("intents.json"))

        merged.update(self._load_all_matching("intents_*.json"))

        groups: dict[str, list[str]] = {}
        for key, value in merged.items():
            if not isinstance(value, list):
                continue

            groups[str(key).lower().strip()] = [
                str(item).lower().strip()
                for item in value
                if str(item).strip()
            ]

        return groups

    def _load_word_groups(self, filename: str) -> dict[str, list[str]]:
        """
        Load a mapping of group names to normalized keyword lists.
        """
        data = self.load_json(filename)
        groups: dict[str, list[str]] = {}

        for key, value in data.items():
            if not isinstance(value, list):
                continue

            groups[str(key).lower().strip()] = [
                str(item).lower().strip()
                for item in value
                if str(item).strip()
            ]

        return groups
