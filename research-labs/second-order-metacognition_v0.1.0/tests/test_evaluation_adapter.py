from __future__ import annotations

from aion_second_order import (
    ConditionVerificationDiagnostics,
    SecondOrderCondition,
    VerificationDiagnostics,
    VerificationInterventionCondition,
    adapt_intervention_experiment,
    adapt_matched_experiment,
    run_matched_experiment,
    run_matched_intervention_experiment,
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
    scoped = ConditionVerificationDiagnostics(
        condition=SecondOrderCondition.MONITOR_PLUS_CONTROL,
        diagnostics=diagnostics(),
        run_ref="run:monitor-plus-control",
        provenance_refs=("fixture:adapter-condition",),
    )
    artifact = adapt_matched_experiment(
        run_matched_experiment(),
        verification_threshold=0.75,
        verification_diagnostics_by_condition={
            SecondOrderCondition.MONITOR_PLUS_CONTROL: scoped,
        },
        experiment_level_diagnostics=diagnostics(),
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
        if output["condition"] == SecondOrderCondition.MONITOR_PLUS_CONTROL.value:
            assert output["verification_attempts"] == 4
            assert output["verification_evidence_rejected"] == 1
            assert output["verification_scope_rejections"] == 1
            assert output["verification_diagnostics_status"] == "PROVIDED"
            assert output["verification_run_ref"] == "run:monitor-plus-control"
        else:
            assert output["verification_attempts"] is None
            assert output["verification_evidence_rejected"] is None
            assert output["verification_scope_rejections"] is None
            assert output["verification_diagnostics_status"] == "NOT_PROVIDED"
            assert output["verification_run_ref"] is None
    assert artifact.experiment_level_diagnostics == diagnostics()


def test_equal_values_still_preserve_distinct_condition_provenance():
    first = ConditionVerificationDiagnostics(
        SecondOrderCondition.MONITOR_PLUS_CONTROL,
        diagnostics(),
        "run:control",
        ("fixture:control",),
    )
    second = ConditionVerificationDiagnostics(
        SecondOrderCondition.MONITOR_ONLY,
        diagnostics(),
        "run:monitor-only",
        ("fixture:monitor-only",),
    )
    artifact = adapt_matched_experiment(
        run_matched_experiment(),
        verification_threshold=0.75,
        verification_diagnostics_by_condition={
            first.condition: first,
            second.condition: second,
        },
    )
    by_condition = {case.output["condition"]: case.output for case in artifact.report.cases}
    assert by_condition[first.condition.value]["verification_run_ref"] == "run:control"
    assert by_condition[second.condition.value]["verification_run_ref"] == "run:monitor-only"
    assert by_condition[first.condition.value]["verification_provenance_refs"] != by_condition[second.condition.value]["verification_provenance_refs"]


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


def test_intervention_adapter_keeps_diagnostics_condition_local():
    source = run_matched_intervention_experiment()
    artifact = adapt_intervention_experiment(source, verification_threshold=0.75)
    assert len(artifact.report.cases) == len(VerificationInterventionCondition)
    source_by_condition = {item.condition.value: item for item in source.conditions}
    for case in artifact.report.cases:
        local = source_by_condition[case.output["condition"]]
        assert case.output["run_ref"] == local.run_ref
        assert case.output["provenance_refs"] == local.provenance_refs
        assert case.output["verification_attempts"] == local.verification_diagnostics.verification_attempts
        assert case.output["intervention_opportunities"] == local.intervention_diagnostics.intervention_opportunities
        assert case.output["interventions_applied"] == local.intervention_diagnostics.interventions_applied
        assert case.metadata["condition_local"] is True


def test_intervention_adapter_pass_rate_does_not_establish_benefit():
    artifact = adapt_intervention_experiment(
        run_matched_intervention_experiment(),
        verification_threshold=0.75,
    )
    assert artifact.report.pass_rate == 1.0
    assert artifact.interpretation == "RESEARCH_EVIDENCE_ONLY"
    assert artifact.functional_contribution_status == "NOT_ESTABLISHED"
    assert artifact.verification_benefit == "NOT_ESTABLISHED"
    assert artifact.subjectivity_claim_disposition == "DENY_PROMOTION"
    assert artifact.consciousness_claim_disposition == "DENY_PROMOTION"
