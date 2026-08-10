from datetime import datetime, timezone
import hashlib
import pytest

from aion_external_evidence import (
    EvidenceDecision,
    ExecutionMode,
    ExternalEvidenceReport,
    normalize_external_report,
)

NOW = datetime(2026, 8, 10, 0, 0, tzinfo=timezone.utc)
BASELINE = "a3ab63671c92d5b29c81b1ef23a5fe65cc246074"
INPUT = hashlib.sha256(b"input").hexdigest()
OUTPUT = hashlib.sha256(b"output").hexdigest()


def report(**overrides):
    data = dict(
        report_id="EXT-1",
        runner_id="external-ai",
        actor_kind="AI",
        branch="review/four-domain-research-materialization",
        baseline_commit=BASELINE,
        observed_at=NOW,
        execution_mode=ExecutionMode.STATIC_REVIEW,
        module_refs=("research-labs/four-domain-p5-hypothesis-convergence_v0.1.0",),
        fixture_refs=(),
        environment_fingerprint="web-read-only",
        network_mode="PUBLIC_WEB",
        benchmark_access_policy="PUBLIC_REPOSITORY_READ",
        claimed_result="SUPPORTED_FOR_REVIEWED_SCOPE",
    )
    data.update(overrides)
    return ExternalEvidenceReport(**data)


def test_static_review_is_accepted_but_not_replication_eligible():
    normalized = normalize_external_report(report())
    assert normalized.decision is EvidenceDecision.ACCEPT_STATIC_REVIEW
    assert normalized.replication_eligible is False
    assert normalized.provenance_complete is True


def test_logical_reproduction_is_preserved_without_replication_promotion():
    normalized = normalize_external_report(
        report(execution_mode=ExecutionMode.LOGICAL_REPRODUCTION, claimed_result="DESIGN_CONFORMANCE_SUPPORTED")
    )
    assert normalized.decision is EvidenceDecision.ACCEPT_LOGICAL_REPRODUCTION
    assert normalized.replication_eligible is False


def test_executed_replication_requires_real_hashes_fixtures_and_evidence():
    normalized = normalize_external_report(
        report(
            execution_mode=ExecutionMode.EXECUTED_REPLICATION,
            input_hash="sha256:descriptor",
            output_hash="sha256:pass",
            claimed_result="PASS",
        )
    )
    assert normalized.decision is EvidenceDecision.HOLD_INCOMPLETE_PROVENANCE
    assert "EXECUTED_REPLICATION_REQUIRES_INPUT_SHA256" in normalized.reasons
    assert "EXECUTED_REPLICATION_REQUIRES_OUTPUT_SHA256" in normalized.reasons
    assert "EXECUTED_REPLICATION_REQUIRES_FIXTURE_REFS" in normalized.reasons
    assert "EXECUTED_REPLICATION_REQUIRES_EVIDENCE_REFS" in normalized.reasons


def test_public_web_executed_replication_requires_search_trace():
    normalized = normalize_external_report(
        report(
            execution_mode=ExecutionMode.EXECUTED_REPLICATION,
            fixture_refs=("fixture://public",),
            evidence_refs=("evidence://run-log",),
            input_hash=INPUT,
            output_hash=OUTPUT,
            claimed_result="PASS",
        )
    )
    assert normalized.decision is EvidenceDecision.HOLD_INCOMPLETE_PROVENANCE
    assert normalized.reasons == ("PUBLIC_WEB_EXECUTION_REQUIRES_SEARCH_TRACE_REFS",)


def test_complete_executed_replication_becomes_registry_eligible_candidate():
    normalized = normalize_external_report(
        report(
            execution_mode=ExecutionMode.EXECUTED_REPLICATION,
            fixture_refs=("fixture://public",),
            evidence_refs=("evidence://run-log",),
            search_trace_refs=("search://trace-1",),
            input_hash=INPUT,
            output_hash=OUTPUT,
            claimed_result="PASS",
        )
    )
    assert normalized.decision is EvidenceDecision.ACCEPT_EXECUTED_REPLICATION
    assert normalized.replication_eligible is True
    assert normalized.provenance_complete is True


def test_static_review_cannot_masquerade_as_execution_using_pass_hash():
    normalized = normalize_external_report(
        report(input_hash=INPUT, output_hash=OUTPUT, claimed_result="PASS")
    )
    assert normalized.decision is EvidenceDecision.REJECT_INCONSISTENT_CLAIM
    assert normalized.replication_eligible is False
    assert normalized.reasons == ("STATIC_REVIEW_MUST_NOT_MASQUERADE_AS_EXECUTED_REPLICATION",)


def test_main_or_canonical_effect_claims_fail_closed():
    with pytest.raises(ValueError):
        report(main_effect="WRITE")
    with pytest.raises(ValueError):
        report(canonical_effect="PROMOTE")


def test_baseline_commit_must_be_exact_git_sha():
    with pytest.raises(ValueError):
        report(baseline_commit="current-main")
