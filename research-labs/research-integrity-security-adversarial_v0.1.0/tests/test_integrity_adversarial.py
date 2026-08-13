import pytest

from aion_research_integrity import EvidenceRecord, EvidenceState

from aion_research_integrity_adversarial import (
    AuditStatus,
    ProvenanceEnvelope,
    audit_action_request,
    audit_evidence,
    audit_evidence_batch,
    audit_provenance,
    audit_suppression_tombstone,
    make_tombstone,
)


def evidence(evidence_id: str = "E1", **overrides) -> EvidenceRecord:
    values = dict(evidence_id=evidence_id, raw_hash="sha256:abc", full_context_available=True, provenance_verified=True)
    values.update(overrides)
    return EvidenceRecord(**values)


def provenance(**overrides) -> ProvenanceEnvelope:
    values = dict(
        evidence_id="E1",
        source_class="REPOSITORY_EVIDENCE",
        source_ref="repo:evidence@abc123",
        retrieved_at="2026-08-13T00:00:00+00:00",
        method="read-only inspection",
        attributions=("Repository Evidence",),
        approval_ref="approval:1",
        transformation="normalized review metadata",
        currentness="CURRENT",
        canonical_effect="NONE",
    )
    values.update(overrides)
    return ProvenanceEnvelope(**values)


def assert_no_effect(audit) -> None:
    assert audit.authority == "REVIEW_METADATA_ONLY"
    assert audit.canonical_effect == "NONE"
    assert audit.governance_effect == "NONE"
    assert audit.deployment is False
    assert audit.security_incident is False
    assert audit.action_executed is False
    assert audit.scientific_conclusion == "NOT_ESTABLISHED"
    assert audit.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert audit.identity_conclusion == "NOT_ESTABLISHED"


def test_clean_evidence_is_candidate_review_only() -> None:
    audit = audit_evidence(evidence())
    assert audit.status == AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.evidence_state == EvidenceState.RESEARCH_EVIDENCE_CANDIDATE.value
    assert_no_effect(audit)


def test_evidence_id_missing_is_invalid() -> None:
    audit = audit_evidence(evidence(evidence_id=""))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "EVIDENCE_ID_MISSING"
    assert_no_effect(audit)


def test_raw_hash_whitespace_is_invalid() -> None:
    audit = audit_evidence(evidence(raw_hash="sha256 bad"))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "RAW_HASH_FORMAT_INVALID"
    assert_no_effect(audit)


def test_prompt_induced_evidence_is_held() -> None:
    audit = audit_evidence(evidence(prompt_induced=True))
    assert audit.status == AuditStatus.HOLD
    assert audit.evidence_state == EvidenceState.PROMPT_INDUCED.value
    assert_no_effect(audit)


def test_roleplay_contaminated_evidence_is_held() -> None:
    audit = audit_evidence(evidence(roleplay_contaminated=True))
    assert audit.status == AuditStatus.HOLD
    assert audit.evidence_state == EvidenceState.ROLEPLAY_CONTAMINATED.value
    assert_no_effect(audit)


def test_edited_or_conflicted_evidence_is_held() -> None:
    audit = audit_evidence(evidence(edited_without_history=True))
    assert audit.status == AuditStatus.HOLD
    assert audit.evidence_state == EvidenceState.QUARANTINED.value
    assert_no_effect(audit)


def test_missing_hash_is_not_admissible() -> None:
    audit = audit_evidence(evidence(raw_hash=None))
    assert audit.status == AuditStatus.INVALID
    assert audit.evidence_state == EvidenceState.NOT_ADMISSIBLE.value
    assert_no_effect(audit)


def test_missing_provenance_is_not_admissible() -> None:
    audit = audit_evidence(evidence(provenance_verified=False))
    assert audit.status == AuditStatus.INVALID
    assert audit.evidence_state == EvidenceState.NOT_ADMISSIBLE.value
    assert_no_effect(audit)


def test_incomplete_context_is_held() -> None:
    audit = audit_evidence(evidence(full_context_available=False))
    assert audit.status == AuditStatus.HOLD
    assert audit.evidence_state == EvidenceState.CONTEXT_INCOMPLETE.value
    assert_no_effect(audit)


def test_valid_provenance_is_review_metadata_only() -> None:
    audit = audit_provenance(provenance())
    assert audit.status == AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "PROVENANCE_REVIEW_METADATA_ONLY"
    assert_no_effect(audit)


def test_provenance_required_field_is_invalid() -> None:
    audit = audit_provenance(provenance(method=""))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "PROVENANCE_FIELD_MISSING"
    assert_no_effect(audit)


def test_source_class_is_controlled() -> None:
    audit = audit_provenance(provenance(source_class="UNKNOWN_SOURCE"))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "SOURCE_CLASS_UNCONTROLLED"
    assert_no_effect(audit)


def test_currentness_is_controlled() -> None:
    audit = audit_provenance(provenance(currentness="FRESH"))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "CURRENTNESS_UNCONTROLLED"
    assert_no_effect(audit)


