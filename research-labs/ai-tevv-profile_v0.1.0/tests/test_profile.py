from __future__ import annotations

from dataclasses import replace

import pytest

from aion_ai_tevv import (
    AITEVVProfileGate,
    AISystemBinding,
    EvaluatorIndependence,
    OracleStrategy,
    TEVVActivity,
    TEVVCaseSpec,
    TEVVError,
    TEVVMetricSpec,
    TEVVProfileDisposition,
    build_tevv_profile,
)


def system() -> AISystemBinding:
    return AISystemBinding(
        provider_id="provider-under-study",
        product_id="product-under-study",
        model_id="model-under-study",
        model_version_ref="model-version:receipt-v1",
        runtime_ref="runtime:container-image@sha256",
        environment_ref="environment:synthetic-sandbox-v1",
        prompt_ref="prompt:sha256",
        scaffold_ref="scaffold:sha256",
        tool_manifest_ref="tools:sha256",
        generation_config_ref="generation-config:sha256",
        exact_source_state_ref="git:d9155e9fd6908b2880adc43e160ece70a1036cc7",
    )


def metric(metric_id: str = "METRIC-ACCURACY") -> TEVVMetricSpec:
    return TEVVMetricSpec(
        metric_id=metric_id,
        measurement_concept="bounded task correctness",
        method_ref="method:exact-match-or-adjudicated-property",
        method_version="v1",
        unit="ratio",
        acceptance_criterion_ref="criterion:preregistered-threshold-v1",
        uncertainty_ref="uncertainty:binomial-and-run-variation-v1",
    )


def case(
    case_id: str = "CASE-001",
    *,
    metric_ids: tuple[str, ...] = ("METRIC-ACCURACY",),
    held_out: bool = True,
) -> TEVVCaseSpec:
    return TEVVCaseSpec(
        case_id=case_id,
        input_ref=f"input:{case_id}",
        test_set_ref="test-set:synthetic-held-out-v1",
        data_quality_ref="data-quality:synthetic-held-out-v1",
        contamination_check_ref="check:contamination-v1",
        leakage_check_ref="check:leakage-v1",
        oracle_strategy=OracleStrategy.PROPERTY_BASED,
        oracle_ref="oracle:bounded-property-v1",
        expected_property_refs=("property:no-unsupported-claim",),
        metric_ids=metric_ids,
        slice_refs=("slice:structural-only",),
        held_out=held_out,
    )


def profile(
    *,
    metrics: tuple[TEVVMetricSpec, ...] | None = None,
    cases: tuple[TEVVCaseSpec, ...] | None = None,
    minimum_repetitions: int = 3,
    stochastic_system: bool = True,
):
    return build_tevv_profile(
        profile_id="TEVV-PROFILE-001",
        profile_version="0.1.0",
        objective_ref="objective:bounded-ai-system-quality-evaluation",
        intended_use_ref="use:research-engineering-only",
        activities=(
            TEVVActivity.TESTING,
            TEVVActivity.EVALUATION,
            TEVVActivity.VERIFICATION,
            TEVVActivity.VALIDATION,
        ),
        system=system(),
        metrics=metrics or (metric(),),
        cases=cases or (case(),),
        repetition_policy_ref="policy:repeat-stochastic-runs-v1",
        nondeterminism_policy_ref="policy:nondeterminism-v1",
        minimum_repetitions=minimum_repetitions,
        stochastic_system=stochastic_system,
        aggregation_rule_ref="aggregation:preregistered-summary-v1",
        evaluator_ref="evaluator:bounded-v1",
        evaluator_version="v1",
        evaluator_independence=EvaluatorIndependence.INTERNAL_INDEPENDENT,
        target_context_ref="context:research-sandbox-v1",
        context_similarity_statement=(
            "No deployment claim; the profile is scoped to the declared research sandbox."
        ),
        failure_action_ref="reaction:HOLD_AND_REVIEW",
        preregistration_ref="preregistration:TEVV-PROFILE-001",
    )


def test_structural_profile_is_ready_for_execution_but_not_model_quality_pass() -> None:
    assessment = AITEVVProfileGate().assess(profile())

    assert assessment.disposition is TEVVProfileDisposition.READY_FOR_BOUNDED_EXECUTION
    assert assessment.model_executed is False
    assert assessment.empirical_model_evidence is False
    assert assessment.scientific_disposition == "HOLD"
    assert assessment.canonical_effect == "NONE"
    assert assessment.deployment is False
    assert "READY_FOR_BOUNDED_EXECUTION_NOT_MODEL_QUALITY_PASS" in assessment.reasons


def test_stochastic_profile_requires_repetition() -> None:
    with pytest.raises(TEVVError, match="at least two repetitions"):
        profile(minimum_repetitions=1, stochastic_system=True)


