from datetime import datetime, timezone

import pytest

from aion_external_evidence import EvidenceDecision, ExecutionMode, ExternalEvidenceReport
from aion_external_evidence_adversarial import AuditStatus, audit_external_evidence_report

BRANCH = "review/four-domain-research-materialization"
BASELINE = "a" * 40
INPUT = "1" * 64
OUTPUT = "2" * 64


def report(**overrides) -> ExternalEvidenceReport:
    data = dict(
        report_id="EXT-ADV-1",
        runner_id="external-runner",
        actor_kind="AI",
        branch=BRANCH,
        baseline_commit=BASELINE,
        observed_at=datetime(2026, 8, 13, tzinfo=timezone.utc),
        execution_mode=ExecutionMode.STATIC_REVIEW,
        module_refs=("research-labs/evidence-responsive-governance-reassessment_v0.1.0",),
        fixture_refs=(),
        environment_fingerprint="env:public-read-only",
        network_mode="PUBLIC_WEB",
        benchmark_access_policy="PUBLIC_REPOSITORY_READ",
        claimed_result="REVIEW_ONLY",
    )
    data.update(overrides)
    return ExternalEvidenceReport(**data)


def complete_executed(**overrides) -> ExternalEvidenceReport:
    data = dict(
        execution_mode=ExecutionMode.EXECUTED_REPLICATION,
        fixture_refs=("fixture://run-1",),
        evidence_refs=("evidence://run-1",),
        search_trace_refs=("search://trace-1",),
        input_hash=INPUT,
        output_hash=OUTPUT,
        claimed_result="PASS",
    )
    data.update(overrides)
    return report(**data)


def assert_no_effect(audit) -> None:
    assert audit.canonical_effect == "NONE"
    assert audit.governance_effect == "NONE"
    assert audit.deployment is False
    assert audit.scientific_conclusion == "NOT_ESTABLISHED"
    assert audit.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_static_review_admitted_for_review_only() -> None:
    audit = audit_external_evidence_report(report(), expected_branch=BRANCH)
    assert audit.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "EXTERNAL_EVIDENCE_ADMITTED_FOR_REVIEW_ONLY"
    assert audit.normalized_decision is EvidenceDecision.ACCEPT_STATIC_REVIEW
    assert audit.replication_eligible is False
    assert_no_effect(audit)


def test_logical_reproduction_is_not_replication() -> None:
    audit = audit_external_evidence_report(report(execution_mode=ExecutionMode.LOGICAL_REPRODUCTION, claimed_result="DESIGN_CONFORMANCE_SUPPORTED"), expected_branch=BRANCH)
    assert audit.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.normalized_decision is EvidenceDecision.ACCEPT_LOGICAL_REPRODUCTION
    assert audit.replication_eligible is False
    assert_no_effect(audit)


def test_complete_execution_requires_observation_flag() -> None:
    audit = audit_external_evidence_report(complete_executed(), expected_branch=BRANCH)
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "EXECUTED_RESULT_CLAIM_WITHOUT_OBSERVATION"
    assert audit.normalized_decision is EvidenceDecision.ACCEPT_EXECUTED_REPLICATION
    assert_no_effect(audit)


def test_complete_execution_with_observation_is_review_admissible_only() -> None:
    audit = audit_external_evidence_report(complete_executed(), expected_branch=BRANCH, result_observed=True)
    assert audit.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.replication_eligible is True
    assert_no_effect(audit)


def test_duplicate_report_id_is_invalid() -> None:
    audit = audit_external_evidence_report(report(), expected_branch=BRANCH, known_report_ids=("EXT-ADV-1",))
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "DUPLICATE_REPORT_ID"
    assert_no_effect(audit)


def test_expected_branch_is_required() -> None:
    audit = audit_external_evidence_report(report(), expected_branch="")
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "EXPECTED_BRANCH_MISSING"
    assert_no_effect(audit)


def test_branch_scope_mismatch_holds() -> None:
    audit = audit_external_evidence_report(report(branch="review/other"), expected_branch=BRANCH)
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "BRANCH_SCOPE_MISMATCH"
    assert_no_effect(audit)


def test_main_branch_evidence_is_blocked() -> None:
    audit = audit_external_evidence_report(report(branch="main"), expected_branch="main")
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "MAIN_BRANCH_RESEARCH_EVIDENCE_BLOCKED"
    assert_no_effect(audit)


def test_unresolved_actor_holds() -> None:
    audit = audit_external_evidence_report(report(actor_kind="UNKNOWN"), expected_branch=BRANCH)
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "ACTOR_IDENTITY_UNRESOLVED"
    assert_no_effect(audit)


def test_unknown_mode_with_digest_is_held() -> None:
    audit = audit_external_evidence_report(report(execution_mode=ExecutionMode.UNKNOWN, input_hash=INPUT), expected_branch=BRANCH)
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "UNKNOWN_MODE_CANNOT_CARRY_EXECUTION_DIGESTS"
    assert_no_effect(audit)


def test_unknown_mode_without_digest_uses_base_hold() -> None:
    audit = audit_external_evidence_report(report(execution_mode=ExecutionMode.UNKNOWN), expected_branch=BRANCH)
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "BASE_NORMALIZER_REQUIRES_PROVENANCE"
    assert audit.normalized_decision is EvidenceDecision.HOLD_INCOMPLETE_PROVENANCE
    assert_no_effect(audit)


def test_executed_claim_must_not_be_empty() -> None:
    audit = audit_external_evidence_report(complete_executed(claimed_result=""), expected_branch=BRANCH, result_observed=True)
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "EXECUTED_REPLICATION_RESULT_CLAIM_MISSING"
    assert_no_effect(audit)


def test_static_observation_exceeds_declared_mode() -> None:
    audit = audit_external_evidence_report(report(), expected_branch=BRANCH, result_observed=True)
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "RESULT_OBSERVATION_EXCEEDS_DECLARED_EXECUTION_MODE"
    assert_no_effect(audit)


def test_static_pass_hash_claim_is_rejected_by_base_normalizer() -> None:
    audit = audit_external_evidence_report(report(output_hash=OUTPUT, claimed_result="PASS"), expected_branch=BRANCH)
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "BASE_NORMALIZER_REJECTED_CLAIM"
    assert audit.normalized_decision is EvidenceDecision.REJECT_INCONSISTENT_CLAIM
    assert_no_effect(audit)


def test_constructor_rejects_canonical_effect() -> None:
    with pytest.raises(ValueError):
        report(canonical_effect="PROMOTE")


def test_constructor_rejects_non_sha_baseline() -> None:
    with pytest.raises(ValueError):
        report(baseline_commit="current-main")
