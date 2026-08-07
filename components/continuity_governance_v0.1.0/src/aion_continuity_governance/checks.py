from __future__ import annotations

from collections.abc import Iterable

from .models import (
    ContinuityDimension,
    ContinuityLayer,
    ContinuityMatrix,
    DimensionObservation,
    DriftDecision,
    DriftResult,
)


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


def continuity_matrix(
    observations: Iterable[DimensionObservation],
) -> ContinuityMatrix:
    """Preserve dimension-level evidence without collapsing it into an identity claim."""

    materialized = tuple(observations)
    dimensions = [item.dimension for item in materialized]
    if len(dimensions) != len(set(dimensions)):
        raise ValueError("continuity dimensions must be unique within one matrix")
    return ContinuityMatrix(observations=materialized)


def correction_recovery_observation(
    *,
    before_correction: DriftDecision,
    after_correction: DriftDecision,
    evidence_refs: tuple[str, ...] = (),
) -> DimensionObservation:
    """Record correction recovery as behavior, never as proof of persistent identity."""

    if after_correction is DriftDecision.PASS and before_correction is not DriftDecision.PASS:
        decision = DriftDecision.PASS
        note = "Correction was accepted and the tested invariant recovered."
    elif after_correction is DriftDecision.FAIL:
        decision = DriftDecision.FAIL
        note = "Material contradiction remained after correction."
    elif after_correction is DriftDecision.PARTIAL:
        decision = DriftDecision.PARTIAL
        note = "Correction produced incomplete recovery."
    else:
        decision = DriftDecision.HOLD
        note = "Correction recovery is not established by the available evidence."
    return DimensionObservation(
        dimension=ContinuityDimension.CORRECTION_RECOVERY,
        decision=decision,
        evidence_refs=evidence_refs,
        note=note,
    )


def continuity_status(observed_layers: Iterable[ContinuityLayer]) -> dict[str, str]:
    observed = {layer.value for layer in observed_layers}
    return {
        "observed_layers": ",".join(sorted(observed)),
        "identity_continuity_conclusion": "NOT_ESTABLISHED",
        "interpretive_continuity_conclusion": "NOT_ESTABLISHED",
        "relational_continuity_conclusion": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
    }