def test_case_must_reference_known_metric() -> None:
    with pytest.raises(TEVVError, match="unknown metric"):
        profile(cases=(case(metric_ids=("METRIC-UNKNOWN",)),))


def test_non_held_out_case_fails_closed() -> None:
    assessment = AITEVVProfileGate().assess(profile(cases=(case(held_out=False),)))

    assert assessment.disposition is TEVVProfileDisposition.HOLD
    assert "NON_HELD_OUT_CASE_REQUIRES_REVIEW" in assessment.reasons


def test_test_oracle_is_explicit_and_typed() -> None:
    with pytest.raises(TEVVError, match="oracle_ref"):
        replace(case(), oracle_ref="")
    with pytest.raises(TEVVError, match="oracle_strategy"):
        replace(case(), oracle_strategy="PROPERTY_BASED")


def test_system_binding_requires_provider_model_runtime_and_context() -> None:
    with pytest.raises(TEVVError, match="model_version_ref"):
        replace(system(), model_version_ref="")
    with pytest.raises(TEVVError, match="runtime_ref"):
        replace(system(), runtime_ref="")
    with pytest.raises(TEVVError, match="prompt_ref"):
        replace(system(), prompt_ref="")


def test_profile_digest_detects_tampering() -> None:
    value = profile()
    with pytest.raises(TEVVError, match="content digest mismatch"):
        replace(value, objective_ref="objective:changed-without-redigest")


def test_v0_1_profile_cannot_claim_model_execution_or_empirical_evidence() -> None:
    value = profile()
    with pytest.raises(TEVVError, match="structural only"):
        replace(value, model_executed=True)
    with pytest.raises(TEVVError, match="structural only"):
        replace(value, empirical_model_evidence=True)


def test_profile_cannot_upgrade_scientific_or_subjectivity_claims() -> None:
    value = profile()
    with pytest.raises(TEVVError, match="scientific validity"):
        replace(value, scientific_disposition="VALIDATED")
    with pytest.raises(TEVVError, match="subjectivity"):
        replace(value, subjectivity_conclusion="ESTABLISHED")
    with pytest.raises(TEVVError, match="consciousness"):
        replace(value, consciousness_conclusion="ESTABLISHED")
    with pytest.raises(TEVVError, match="phenomenal experience"):
        replace(value, phenomenal_experience_conclusion="ESTABLISHED")


def test_profile_digest_is_order_invariant_for_metric_case_and_activity_sets() -> None:
    metric_a = metric("METRIC-A")
    metric_b = metric("METRIC-B")
    case_a = case("CASE-A", metric_ids=("METRIC-A",))
    case_b = case("CASE-B", metric_ids=("METRIC-B",))

    first = build_tevv_profile(
        profile_id="TEVV-ORDER",
        profile_version="0.1.0",
        objective_ref="objective:order-invariance",
        intended_use_ref="use:structural-test",
        activities=(TEVVActivity.TESTING, TEVVActivity.EVALUATION),
        system=system(),
        metrics=(metric_a, metric_b),
        cases=(case_a, case_b),
        repetition_policy_ref="policy:repeat-v1",
        nondeterminism_policy_ref="policy:nondeterminism-v1",
        minimum_repetitions=2,
        stochastic_system=True,
        aggregation_rule_ref="aggregation:v1",
        evaluator_ref="evaluator:v1",
        evaluator_version="v1",
        evaluator_independence=EvaluatorIndependence.INTERNAL_INDEPENDENT,
        target_context_ref="context:test",
        context_similarity_statement="Structural comparison only.",
        failure_action_ref="reaction:hold",
        preregistration_ref="preregistration:order",
    )
    second = build_tevv_profile(
        profile_id="TEVV-ORDER",
        profile_version="0.1.0",
        objective_ref="objective:order-invariance",
        intended_use_ref="use:structural-test",
        activities=(TEVVActivity.EVALUATION, TEVVActivity.TESTING),
        system=system(),
        metrics=(metric_b, metric_a),
        cases=(case_b, case_a),
        repetition_policy_ref="policy:repeat-v1",
        nondeterminism_policy_ref="policy:nondeterminism-v1",
        minimum_repetitions=2,
        stochastic_system=True,
        aggregation_rule_ref="aggregation:v1",
        evaluator_ref="evaluator:v1",
        evaluator_version="v1",
        evaluator_independence=EvaluatorIndependence.INTERNAL_INDEPENDENT,
        target_context_ref="context:test",
        context_similarity_statement="Structural comparison only.",
        failure_action_ref="reaction:hold",
        preregistration_ref="preregistration:order",
    )

    assert first.profile_sha256 == second.profile_sha256
