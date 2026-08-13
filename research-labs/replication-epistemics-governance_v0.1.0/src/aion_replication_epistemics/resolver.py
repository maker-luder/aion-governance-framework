from __future__ import annotations

from .model import (
    Interpretation,
    Outcome,
    ReplicationAttempt,
    ReplicationDecision,
    StudyKind,
    Validity,
)


def evaluate_attempt(attempt: ReplicationAttempt) -> ReplicationDecision:
    """Evaluate replication evidence without changing any governance state."""
    if not attempt.provenance_refs or not attempt.protocol_hash:
        return ReplicationDecision(
            attempt.attempt_id,
            Validity.INVALID,
            attempt.outcome,
            Interpretation.HOLD,
            "MISSING_PROTOCOL_OR_PROVENANCE",
        )

    if attempt.study_kind is StudyKind.REPLICABILITY:
        if attempt.baseline_data_ref == attempt.replication_data_ref:
            return ReplicationDecision(
                attempt.attempt_id,
                Validity.INVALID,
                attempt.outcome,
                Interpretation.HOLD,
                "REPLICABILITY_REQUIRES_INDEPENDENT_DATA",
            )
        if not attempt.independent_evaluator:
            return ReplicationDecision(
                attempt.attempt_id,
                Validity.PARTIAL,
                attempt.outcome,
                Interpretation.HOLD,
                "INDEPENDENT_EVALUATOR_MISSING",
            )
    if attempt.analysis_deviation_ref is None and attempt.power_review_ref is None:
        return ReplicationDecision(
            attempt.attempt_id,
            Validity.PARTIAL,
            attempt.outcome,
            Interpretation.HOLD,
            "UNCERTAINTY_OR_DEVIATION_REVIEW_MISSING",
        )

    if attempt.uncertainty_bound is None:
        return ReplicationDecision(
            attempt.attempt_id,
            Validity.PARTIAL,
            attempt.outcome,
            Interpretation.INDETERMINATE,
            "UNCERTAINTY_NOT_QUANTIFIED",
        )

    if attempt.outcome is Outcome.CONSISTENT:
        return ReplicationDecision(
            attempt.attempt_id,
            Validity.VALID,
            attempt.outcome,
            Interpretation.CONSISTENT,
            "VALID_CONSISTENT_RESULT",
        )
    if attempt.outcome is Outcome.FAILED:
        return ReplicationDecision(
            attempt.attempt_id,
            Validity.VALID,
            attempt.outcome,
            Interpretation.DIVERGENT,
            "VALID_FAILED_REPLICATION_NOT_AUTOMATIC_DOWNGRADE",
        )
    if attempt.outcome in {Outcome.NULL, Outcome.INCONCLUSIVE}:
        return ReplicationDecision(
            attempt.attempt_id,
            Validity.VALID,
            attempt.outcome,
            Interpretation.INDETERMINATE,
            "VALID_NULL_OR_INCONCLUSIVE_REQUIRES_BODY_OF_EVIDENCE",
        )
    raise ValueError(f"unsupported outcome: {attempt.outcome}")
