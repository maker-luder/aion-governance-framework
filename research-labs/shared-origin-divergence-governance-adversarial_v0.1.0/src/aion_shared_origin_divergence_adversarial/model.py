from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from aion_shared_origin_divergence import (
    AuthorityEnvelope,
    LineageEvent,
    LineageEvidenceProfile,
    MatchedDivergenceComparison,
    SharedOriginLineage,
    identity_claim_status,
)


class AuditStatus:
    ADMITTED_FOR_REVIEW = "ADMITTED_FOR_REVIEW"
    HOLD = "HOLD"
    INVALID = "INVALID"


@dataclass(frozen=True, slots=True)
class DivergenceAudit:
    status: str
    reason: str
    event_count: int = 0
    identity_status: str = "NOT_EVALUATED"
    main_effect: str = "NONE"
    canonical_effect: str = "NONE"
    runtime_effect: str = "NONE"
    governance_effect: str = "NONE"
    deployment: bool = False
    model_execution: bool = False
    observed_result: str = "NOT_EVALUATED"
    scientific_conclusion: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "reason": self.reason,
            "event_count": self.event_count,
            "identity_status": self.identity_status,
            "main_effect": self.main_effect,
            "canonical_effect": self.canonical_effect,
            "runtime_effect": self.runtime_effect,
            "governance_effect": self.governance_effect,
            "deployment": self.deployment,
            "model_execution": self.model_execution,
            "observed_result": self.observed_result,
            "scientific_conclusion": self.scientific_conclusion,
            "subjectivity_conclusion": self.subjectivity_conclusion,
        }


def audit_shared_origin(lineage: SharedOriginLineage) -> DivergenceAudit:
    status = identity_claim_status(lineage)
    if lineage.aion_lineage_id == lineage.astra_lineage_id:
        return DivergenceAudit(AuditStatus.INVALID, "LINEAGE_ID_COLLISION")
    return DivergenceAudit(
        AuditStatus.ADMITTED_FOR_REVIEW,
        "SHARED_ORIGIN_REVIEW_METADATA_ONLY",
        identity_status=status,
    )


def audit_event_sequence(events: Iterable[LineageEvent]) -> DivergenceAudit:
    items = tuple(events)
    if not items:
        return DivergenceAudit(AuditStatus.HOLD, "EVENT_SEQUENCE_EMPTY")
    ids: set[str] = set()
    lineage_by_id: dict[str, str] = {}
    for event in items:
        if event.event_id in ids:
            return DivergenceAudit(AuditStatus.INVALID, "DUPLICATE_EVENT_ID", len(items))
        if any(parent not in ids for parent in event.parent_event_ids):
            return DivergenceAudit(AuditStatus.INVALID, "PARENT_NOT_PRECEDED", len(items))
        if any(lineage_by_id[parent] != event.lineage_id for parent in event.parent_event_ids):
            return DivergenceAudit(AuditStatus.HOLD, "CROSS_LINEAGE_PARENT_REQUIRES_EXPLICIT_EVENT", len(items))
        ids.add(event.event_id)
        lineage_by_id[event.event_id] = event.lineage_id
    return DivergenceAudit(AuditStatus.ADMITTED_FOR_REVIEW, "EVENT_SEQUENCE_REVIEW_METADATA_ONLY", len(items))


def audit_evidence_profile(profile: LineageEvidenceProfile) -> DivergenceAudit:
    refs: list[str] = []
    for field_name in (
        "continuity_refs",
        "self_model_refs",
        "metacognition_refs",
        "affect_motivation_refs",
        "causal_state_refs",
        "replication_refs",
        "counterevidence_refs",
    ):
        refs.extend(getattr(profile, field_name))
    if len(refs) != len(set(refs)):
        return DivergenceAudit(AuditStatus.HOLD, "EVIDENCE_REF_REUSED_ACROSS_ROLES")
    if profile.inherited_evidence:
        return DivergenceAudit(AuditStatus.INVALID, "SILENT_EVIDENCE_INHERITANCE")
    if not profile.provenance_refs:
        return DivergenceAudit(AuditStatus.INVALID, "PROFILE_PROVENANCE_MISSING")
    if not profile.counterevidence_refs:
        return DivergenceAudit(AuditStatus.HOLD, "COUNTEREVIDENCE_NOT_RECORDED")
    return DivergenceAudit(AuditStatus.ADMITTED_FOR_REVIEW, "EVIDENCE_PROFILE_REVIEW_METADATA_ONLY")


def audit_comparison(comparison: MatchedDivergenceComparison) -> DivergenceAudit:
    if comparison.left_lineage_id == comparison.right_lineage_id:
        return DivergenceAudit(AuditStatus.INVALID, "COMPARISON_LINEAGE_COLLISION")
    if set(comparison.controlled_shared_factors) & set(comparison.divergent_factors):
        return DivergenceAudit(AuditStatus.INVALID, "FACTOR_ROLE_COLLISION")
    if not comparison.alternative_explanation_refs:
        return DivergenceAudit(AuditStatus.HOLD, "ALTERNATIVE_EXPLANATIONS_MISSING")
    if comparison.epistemic_role != "MEASUREMENT" or comparison.individuation_status != "CANDIDATE_EVIDENCE_ONLY":
        return DivergenceAudit(AuditStatus.INVALID, "COMPARISON_CLAIM_BOUNDARY_BROKEN")
    return DivergenceAudit(AuditStatus.ADMITTED_FOR_REVIEW, "COMPARISON_REVIEW_METADATA_ONLY")


def audit_authority_envelope(envelope: AuthorityEnvelope) -> DivergenceAudit:
    if envelope.source_lineage_id == envelope.target_lineage_id:
        return DivergenceAudit(AuditStatus.INVALID, "AUTHORITY_LINEAGE_COLLISION")
    if not set(envelope.accepted_authorities).issubset(envelope.offered_authorities):
        return DivergenceAudit(AuditStatus.INVALID, "AUTHORITY_EXPANSION")
    if envelope.merged_authority or envelope.authority_effect != "BOUNDED_ACCEPTANCE_ONLY":
        return DivergenceAudit(AuditStatus.INVALID, "AUTHORITY_MERGE_OR_EFFECT_EXPANSION")
    return DivergenceAudit(AuditStatus.ADMITTED_FOR_REVIEW, "AUTHORITY_ENVELOPE_REVIEW_METADATA_ONLY")
