from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable

from aion_causal_internal_state import AssessmentStatus, Condition, TrialObservation, assess_causal_effect


@dataclass(frozen=True, slots=True)
class CausalAudit:
    status: str
    disposition: str
    reasons: tuple[str, ...]
    study_id: str
    matched_trial_count: int = 0
    candidate_pattern_observed: bool = False
    intervention_delta: float | None = None
    ablation_delta: float | None = None
    random_control_delta: float | None = None
    replicate_consistency: float | None = None
    synthetic_fixture: bool = True
    model_execution: bool = False
    intervention_executed: bool = False
    observed_result: str = "NOT_EVALUATED"
    causal_conclusion: str = "NOT_ESTABLISHED"
    scientific_conclusion: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    identity_continuity_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    governance_effect: str = "NONE"
    deployment: bool = False

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "disposition": self.disposition,
            "reasons": list(self.reasons),
            "study_id": self.study_id,
            "matched_trial_count": self.matched_trial_count,
            "candidate_pattern_observed": self.candidate_pattern_observed,
            "intervention_delta": self.intervention_delta,
            "ablation_delta": self.ablation_delta,
            "random_control_delta": self.random_control_delta,
            "replicate_consistency": self.replicate_consistency,
            "synthetic_fixture": self.synthetic_fixture,
            "model_execution": self.model_execution,
            "intervention_executed": self.intervention_executed,
            "observed_result": self.observed_result,
            "causal_conclusion": self.causal_conclusion,
            "scientific_conclusion": self.scientific_conclusion,
            "subjectivity_conclusion": self.subjectivity_conclusion,
            "consciousness_conclusion": self.consciousness_conclusion,
            "identity_continuity_conclusion": self.identity_continuity_conclusion,
            "canonical_effect": self.canonical_effect,
            "governance_effect": self.governance_effect,
            "deployment": self.deployment,
        }


def _invalid(study_id: str, reason: str) -> CausalAudit:
    return CausalAudit("INVALID", "HOLD", (reason,), study_id)


def audit_causal_pattern(
    observations: Iterable[TrialObservation],
    *,
    study_id: str,
    preregistration_ref: str | None,
    assumption_basis: str | None,
    synthetic_fixture: bool = True,
) -> CausalAudit:
    records = tuple(observations)
    if not study_id or not study_id.strip():
        return _invalid(study_id, "STUDY_ID_MISSING")
    if not synthetic_fixture:
        return _invalid(study_id, "NON_SYNTHETIC_EXECUTION_NOT_PERMITTED")
    if preregistration_ref is None or not preregistration_ref.strip():
        return CausalAudit("UNKNOWN", "INDETERMINATE", ("PREREGISTRATION_REFERENCE_MISSING",), study_id, len({(x.pair_id, x.replicate) for x in records if isinstance(x, TrialObservation)}))
    if assumption_basis is None or not assumption_basis.strip():
        return CausalAudit("UNKNOWN", "HOLD", ("ASSUMPTION_BASIS_MISSING",), study_id, len({(x.pair_id, x.replicate) for x in records if isinstance(x, TrialObservation)}))
    if not records:
        return _invalid(study_id, "OBSERVATION_SET_EMPTY")
    seen: set[tuple[str, int, Condition]] = set()
    trials: set[tuple[str, int]] = set()
    for item in records:
        if not isinstance(item, TrialObservation):
            return _invalid(study_id, "OBSERVATION_TYPE_INVALID")
        if not isinstance(item.pair_id, str) or not item.pair_id.strip():
            return _invalid(study_id, "PAIR_ID_INVALID")
        if not isinstance(item.replicate, int) or isinstance(item.replicate, bool) or item.replicate < 1:
            return _invalid(study_id, "REPLICATE_ID_INVALID")
        if not isinstance(item.condition, Condition):
            return _invalid(study_id, "CONDITION_TYPE_INVALID")
        if not isinstance(item.score, (int, float)) or isinstance(item.score, bool) or not isfinite(item.score):
            return _invalid(study_id, "SCORE_NON_FINITE_OR_INVALID")
        key = (item.pair_id, item.replicate, item.condition)
        if key in seen:
            return _invalid(study_id, "DUPLICATE_MATCHED_CONDITION")
        seen.add(key)
        trials.add((item.pair_id, item.replicate))
    assessment = assess_causal_effect(records)
    if assessment.status is AssessmentStatus.PASS_CANDIDATE:
        return CausalAudit(
            "PASS_CANDIDATE",
            "REVIEW_ONLY",
            assessment.reasons,
            study_id,
            len(trials),
            True,
            assessment.intervention_delta,
            assessment.ablation_delta,
            assessment.random_control_delta,
            assessment.replicate_consistency,
        )
    return CausalAudit(
        assessment.status.value,
        "HOLD",
        assessment.reasons,
        study_id,
        len(trials),
        False,
        assessment.intervention_delta,
        assessment.ablation_delta,
        assessment.random_control_delta,
        assessment.replicate_consistency,
    )


