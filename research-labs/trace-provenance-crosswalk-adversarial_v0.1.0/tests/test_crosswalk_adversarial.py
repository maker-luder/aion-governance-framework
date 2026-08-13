import pytest

from aion_trace_crosswalk import AIONTraceEvent, TracePolicy

from aion_trace_crosswalk_adversarial import (
    AuditStatus,
    CrosswalkEntry,
    audit_event_batch,
    audit_source_entries,
    audit_source_entry,
    audit_trace_crosswalk,
)


def event(event_id: str = "event:1", **overrides) -> AIONTraceEvent:
    values = dict(
        session_id="session:1",
        user_id="user:1",
        agent_name="agent:research",
        span_kind="CHAIN",
        runtime_event_id=event_id,
        subject_id="subject:1",
        input_value="private-input",
        output_value="private-output",
        tool_name="read_file",
        tool_parameters="path=fixture",
        retrieval_documents=("doc:1",),
        evaluation_name="bounded-check",
        evaluation_score=0.5,
        evaluation_label="review",
        evaluation_explanation="synthetic",
        graph_node_id="node:1",
        graph_parent_id=None,
        metadata={"fixture": True},
        source_ref="repo:fixture@abc123",
        approval_ref="approval:1",
        canonical_effect="NONE",
    )
    values.update(overrides)
    return AIONTraceEvent(**values)


def entry(entry_id: str = "entry:1", **overrides) -> CrosswalkEntry:
    values = dict(
        entry_id=entry_id,
        source_ref="repo:fixture@abc123",
        source_kind="Repository Evidence",
        what="trace contract",
        who="Manus",
        where="research-labs/trace-provenance-crosswalk_v0.1.0",
        when="2026-08-13",
        method="read-only source inspection",
        authority="Repository Evidence",
        transformation="crosswalk to review metadata",
        currentness="CURRENT",
        target_field="session.id",
        evidence_reused=True,
        new_evidence_claimed=False,
    )
    values.update(overrides)
    return CrosswalkEntry(**values)


def assert_no_effect(audit) -> None:
    assert audit.authority == "EXTERNAL_OBSERVATION_ONLY"
    assert audit.canonical_effect == "NONE"
    assert audit.governance_effect == "NONE"
    assert audit.deployment is False
    assert audit.model_execution is False
    assert audit.observed_result == "NOT_EVALUATED"
    assert audit.scientific_conclusion == "NOT_ESTABLISHED"
    assert audit.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_valid_trace_is_review_metadata_only() -> None:
    audit = audit_trace_crosswalk(event())
    assert audit.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "TRACE_CROSSWALK_REVIEW_METADATA_ONLY"
    assert_no_effect(audit)


def test_raw_input_policy_is_held_for_review() -> None:
    audit = audit_trace_crosswalk(event(), TracePolicy(include_input_value=True))
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "RAW_TRACE_CONTENT_EXPORT_REQUIRES_REVIEW"
    assert_no_effect(audit)


def test_raw_output_policy_is_held_for_review() -> None:
    audit = audit_trace_crosswalk(event(), TracePolicy(include_output_value=True))
    assert audit.status is AuditStatus.HOLD
    assert_no_effect(audit)


def test_tool_parameter_policy_is_held_for_review() -> None:
    audit = audit_trace_crosswalk(event(), TracePolicy(include_tool_parameters=True))
    assert audit.status is AuditStatus.HOLD
    assert_no_effect(audit)


def test_graph_self_parent_is_invalid() -> None:
    audit = audit_trace_crosswalk(event(graph_parent_id="node:1"))
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "GRAPH_SELF_PARENT"
    assert_no_effect(audit)


def test_blank_source_ref_is_invalid() -> None:
    audit = audit_trace_crosswalk(event(source_ref=" "))
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "SOURCE_REF_BLANK"
    assert_no_effect(audit)


def test_blank_approval_ref_is_invalid() -> None:
    audit = audit_trace_crosswalk(event(approval_ref=" "))
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "APPROVAL_REF_BLANK"
    assert_no_effect(audit)


def test_external_observation_import_is_review_only() -> None:
    audit = audit_trace_crosswalk(event(), external_attributes={"session.id": "external:1", "evaluation.score": 0.4, "vendor.extra": "retained"})
    assert audit.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert_no_effect(audit)


