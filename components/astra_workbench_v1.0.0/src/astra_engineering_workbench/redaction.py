"""Conservative secret, personal path and contact redaction."""

from __future__ import annotations

import re

PATTERNS = (
    (re.compile(r"(?i)\b(?:api[_-]?key|token|password|secret)\s*[:=]\s*\S+"), "[REDACTED_SECRET]"),
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "[REDACTED_EMAIL]"),
    (re.compile(r"(?i)\bC:\\Users\\[^\\\s]+"), r"C:\\Users\\[REDACTED_USER]"),
    (re.compile(r"\b(?:\+?\d[\d -]{7,}\d)\b"), "[REDACTED_PHONE]"),
)


def redact_text(text: str) -> tuple[str, tuple[str, ...]]:
    applied: list[str] = []
    result = text
    for pattern, replacement in PATTERNS:
        updated, count = pattern.subn(replacement, result)
        if count:
            applied.append(replacement)
        result = updated
    return result, tuple(applied)