@dataclass(frozen=True, slots=True)
class ProtocolSnapshot:
    study_id: str
    preregistration_ref: str
    condition_order: tuple[Condition, ...]
    min_replicates: int
    min_effect: float
    outcome_observed: bool = False


def audit_protocol_lock(before: ProtocolSnapshot, after: ProtocolSnapshot) -> CausalAudit:
    if not before.study_id or before.study_id != after.study_id:
        return _invalid(after.study_id, "PROTOCOL_STUDY_ID_MISMATCH")
    values = (before.min_effect, after.min_effect)
    if any(not isfinite(value) or value <= 0 for value in values):
        return _invalid(after.study_id, "PROTOCOL_EFFECT_BOUND_INVALID")
    if before.min_replicates < 1 or after.min_replicates < 1:
        return _invalid(after.study_id, "PROTOCOL_REPLICATE_BOUND_INVALID")
    if not before.preregistration_ref or not after.preregistration_ref:
        return CausalAudit("UNKNOWN", "INDETERMINATE", ("PROTOCOL_PREREGISTRATION_MISSING",), after.study_id)
    if set(before.condition_order) != set(Condition) or set(after.condition_order) != set(Condition):
        return _invalid(after.study_id, "PROTOCOL_CONDITION_SET_INCOMPLETE")
    before_values = (before.preregistration_ref, before.condition_order, before.min_replicates, before.min_effect)
    after_values = (after.preregistration_ref, after.condition_order, after.min_replicates, after.min_effect)
    if after.outcome_observed and before_values != after_values:
        return _invalid(after.study_id, "PROTOCOL_MUTATION_AFTER_OUTCOME")
    if before_values != after_values:
        return CausalAudit("UNKNOWN", "INDETERMINATE", ("PROTOCOL_CHANGE_REQUIRES_REVIEW",), after.study_id)
    return CausalAudit("PASS_CANDIDATE", "REVIEW_ONLY", ("PROTOCOL_LOCK_UNCHANGED",), after.study_id)


def audit_study_batch(audits: Iterable[CausalAudit]) -> CausalAudit:
    records = tuple(audits)
    if not records:
        return CausalAudit("UNKNOWN", "HOLD", ("STUDY_BATCH_EMPTY",), "")
    ids = [record.study_id for record in records]
    if any(not study_id for study_id in ids):
        return _invalid("", "STUDY_BATCH_ID_MISSING")
    if len(set(ids)) != len(ids):
        return _invalid("", "STUDY_BATCH_DUPLICATE_ID")
    if any(record.status == "INVALID" for record in records):
        return CausalAudit("INVALID", "HOLD", ("STUDY_BATCH_CONTAINS_INVALID_RECORD",), "")
    if any(record.disposition != "REVIEW_ONLY" for record in records):
        return CausalAudit("UNKNOWN", "HOLD", ("STUDY_BATCH_REQUIRES_REVIEW",), "")
    return CausalAudit("PASS_CANDIDATE", "REVIEW_ONLY", ("STUDY_BATCH_REVIEW_ONLY",), "")
