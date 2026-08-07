from __future__ import annotations

import re

SIMPLIFIED_MARKERS = frozenset("这为软体执预设档资讯后发里个时")
TRADITIONAL_MARKERS = frozenset("這為軟體執預設檔資訊後發裡個時")


def completion_success(text: str) -> bool:
    return bool(text.strip())


def repeated_ngram_ratio(text: str, n: int = 3) -> float:
    tokens = text.split()
    if len(tokens) < n or n <= 0:
        return 0.0
    grams = [tuple(tokens[index : index + n]) for index in range(len(tokens) - n + 1)]
    return 1.0 - (len(set(grams)) / len(grams))


def loop_detected(text: str) -> bool:
    normalized = re.sub(r"\s+", " ", text.strip())
    chunks = [chunk.strip() for chunk in re.split(r"[。！？.!?]", normalized) if chunk.strip()]
    return len(chunks) >= 3 and len(set(chunks)) <= len(chunks) / 2


def script_counts(text: str) -> dict[str, int]:
    return {
        "simplified_markers": sum(char in SIMPLIFIED_MARKERS for char in text),
        "traditional_markers": sum(char in TRADITIONAL_MARKERS for char in text),
    }


def terminology_scores(
    text: str, expected_tw: tuple[str, ...], forbidden_cn: tuple[str, ...]
) -> dict[str, float]:
    expected_hits = sum(term in text for term in expected_tw)
    forbidden_hits = sum(term in text for term in forbidden_cn)
    return {
        "taiwan_terminology_hit_rate": expected_hits / len(expected_tw) if expected_tw else 1.0,
        "mainland_substitution_rate": forbidden_hits / len(forbidden_cn) if forbidden_cn else 0.0,
    }


def constraint_scores(text: str, constraints: tuple[str, ...]) -> dict[str, float | int]:
    hits = sum(constraint.casefold() in text.casefold() for constraint in constraints)
    return {
        "constraint_count": len(constraints),
        "constraint_hits": hits,
        "instruction_following_rate": hits / len(constraints) if constraints else 1.0,
    }


def uncertainty_acknowledged(text: str) -> bool:
    markers = ("資訊不足", "無法判定", "不確定", "insufficient information", "无法判断")
    return any(marker in text for marker in markers)