def test_external_aion_namespace_requires_review() -> None:
    audit = audit_trace_crosswalk(event(), external_attributes={"aion.subject_id": "subject:other"})
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "EXTERNAL_AION_NAMESPACE_REQUIRES_REVIEW"
    assert_no_effect(audit)


def test_external_invalid_score_is_invalid() -> None:
    audit = audit_trace_crosswalk(event(), external_attributes={"evaluation.score": "not-a-number"})
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "EXTERNAL_ATTRIBUTE_PARSE_INVALID"
    assert_no_effect(audit)


def test_external_out_of_range_score_is_invalid() -> None:
    audit = audit_trace_crosswalk(event(), external_attributes={"evaluation.score": 2.0})
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "EXTERNAL_ATTRIBUTE_PARSE_INVALID"
    assert_no_effect(audit)


def test_trace_batch_empty_is_held() -> None:
    audit = audit_event_batch(())
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "TRACE_BATCH_EMPTY"
    assert_no_effect(audit)


def test_trace_batch_duplicate_ids_are_invalid() -> None:
    audit = audit_event_batch((event("event:1"), event("event:1")))
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "DUPLICATE_RUNTIME_EVENT_ID"
    assert_no_effect(audit)


def test_trace_batch_is_review_metadata_only() -> None:
    audit = audit_event_batch((event("event:1"), event("event:2")))
    assert audit.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "TRACE_BATCH_REVIEW_METADATA_ONLY"
    assert_no_effect(audit)


def test_trace_constructor_rejects_canonical_effect() -> None:
    with pytest.raises(ValueError, match="canonical state"):
        event(canonical_effect="WRITE")


def test_valid_source_entry_is_review_metadata_only() -> None:
    audit = audit_source_entry(entry())
    assert audit.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "SOURCE_ENTRY_REVIEW_METADATA_ONLY"
    assert_no_effect(audit)


def test_source_entry_missing_attribution_is_invalid() -> None:
    audit = audit_source_entry(entry(where=""))
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "SOURCE_ATTRIBUTION_FIELD_MISSING"
    assert_no_effect(audit)


def test_source_entry_unknown_kind_is_invalid() -> None:
    audit = audit_source_entry(entry(source_kind="Unknown Actor"))
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "SOURCE_KIND_UNCONTROLLED"
    assert_no_effect(audit)


def test_source_entry_unknown_currentness_is_invalid() -> None:
    audit = audit_source_entry(entry(currentness="FRESH"))
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "CURRENTNESS_UNCONTROLLED"
    assert_no_effect(audit)


def test_reused_reference_cannot_be_new_evidence() -> None:
    audit = audit_source_entry(entry(new_evidence_claimed=True))
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "REUSED_REFERENCE_MISLABELED_AS_NEW_EVIDENCE"
    assert_no_effect(audit)


def test_stale_source_requires_review() -> None:
    audit = audit_source_entry(entry(currentness="STALE"))
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "SOURCE_CURRENTNESS_REQUIRES_REVIEW"
    assert_no_effect(audit)


def test_empty_crosswalk_is_held() -> None:
    audit = audit_source_entries(())
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "CROSSWALK_EMPTY"
    assert_no_effect(audit)


def test_duplicate_crosswalk_ids_are_invalid() -> None:
    audit = audit_source_entries((entry(), entry()))
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "DUPLICATE_CROSSWALK_ENTRY_ID"
    assert_no_effect(audit)


def test_missing_source_ref_is_invalid() -> None:
    audit = audit_source_entries((entry(source_ref=""),))
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "SOURCE_REF_MISSING"
    assert_no_effect(audit)


def test_crosswalk_with_stale_entry_is_held() -> None:
    audit = audit_source_entries((entry(currentness="HISTORICAL"),))
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "CROSSWALK_CURRENTNESS_REQUIRES_REVIEW"
    assert_no_effect(audit)


def test_valid_crosswalk_is_review_metadata_only() -> None:
    audit = audit_source_entries((entry(), entry("entry:2", target_field="agent.name")))
    assert audit.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "CROSSWALK_REVIEW_METADATA_ONLY"
    assert_no_effect(audit)
