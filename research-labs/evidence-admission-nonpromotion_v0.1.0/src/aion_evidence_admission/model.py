"""Evidence admission and non-promotion contract for research-only claims."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class AdmissionStatus(StrEnum):
    ADMISSIBLE_FOR_REVIEW = "ADMISSIBLE_FOR_REVIEW"
    INDETERMINATE = "INDETERMINATE"
    HOLD = "HOLD"


class EvidenceTier(StrEnum):
    MECHANISM_ONLY = "MECHANISM_ONLY"
    REPLICATION_SUPPORT = "REPLICATION_SUPPORT"
    SYNTHESIS = "SYNTHESIS"


class ReplicationState(StrEnum):
    NOT_EVALUATED = "NOT_EVALUATED"
    CONSISTENT = "CONSISTENT"
    DIVERGENT = "DIVERGENT"
    INDETERMINATE = "INDETERMINATE"


@dataclass(frozen=True, slots=True)
class EvidenceDimensions:
    risk_of_bias: str | None
    consistency: str | None
    precision: str | None
    directness: str | None
    reporting_bias: str | None


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    evidence_id: str
    claim_ref: str | None
    claim_type: str | None
    evidence_tier: EvidenceTier
    source_ref: str | None
    provenance_ref: str | None
    method_ref: str | None
    data_ref: str | None
    dimensions: EvidenceDimensions
    replication_state: ReplicationState
    contradiction_refs: tuple[str, ...]
    observed_effect: bool
    uncertainty_ref: str | None
    governance_effect_requested: bool


@dataclass(frozen=True, slots=True)
class AdmissionDecision:
    status: AdmissionStatus
    reason: str
    evidence_id: str
    missing_fields: tuple[str, ...] = ()
    contradiction_fields: tuple[str, ...] = ()
    evidence_tier: EvidenceTier | None = None
    replication_state: ReplicationState = ReplicationState.NOT_EVALUATED
    scientific_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False
    governance_effect: str = "NONE"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    identity_continuity_conclusion: str = "NOT_ESTABLISHED"

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["status"] = self.status.value
        if self.evidence_tier is not None:
            payload["evidence_tier"] = self.evidence_tier.value
        payload["replication_state"] = self.replication_state.value
        return payload


def _missing(values: dict[str, object]) -> tuple[str, ...]:
    return tuple(key for key, value in values.items() if value is None or value == "")


def _base_hold(record: EvidenceRecord, reason: str, *, missing: tuple[str, ...] = (), contradictions: tuple[str, ...] = ()) -> AdmissionDecision:
    return AdmissionDecision(
        AdmissionStatus.HOLD,
        reason,
        record.evidence_id,
        missing_fields=missing,
        contradiction_fields=contradictions,
        evidence_tier=record.evidence_tier,
        replication_state=record.replication_state,
    )


def audit_evidence(record: EvidenceRecord) -> AdmissionDecision:
    """Audit claim-evidence metadata only; never promotes or deploys a claim."""

    required = {
        "claim_ref": record.claim_ref,
        "claim_type": record.claim_type,
        "source_ref": record.source_ref,
        "provenance_ref": record.provenance_ref,
        "method_ref": record.method_ref,
        "data_ref": record.data_ref,
        "uncertainty_ref": record.uncertainty_ref,
        "dimensions.risk_of_bias": record.dimensions.risk_of_bias,
        "dimensions.consistency": record.dimensions.consistency,
        "dimensions.precision": record.dimensions.precision,
        "dimensions.directness": record.dimensions.directness,
        "dimensions.reporting_bias": record.dimensions.reporting_bias,
    }
    missing = _missing(required)
    if missing:
        return _base_hold(record, "EVIDENCE_METADATA_INCOMPLETE", missing=missing)
    if record.contradiction_refs:
        return _base_hold(record, "CONTRADICTORY_EVIDENCE_REQUIRES_REVIEW", contradictions=("contradiction_refs",))
    if record.governance_effect_requested:
        return _base_hold(record, "EVIDENCE_ADMISSION_CANNOT_REQUEST_GOVERNANCE_EFFECT", contradictions=("governance_effect_requested",))
    if record.observed_effect and record.evidence_tier is EvidenceTier.MECHANISM_ONLY:
        return _base_hold(record, "MECHANISM_ONLY_CANNOT_ASSERT_OBSERVED_EFFECT", contradictions=("observed_effect", "evidence_tier"))
    if record.evidence_tier is EvidenceTier.REPLICATION_SUPPORT and record.replication_state is ReplicationState.NOT_EVALUATED:
        return _base_hold(record, "REPLICATION_TIER_REQUIRES_REPLICATION_STATE", contradictions=("replication_state",))
    if record.evidence_tier is EvidenceTier.SYNTHESIS and record.replication_state is ReplicationState.DIVERGENT:
        return _base_hold(record, "DIVERGENT_SYNTHESIS_REQUIRES_REVIEW", contradictions=("replication_state",))
    if record.replication_state is ReplicationState.INDETERMINATE:
        return AdmissionDecision(
            AdmissionStatus.INDETERMINATE,
            "REPLICATION_UNCERTAINTY_LIMITS_ADMISSION",
            record.evidence_id,
            evidence_tier=record.evidence_tier,
            replication_state=record.replication_state,
        )
    return AdmissionDecision(
        AdmissionStatus.ADMISSIBLE_FOR_REVIEW,
        "EVIDENCE_ADMISSIBLE_FOR_REVIEW_ONLY",
        record.evidence_id,
        evidence_tier=record.evidence_tier,
        replication_state=record.replication_state,
    )