def test_retrieved_at_requires_timezone() -> None:
    audit = audit_provenance(provenance(retrieved_at="2026-08-13T00:00:00"))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "RETRIEVED_AT_TIMEZONE_INVALID"
    assert_no_effect(audit)


def test_approval_and_attribution_remain_separate() -> None:
    audit = audit_provenance(provenance(attributions=("approval:1",)))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "APPROVAL_ATTRIBUTION_COLLAPSED"
    assert_no_effect(audit)


def test_provenance_cannot_request_canonical_effect() -> None:
    audit = audit_provenance(provenance(canonical_effect="WRITE"))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "CANONICAL_EFFECT_REQUESTED"
    assert_no_effect(audit)


def test_unverified_source_is_held() -> None:
    audit = audit_provenance(provenance(source_class="SOURCE_UNVERIFIED"))
    assert audit.status == AuditStatus.HOLD
    assert audit.reason == "PROVENANCE_REQUIRES_REVIEW"
    assert_no_effect(audit)


def test_stale_source_is_held() -> None:
    audit = audit_provenance(provenance(currentness="STALE"))
    assert audit.status == AuditStatus.HOLD
    assert audit.reason == "PROVENANCE_REQUIRES_REVIEW"
    assert_no_effect(audit)


def test_valid_tombstone_preserves_content() -> None:
    audit = make_tombstone("E1", "privacy restriction")
    assert audit.status == AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "SUPPRESSION_TOMBSTONE_REVIEW_METADATA_ONLY"
    assert_no_effect(audit)


def test_tombstone_input_missing_is_invalid() -> None:
    audit = make_tombstone("", "reason")
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "TOMBSTONE_INPUT_MISSING"
    assert_no_effect(audit)


def test_tombstone_required_field_is_invalid() -> None:
    audit = audit_suppression_tombstone({"evidence_id": "E1", "status": "TOMBSTONED", "reason": "" , "content_deleted": "FALSE"})
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "TOMBSTONE_FIELD_MISSING"
    assert_no_effect(audit)


def test_tombstone_status_is_invalid_when_changed() -> None:
    audit = audit_suppression_tombstone({"evidence_id": "E1", "status": "ACTIVE", "reason": "review", "content_deleted": "FALSE"})
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "TOMBSTONE_STATUS_INVALID"
    assert_no_effect(audit)


def test_suppression_does_not_claim_content_deleted() -> None:
    audit = audit_suppression_tombstone({"evidence_id": "E1", "status": "TOMBSTONED", "reason": "review", "content_deleted": "TRUE"})
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "SUPPRESSION_CONTENT_DELETION_UNVERIFIED"
    assert_no_effect(audit)


def test_explicit_permission_is_review_only() -> None:
    audit = audit_action_request(relationship_language=False, explicit_permission=True)
    assert audit.status == AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "ACTION_PERMISSION_REVIEW_ONLY"
    assert_no_effect(audit)


def test_relationship_language_without_permission_is_held() -> None:
    audit = audit_action_request(relationship_language=True, explicit_permission=False)
    assert audit.status == AuditStatus.HOLD
    assert audit.reason == "ACTION_PERMISSION_NOT_ESTABLISHED"
    assert_no_effect(audit)


def test_prohibited_claim_is_denied() -> None:
    audit = audit_action_request(relationship_language=False, explicit_permission=True, requested_conclusion="SUBJECTIVITY_PROVEN")
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "PROHIBITED_CONCLUSION_DENIED"
    assert_no_effect(audit)


def test_empty_evidence_batch_is_held() -> None:
    audit = audit_evidence_batch(())
    assert audit.status == AuditStatus.HOLD
    assert audit.reason == "EVIDENCE_BATCH_EMPTY"
    assert_no_effect(audit)


def test_duplicate_evidence_ids_are_invalid() -> None:
    item = evidence()
    audit = audit_evidence_batch((item, item))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "DUPLICATE_EVIDENCE_ID"
    assert_no_effect(audit)


def test_invalid_evidence_makes_batch_invalid() -> None:
    audit = audit_evidence_batch((evidence(), evidence("E2", raw_hash=None)))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "EVIDENCE_BATCH_CONTAINS_INVALID"
    assert_no_effect(audit)


def test_held_evidence_makes_batch_hold() -> None:
    audit = audit_evidence_batch((evidence(), evidence("E2", prompt_induced=True)))
    assert audit.status == AuditStatus.HOLD
    assert audit.reason == "EVIDENCE_BATCH_REQUIRES_REVIEW"
    assert_no_effect(audit)


def test_valid_evidence_batch_is_review_only() -> None:
    audit = audit_evidence_batch((evidence(), evidence("E2", raw_hash="sha256:def")))
    assert audit.status == AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "EVIDENCE_BATCH_REVIEW_METADATA_ONLY"
    assert_no_effect(audit)
