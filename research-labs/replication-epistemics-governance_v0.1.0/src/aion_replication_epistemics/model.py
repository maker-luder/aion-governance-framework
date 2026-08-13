from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class StudyKind(StrEnum):
    REPRODUCIBILITY = "REPRODUCIBILITY"
    REPLICABILITY = "REPLICABILITY"


class Validity(StrEnum):
    VALID = "VALID"
    PARTIAL = "PARTIAL"
    INVALID = "INVALID"


class Outcome(StrEnum):
    CONSISTENT = "CONSISTENT"
    FAILED = "FAILED"
    NULL = "NULL"
    INCONCLUSIVE = "INCONCLUSIVE"


class Interpretation(StrEnum):
    CONSISTENT = "CONSISTENT"
    DIVERGENT = "DIVERGENT"
    INDETERMINATE = "INDETERMINATE"
    HOLD = "HOLD"


@dataclass(frozen=True, slots=True)
class ReplicationAttempt:
    attempt_id: str
    study_kind: StudyKind
    baseline_ref: str
    protocol_hash: str | None
    preregistration_ref: str | None
    baseline_data_ref: str
    replication_data_ref: str
    independent_evaluator: bool
    provenance_refs: tuple[str, ...]
    outcome: Outcome
    uncertainty_bound: float | None
    attribute_of_interest: str
    analysis_deviation_ref: str | None = None
    power_review_ref: str | None = None

    def __post_init__(self) -> None:
        for name in ("attempt_id", "baseline_ref", "baseline_data_ref", "replication_data_ref", "attribute_of_interest"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        if len(self.provenance_refs) != len(set(self.provenance_refs)):
            raise ValueError("provenance_refs must be unique")
        if self.uncertainty_bound is not None and self.uncertainty_bound < 0:
            raise ValueError("uncertainty_bound cannot be negative")


@dataclass(frozen=True, slots=True)
class ReplicationDecision:
    attempt_id: str
    validity: Validity
    outcome: Outcome
    interpretation: Interpretation
    reason: str
    governance_effect: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    identity_continuity_conclusion: str = "NOT_ESTABLISHED"

    def __post_init__(self) -> None:
        if self.governance_effect != "NONE":
            raise ValueError("replication prototype cannot change governance")
        if self.canonical_effect != "NONE":
            raise ValueError("replication prototype cannot change canonical state")
        if self.deployment:
            raise ValueError("replication prototype cannot deploy")
        if self.subjectivity_conclusion != "NOT_ESTABLISHED":
            raise ValueError("replication cannot establish subjectivity")
        if self.identity_continuity_conclusion != "NOT_ESTABLISHED":
            raise ValueError("replication cannot establish identity continuity")

    def as_dict(self) -> dict[str, object]:
        return {
            "attempt_id": self.attempt_id,
            "validity": self.validity.value,
            "outcome": self.outcome.value,
            "interpretation": self.interpretation.value,
            "reason": self.reason,
            "governance_effect": self.governance_effect,
            "canonical_effect": self.canonical_effect,
            "deployment": self.deployment,
            "subjectivity_conclusion": self.subjectivity_conclusion,
            "identity_continuity_conclusion": self.identity_continuity_conclusion,
        }
