from __future__ import annotations

from aion_second_order import (
    VerificationDiagnostics,
    adapt_matched_experiment,
    run_matched_experiment,
)


def diagnostics() -> VerificationDiagnostics:
    return VerificationDiagnostics(
        verification_requests=4,
        verification_attempts=4,
        verification_evidence_available=1,
        verification_evidence_unavailable=1,
        verification_evidence_ambiguous=1,
        verification_evidence_rejected=1,
        verification_scope_rejections=1,
        oracle_leakage_rejections=0,
    )


def test_adapter_reuses_generic_experiment_report_and_preserves_raw_fields():
    artifact = adapt_matched_experiment(
        run_matched_experiment(),
        verification_threshold=0.75,
        verification_diagnostics=diagnostics(),
    )
    assert artifact.report.dataset_name == "second-order-matched-threshold-0.75"
    assert artifact.report.research_only is True
    assert artifact.report.canonical_effect == "NONE"
    assert len(artifact.report.cases) == 5
    for case in artifact.report.cases:
        output = case.output
        assert output["trial_count"] == case.metadata["raw_denominator"]
        assert output["observed_sample_size"] <= output["trial_count"]
        assert "missing_outcomes" in output
        assert "monitor_coverage" in output
        assert "verification_requests" in output
        assert output["verification_attempts"] == 4
        assert output["verification_evidence_rejected"] == 1
        assert output["verification_scope_rejections"] == 1


def test_claim_boundary_denies_subjectivity_and_consciousness_promotion():
    artifact = adapt_matched_experiment(
        run_matched_experiment(),
        verification_threshold=0.75,
    )
    assert artifact.subjectivity_claim_disposition == "DENY_PROMOTION"
    assert artifact.consciousness_claim_disposition == "DENY_PROMOTION"
    assert artifact.canonical_effect == "NONE"


def test_perfect_adapter_pass_rate_is_not_scientific_proof():
    artifact = adapt_matched_experiment(
        run_matched_experiment(),
        verification_threshold=0.75,
    )
    assert artifact.report.pass_rate == 1.0
    assert artifact.interpretation == "RESEARCH_EVIDENCE_ONLY"
    assert artifact.functional_contribution_status == "NOT_ESTABLISHED"
    assert artifact.threshold_scientific_result == "NOT_ESTABLISHED"


def test_adapter_does_not_rank_or_select_thresholds():
    first = adapt_matched_experiment(run_matched_experiment(), verification_threshold=0.50)
    second = adapt_matched_experiment(run_matched_experiment(), verification_threshold=0.90)
    assert first.requested_threshold == 0.50
    assert second.requested_threshold == 0.90
    assert first.report.dataset_name != second.report.dataset_name
    assert first.threshold_scientific_result == second.threshold_scientific_result == "NOT_ESTABLISHED"
