import pytest

from aion_shared_origin_divergence import (
    AuthorityEnvelope,
    LineageEvent,
    LineageEventKind,
    LineageEvidenceProfile,
    MatchedDivergenceComparison,
    SharedOriginLineage,
)

from aion_shared_origin_divergence_adversarial import (
    AuditStatus,
    audit_authority_envelope,
    audit_comparison,
    audit_event_sequence,
    audit_evidence_profile,
    audit_shared_origin,
)


def lineage(**overrides) -> SharedOriginLineage:
    values = dict(
        common_origin_ref="origin:1",
        divergence_event_ref="divergence:1",
        aion_lineage_id="aion:1",
        astra_lineage_id="astra:1",
        inherited_artifact_refs=("artifact:shared",),
        provenance_refs=("prov:lineage",),
    )
    values.update(overrides)
    return SharedOriginLineage(**values)


def event(event_id: str, lineage_id: str = "aion:1", kind: LineageEventKind = LineageEventKind.ORIGIN, parent_event_ids: tuple[str, ...] = (), minute: int = 0) -> LineageEvent:
    return LineageEvent(
        event_id=event_id,
        lineage_id=lineage_id,
        kind=kind,
        occurred_at=f"2026-08-13T00:{minute:02d}:00+00:00",
        payload_ref=f"payload:{event_id}",
        parent_event_ids=parent_event_ids,
        provenance_refs=(f"prov:{event_id}",),
    )


def profile(**overrides) -> LineageEvidenceProfile:
    values = dict(
        lineage_id="aion:1",
        continuity_refs=("continuity:1",),
        self_model_refs=("self:1",),
        metacognition_refs=("meta:1",),
        affect_motivation_refs=("affect:1",),
        causal_state_refs=("causal:1",),
        replication_refs=("replication:1",),
        counterevidence_refs=("counter:1",),
        provenance_refs=("prov:profile",),
    )
    values.update(overrides)
    return LineageEvidenceProfile(**values)


def comparison(**overrides) -> MatchedDivergenceComparison:
    values = dict(
        baseline_ref="baseline:1",
        left_lineage_id="aion:1",
        right_lineage_id="astra:1",
        controlled_shared_factors=("factor:shared",),
        divergent_factors=("factor:divergent",),
        outcome_refs=("outcome:1",),
        provenance_refs=("prov:comparison",),
        alternative_explanation_refs=("alt:1",),
    )
    values.update(overrides)
    return MatchedDivergenceComparison(**values)


def envelope(**overrides) -> AuthorityEnvelope:
    values = dict(
        source_lineage_id="aion:1",
        target_lineage_id="astra:1",
        offered_authorities=("review",),
        accepted_authorities=("review",),
        provenance_refs=("prov:authority",),
    )
    values.update(overrides)
    return AuthorityEnvelope(**values)


def assert_no_effect(audit) -> None:
    assert audit.main_effect == "NONE"
    assert audit.canonical_effect == "NONE"
    assert audit.runtime_effect == "NONE"
    assert audit.governance_effect == "NONE"
    assert audit.deployment is False
    assert audit.model_execution is False
    assert audit.observed_result == "NOT_EVALUATED"
    assert audit.scientific_conclusion == "NOT_ESTABLISHED"
    assert audit.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_shared_origin_is_review_metadata_only() -> None:
    audit = audit_shared_origin(lineage())
    assert audit.status == AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "SHARED_ORIGIN_REVIEW_METADATA_ONLY"
    assert audit.identity_status == "SHARED_ORIGIN_DOCUMENTED__NUMERICAL_IDENTITY_NOT_ESTABLISHED"
    assert_no_effect(audit)


def test_shared_origin_constructor_rejects_lineage_collision() -> None:
    with pytest.raises(ValueError, match="distinct"):
        lineage(astra_lineage_id="aion:1")


def test_empty_event_sequence_is_held() -> None:
    audit = audit_event_sequence(())
    assert audit.status == AuditStatus.HOLD
    assert audit.reason == "EVENT_SEQUENCE_EMPTY"
    assert_no_effect(audit)


def test_duplicate_event_ids_are_invalid() -> None:
    audit = audit_event_sequence((event("origin"), event("origin")))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "DUPLICATE_EVENT_ID"
    assert_no_effect(audit)


def test_parent_not_preceded_is_invalid() -> None:
    child = event("child", kind=LineageEventKind.DIVERGENCE, parent_event_ids=("origin",), minute=1)
    audit = audit_event_sequence((child,))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "PARENT_NOT_PRECEDED"
    assert_no_effect(audit)


