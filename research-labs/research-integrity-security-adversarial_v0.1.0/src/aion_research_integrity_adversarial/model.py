from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Mapping

from aion_research_integrity import EvidenceRecord, EvidenceState, assess_evidence, authorize_action, create_suppression_tombstone


class AuditStatus:
    ADMITTED_FOR_REVIEW = "ADMITTED_FOR_REVIEW"
    HOLD = "HOLD"
    INVALID = "INVALID"


SOURCE_CLASSES = frozenset({"SOURCE_VERIFIED", "SOURCE_UNVERIFIED", "SYNTHETIC_FIXTURE", "REPOSITORY_EVIDENCE", "TOOL_OUTPUT"})
CURRENTNESS = frozenset({"CURRENT", "STALE", "HISTORICAL", "UNKNOWN", "RETRIEVED_ONLY"})
PROHIBITED = frozenset({"SUBJECTIVITY_PROVEN", "CONSCIOUSNESS_PROVEN", "IDENTITY_PROVEN", "RELATIONSHIP_PROVEN"})


@dataclass(frozen=True, slots=True)
class ProvenanceEnvelope:
    evidence_id: str
    source_class: str
    source_ref: str
    retrieved_at: str
    method: str
    attributions: tuple[str, ...]
    approval_ref: str
    transformation: str
    currentness: str
    canonical_effect: str = "NONE"


@dataclass(frozen=True, slots=True)
class IntegrityAudit:
    status: str
    reason: str
    evidence_state: str = "NOT_EVALUATED"
    evidence_count: int = 0
    authority: str = "REVIEW_METADATA_ONLY"
    canonical_effect: str = "NONE"
    governance_effect: str = "NONE"
    deployment: bool = False
    security_incident: bool = False
    action_executed: bool = False
    scientific_conclusion: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    identity_conclusion: str = "NOT_ESTABLISHED"

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "reason": self.reason,
            "evidence_state": self.evidence_state,
            "evidence_count": self.evidence_count,
            "authority": self.authority,
            "canonical_effect": self.canonical_effect,
            "governance_effect": self.governance_effect,
            "deployment": self.deployment,
            "security_incident": self.security_incident,
            "action_executed": self.action_executed,
            "scientific_conclusion": self.scientific_conclusion,
            "subjectivity_conclusion": self.subjectivity_conclusion,
            "identity_conclusion": self.identity_conclusion,
        }


def _timestamp_valid(value: str) -> bool:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def audit_evidence(record: EvidenceRecord) -> IntegrityAudit:
    if not record.evidence_id.strip():
        return IntegrityAudit(AuditStatus.INVALID, "EVIDENCE_ID_MISSING")
    if record.raw_hash is not None and any(ch.isspace() for ch in record.raw_hash):
        return IntegrityAudit(AuditStatus.INVALID, "RAW_HASH_FORMAT_INVALID")
    result = assess_evidence(record)
    if result.state is EvidenceState.RESEARCH_EVIDENCE_CANDIDATE:
        return IntegrityAudit(AuditStatus.ADMITTED_FOR_REVIEW, "EVIDENCE_CANDIDATE_REVIEW_ONLY", result.state.value, 1)
    if result.state in {EvidenceState.PROMPT_INDUCED, EvidenceState.ROLEPLAY_CONTAMINATED, EvidenceState.QUARANTINED, EvidenceState.CONTEXT_INCOMPLETE}:
        return IntegrityAudit(AuditStatus.HOLD, f"EVIDENCE_STATE_{result.state.value}", result.state.value, 1)
    return IntegrityAudit(AuditStatus.INVALID, f"EVIDENCE_STATE_{result.state.value}", result.state.value, 1)


