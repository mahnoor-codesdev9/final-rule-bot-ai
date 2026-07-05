"""Enhanced response matcher with fuzzy scoring, synonyms and typo correction.

This matcher tries to provide a best-effort rule-based response while
providing confidence scores and candidate suggestions. It prefers exact
matches, then synonym/intent matches, then fuzzy matches. Typo correction
and token-aware matching use `rapidfuzz` when available with a difflib
fallback.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

try:
    from rapidfuzz import fuzz, process
except Exception:  # pragma: no cover - optional dependency
    fuzz = None
    process = None

from difflib import SequenceMatcher, get_close_matches

from chatbot.knowledge_loader import KnowledgeLoader


@dataclass
class MatchResult:
    response: str | None
    intent: str | None
    confidence: float
    candidates: list[tuple[str, float]]


class ResponseMatcher:
    """Match user input against the knowledge base with confidence scoring."""

    HIGH_CONFIDENCE = 0.86
    MEDIUM_CONFIDENCE = 0.7
    LOW_CONFIDENCE = 0.6

    def __init__(self, loader: KnowledgeLoader | None = None) -> None:
        knowledge = loader or KnowledgeLoader()
        self.responses = knowledge.responses
        self.synonyms = knowledge.synonyms
        self.intents = knowledge.intents
        # Build candidate phrase list for fast iteration
        self._phrases = list(self.responses.keys())

    def match(self, user_input: str) -> MatchResult:
        query = self._normalize(user_input)

        if not query:
            return MatchResult(response=None, intent=None, confidence=0.0, candidates=[])

        # Exact normalized match
        if query in self.responses:
            return MatchResult(self.responses[query], None, 1.0, [(query, 1.0)])

        # Synonym / intent group match
        grp = self._match_groups(query, self.synonyms)
        if grp:
            return MatchResult(grp, None, 0.98, [(grp, 0.98)])

        grp = self._match_groups(query, self.intents)
        if grp:
            return MatchResult(grp, None, 0.95, [(grp, 0.95)])

        # Partial phrase containment
        partial = self._partial_match(query)
        if partial:
            return MatchResult(partial, None, 0.92, [(partial, 0.92)])

        # Fuzzy matching with optional rapidfuzz
        candidates = self._fuzzy_candidates(query, top_n=5)

        if not candidates:
            # Typo correction using difflib as last resort
            corrected = self._typo_correction(query)
            if corrected:
                return MatchResult(self.responses[corrected], None, 0.8, [(corrected, 0.8)])

            return MatchResult(response=None, intent=None, confidence=0.0, candidates=[])

        best, best_score = candidates[0]

        if best_score >= self.HIGH_CONFIDENCE:
            return MatchResult(self.responses[best], None, best_score, candidates)

        if best_score >= self.MEDIUM_CONFIDENCE:
            return MatchResult(self.responses[best], None, best_score, candidates)

        # Return candidates for suggestions when low confidence
        return MatchResult(response=None, intent=None, confidence=best_score, candidates=candidates)

    def _match_groups(self, query: str, groups: dict[str, Iterable[str]]) -> str | None:
        for group_name, keywords in groups.items():
            candidates = [group_name, *keywords]
            # Prioritize direct match of group_name if it's a response key
            if group_name in self.responses and self._contains_phrase(query, group_name):
                return self.responses[group_name]
            for keyword in keywords:
                if self._contains_phrase(query, keyword) and group_name in self.responses:
                    return self.responses[group_name]

        return None

    def _partial_match(self, query: str) -> str | None:
        for key, response in self.responses.items():
            if self._contains_phrase(query, key):
                return response
        return None

    def _fuzzy_candidates(self, query: str, top_n: int = 5) -> list[tuple[str, float]]:
        if process is not None and fuzz is not None:
            # Use rapidfuzz for token-aware scoring
            results = process.extract(query, self._phrases, scorer=fuzz.token_sort_ratio, limit=top_n)
            # rapidfuzz returns scores 0-100
            return [(item[0], item[1] / 100.0) for item in results if item[1] > 0]

        # Fallback to difflib SequenceMatcher-based scoring
        scored: list[tuple[str, float]] = []
        for phrase in self._phrases:
            score = SequenceMatcher(None, query, phrase).ratio()
            scored.append((phrase, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_n]

    def _typo_correction(self, query: str) -> str | None:
        # Use difflib to find close phrase matches by name
        candidates = get_close_matches(query, self._phrases, n=1, cutoff=0.7)
        if candidates:
            return candidates[0]
        return None

    def _contains_phrase(self, query: str, phrase: str) -> bool:
        if not phrase:
            return False
        pattern = r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"
        return re.search(pattern, query) is not None

    def _normalize(self, value: str) -> str:
        return re.sub(r"\s+", " ", value.lower().strip())

    def find_response(self, user_input: str) -> str:
        """Compatibility wrapper to return a simple response string.

        Preserves existing API used across the project and tests. If the
        enhanced matcher finds candidates but confidence is low, return a
        helpful suggestion instead of an immediate unknown response.
        """
        from chatbot.config import UNKNOWN_RESPONSE

        result = self.match(user_input)

        if result.response:
            return result.response

        if result.candidates:
            best, score = result.candidates[0]
            if score >= self.MEDIUM_CONFIDENCE:
                return self.responses.get(best, UNKNOWN_RESPONSE) # Return the best match directly

            if score >= self.LOW_CONFIDENCE:
                # For low confidence, offer a suggestion without immediately giving the answer
                if best in self.responses:
                    return f"I'm not sure I understood. Did you mean '{best}'?"

        return UNKNOWN_RESPONSE