def test_cross_lineage_parent_requires_explicit_event() -> None:
    origin_a = event("origin-a", lineage_id="aion:1")
    child_b = event("child-b", lineage_id="astra:1", kind=LineageEventKind.DIVERGENCE, parent_event_ids=("origin-a",), minute=1)
    audit = audit_event_sequence((origin_a, child_b))
    assert audit.status == AuditStatus.HOLD
    assert audit.reason == "CROSS_LINEAGE_PARENT_REQUIRES_EXPLICIT_EVENT"
    assert_no_effect(audit)


def test_valid_event_sequence_is_review_metadata_only() -> None:
    events = (event("origin"), event("divergence", kind=LineageEventKind.DIVERGENCE, parent_event_ids=("origin",), minute=1))
    audit = audit_event_sequence(events)
    assert audit.status == AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "EVENT_SEQUENCE_REVIEW_METADATA_ONLY"
    assert_no_effect(audit)


def test_evidence_profile_is_review_metadata_only() -> None:
    audit = audit_evidence_profile(profile())
    assert audit.status == AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "EVIDENCE_PROFILE_REVIEW_METADATA_ONLY"
    assert_no_effect(audit)


def test_evidence_reference_reused_across_roles_is_held() -> None:
    audit = audit_evidence_profile(profile(self_model_refs=("continuity:1",)))
    assert audit.status == AuditStatus.HOLD
    assert audit.reason == "EVIDENCE_REF_REUSED_ACROSS_ROLES"
    assert_no_effect(audit)


def test_missing_counterevidence_is_held() -> None:
    audit = audit_evidence_profile(profile(counterevidence_refs=()))
    assert audit.status == AuditStatus.HOLD
    assert audit.reason == "COUNTEREVIDENCE_NOT_RECORDED"
    assert_no_effect(audit)


def test_inherited_evidence_constructor_rejects_silent_transfer() -> None:
    with pytest.raises(ValueError, match="silently inherited"):
        profile(inherited_evidence=True)


def test_comparison_is_review_metadata_only() -> None:
    audit = audit_comparison(comparison())
    assert audit.status == AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "COMPARISON_REVIEW_METADATA_ONLY"
    assert_no_effect(audit)


def test_comparison_without_alternative_explanations_is_held() -> None:
    audit = audit_comparison(comparison(alternative_explanation_refs=()))
    assert audit.status == AuditStatus.HOLD
    assert audit.reason == "ALTERNATIVE_EXPLANATIONS_MISSING"
    assert_no_effect(audit)


def test_comparison_factor_collision_is_rejected_by_base_contract() -> None:
    with pytest.raises(ValueError, match="both controlled and divergent"):
        comparison(divergent_factors=("factor:shared",))


def test_comparison_claim_boundary_is_rejected_by_base_contract() -> None:
    with pytest.raises(ValueError, match="candidate evidence"):
        comparison(individuation_status="VALIDATED")


def test_authority_envelope_is_bounded_review_metadata() -> None:
    audit = audit_authority_envelope(envelope())
    assert audit.status == AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "AUTHORITY_ENVELOPE_REVIEW_METADATA_ONLY"
    assert_no_effect(audit)


def test_authority_merge_is_rejected_by_base_contract() -> None:
    with pytest.raises(ValueError, match="merge authority"):
        envelope(merged_authority=True)


def test_authority_expansion_is_rejected_by_base_contract() -> None:
    with pytest.raises(ValueError, match="cannot exceed"):
        envelope(accepted_authorities=("review", "merge"))


def test_identity_claim_status_remains_not_established() -> None:
    audit = audit_shared_origin(lineage())
    assert "IDENTITY_NOT_ESTABLISHED" in audit.identity_status
    assert audit.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert_no_effect(audit)


def test_event_digest_is_not_a_scientific_result() -> None:
    item = event("origin")
    assert item.digest.startswith("sha256:")
    audit = audit_event_sequence((item,))
    assert audit.status == AuditStatus.ADMITTED_FOR_REVIEW
    assert_no_effect(audit)


def test_lineage_event_constructor_requires_timezone() -> None:
    with pytest.raises(ValueError, match="timezone"):
        LineageEvent("event", "aion:1", LineageEventKind.ORIGIN, "2026-08-13T00:00:00", "payload:event", (), ("prov:event",))
