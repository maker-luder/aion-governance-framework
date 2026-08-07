from __future__ import annotations

from collections.abc import Iterable

from .models import ContinuityLayer, DriftDecision, DriftResult


def _normal(text: str) -> str:
    return " ".join(text.casefold().split())


def check_interpretation_drift(
    text: str,
    required_terms: Iterable[str],
    prohibited_claims: Iterable[str],
) -> DriftResult:
    normalized = _normal(text)
    missing = tuple(term for term in required_terms if _normal(term) not in normalized)
    found_prohibited = tuple(claim for claim in prohibited_claims if _normal(claim) in normalized)
    if found_prohibited:
        decision = DriftDecision.FAIL
    elif missing:
        decision = DriftDecision.HOLD
    else:
        decision = DriftDecision.PASS
    return DriftResult(decision, missing, found_prohibited)


def continuity_status(observed_layers: Iterable[ContinuityLayer]) -> dict[str, str]:
    observed = {layer.value for layer in observed_layers}
    return {
        "observed_layers": ",".join(sorted(observed)),
        "identity_continuity_conclusion": "NOT_ESTABLISHED",
        "interpretive_continuity_conclusion": "NOT_ESTABLISHED",
        "relational_continuity_conclusion": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
    }