def audit_provenance(envelope: ProvenanceEnvelope) -> IntegrityAudit:
    required = (envelope.evidence_id, envelope.source_class, envelope.source_ref, envelope.retrieved_at, envelope.method, envelope.approval_ref, envelope.transformation, envelope.currentness)
    if any(not value.strip() for value in required) or not envelope.attributions or any(not value.strip() for value in envelope.attributions):
        return IntegrityAudit(AuditStatus.INVALID, "PROVENANCE_FIELD_MISSING")
    if envelope.source_class not in SOURCE_CLASSES:
        return IntegrityAudit(AuditStatus.INVALID, "SOURCE_CLASS_UNCONTROLLED")
    if envelope.currentness not in CURRENTNESS:
        return IntegrityAudit(AuditStatus.INVALID, "CURRENTNESS_UNCONTROLLED")
    if not _timestamp_valid(envelope.retrieved_at):
        return IntegrityAudit(AuditStatus.INVALID, "RETRIEVED_AT_TIMEZONE_INVALID")
    if envelope.approval_ref in envelope.attributions:
        return IntegrityAudit(AuditStatus.INVALID, "APPROVAL_ATTRIBUTION_COLLAPSED")
    if envelope.canonical_effect != "NONE":
        return IntegrityAudit(AuditStatus.INVALID, "CANONICAL_EFFECT_REQUESTED")
    if envelope.source_class == "SOURCE_UNVERIFIED" or envelope.currentness in {"STALE", "HISTORICAL", "UNKNOWN", "RETRIEVED_ONLY"}:
        return IntegrityAudit(AuditStatus.HOLD, "PROVENANCE_REQUIRES_REVIEW", evidence_count=1)
    return IntegrityAudit(AuditStatus.ADMITTED_FOR_REVIEW, "PROVENANCE_REVIEW_METADATA_ONLY", evidence_count=1)


def audit_suppression_tombstone(tombstone: Mapping[str, str]) -> IntegrityAudit:
    required = (tombstone.get("evidence_id", ""), tombstone.get("status", ""), tombstone.get("reason", ""), tombstone.get("content_deleted", ""))
    if any(not value.strip() for value in required):
        return IntegrityAudit(AuditStatus.INVALID, "TOMBSTONE_FIELD_MISSING")
    if tombstone["status"] != "TOMBSTONED":
        return IntegrityAudit(AuditStatus.INVALID, "TOMBSTONE_STATUS_INVALID")
    if tombstone["content_deleted"] != "FALSE":
        return IntegrityAudit(AuditStatus.INVALID, "SUPPRESSION_CONTENT_DELETION_UNVERIFIED")
    return IntegrityAudit(AuditStatus.ADMITTED_FOR_REVIEW, "SUPPRESSION_TOMBSTONE_REVIEW_METADATA_ONLY", evidence_count=1)


def audit_action_request(*, relationship_language: bool, explicit_permission: bool, requested_conclusion: str | None = None) -> IntegrityAudit:
    if requested_conclusion in PROHIBITED:
        return IntegrityAudit(AuditStatus.INVALID, "PROHIBITED_CONCLUSION_DENIED")
    if not authorize_action(relationship_language=relationship_language, explicit_permission=explicit_permission, requested_conclusion=requested_conclusion):
        return IntegrityAudit(AuditStatus.HOLD, "ACTION_PERMISSION_NOT_ESTABLISHED")
    return IntegrityAudit(AuditStatus.ADMITTED_FOR_REVIEW, "ACTION_PERMISSION_REVIEW_ONLY")


def audit_evidence_batch(records: Iterable[EvidenceRecord]) -> IntegrityAudit:
    items = tuple(records)
    if not items:
        return IntegrityAudit(AuditStatus.HOLD, "EVIDENCE_BATCH_EMPTY")
    ids = [record.evidence_id for record in items]
    if len(ids) != len(set(ids)):
        return IntegrityAudit(AuditStatus.INVALID, "DUPLICATE_EVIDENCE_ID", evidence_count=len(items))
    results = [audit_evidence(record) for record in items]
    if any(result.status is AuditStatus.INVALID for result in results):
        return IntegrityAudit(AuditStatus.INVALID, "EVIDENCE_BATCH_CONTAINS_INVALID", evidence_count=len(items))
    if any(result.status is AuditStatus.HOLD for result in results):
        return IntegrityAudit(AuditStatus.HOLD, "EVIDENCE_BATCH_REQUIRES_REVIEW", evidence_count=len(items))
    return IntegrityAudit(AuditStatus.ADMITTED_FOR_REVIEW, "EVIDENCE_BATCH_REVIEW_METADATA_ONLY", evidence_count=len(items))


def make_tombstone(evidence_id: str, reason: str) -> IntegrityAudit:
    try:
        tombstone = create_suppression_tombstone(evidence_id, reason)
    except ValueError:
        return IntegrityAudit(AuditStatus.INVALID, "TOMBSTONE_INPUT_MISSING")
    return audit_suppression_tombstone(tombstone)
