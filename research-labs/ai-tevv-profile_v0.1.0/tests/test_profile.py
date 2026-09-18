from __future__ import annotations

from dataclasses import replace

import pytest

from aion_ai_tevv import (
    AITEVVProfileGate,
    AISystemBinding,
    EvaluatorIndependence,
    OracleStrategy,
    TEVVActivity,
    TEVVLifecycleStage,
    TEVVCaseSpec,
    TEVVError,
    TEVVMetricSpec,
    TEVVProfileDisposition,
    TEVVTestApproach,
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
        exact_source_state_ref="git:3953f70c0a37e44da95f412143876e1c753fee76",
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
        risk_refs=("risk:bounded-model-quality",),
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
        scenario_ref="scenario:bounded-research-task-v1",
        test_environment_ref="test-environment:synthetic-sandbox-v1",
        test_approach=TEVVTestApproach.BLACK_BOX,
        oracle_strategy=OracleStrategy.PROPERTY_BASED,
        oracle_ref="oracle:bounded-property-v1",
        oracle_qualification_ref="NOT_APPLICABLE",
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
        tevv_vocabulary_ref="subjectivity-pipeline:TevvDefinition:v0.1.0",
        tevv_vocabulary_sha256="a" * 64,
        lifecycle_stage=TEVVLifecycleStage.RESEARCH,
        risk_refs=("risk:bounded-model-quality",),
        activities=(
            TEVVActivity.TEST,
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
        tevv_toolchain_ref="tevv-toolchain:pytest-plus-adjudication-v1",
        tevv_toolchain_version="v1",
        verification_requirement_refs=("requirement:bounded-system-contract-v1",),
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
        tevv_vocabulary_ref="subjectivity-pipeline:TevvDefinition:v0.1.0",
        tevv_vocabulary_sha256="a" * 64,
        lifecycle_stage=TEVVLifecycleStage.RESEARCH,
        risk_refs=("risk:bounded-model-quality",),
        activities=(TEVVActivity.TEST, TEVVActivity.EVALUATION),
        system=system(),
        metrics=(metric_a, metric_b),
        cases=(case_a, case_b),
        repetition_policy_ref="policy:repeat-v1",
        nondeterminism_policy_ref="policy:nondeterminism-v1",
        minimum_repetitions=2,
        stochastic_system=True,
        aggregation_rule_ref="aggregation:v1",
        tevv_toolchain_ref="tevv-toolchain:test-v1",
        tevv_toolchain_version="v1",
        verification_requirement_refs=(),
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
        tevv_vocabulary_ref="subjectivity-pipeline:TevvDefinition:v0.1.0",
        tevv_vocabulary_sha256="a" * 64,
        lifecycle_stage=TEVVLifecycleStage.RESEARCH,
        risk_refs=("risk:bounded-model-quality",),
        activities=(TEVVActivity.EVALUATION, TEVVActivity.TEST),
        system=system(),
        metrics=(metric_b, metric_a),
        cases=(case_b, case_a),
        repetition_policy_ref="policy:repeat-v1",
        nondeterminism_policy_ref="policy:nondeterminism-v1",
        minimum_repetitions=2,
        stochastic_system=True,
        aggregation_rule_ref="aggregation:v1",
        tevv_toolchain_ref="tevv-toolchain:test-v1",
        tevv_toolchain_version="v1",
        verification_requirement_refs=(),
        evaluator_ref="evaluator:v1",
        evaluator_version="v1",
        evaluator_independence=EvaluatorIndependence.INTERNAL_INDEPENDENT,
        target_context_ref="context:test",
        context_similarity_statement="Structural comparison only.",
        failure_action_ref="reaction:hold",
        preregistration_ref="preregistration:order",
    )

    assert first.profile_sha256 == second.profile_sha256



def test_case_requires_explicit_scenario_environment_and_test_approach() -> None:
    with pytest.raises(TEVVError, match="scenario_ref"):
        replace(case(), scenario_ref="")
    with pytest.raises(TEVVError, match="test_environment_ref"):
        replace(case(), test_environment_ref="")
    with pytest.raises(TEVVError, match="test_approach"):
        replace(case(), test_approach="BLACK_BOX")


def test_human_or_composite_oracle_requires_qualification_provenance() -> None:
    with pytest.raises(TEVVError, match="oracle qualification provenance"):
        replace(
            case(),
            oracle_strategy=OracleStrategy.HUMAN_ADJUDICATION,
            oracle_qualification_ref="NOT_APPLICABLE",
        )


def test_verification_activity_requires_requirement_traceability() -> None:
    value = profile()
    with pytest.raises(TEVVError, match="verification activity requires requirement references"):
        replace(value, verification_requirement_refs=())


def test_tevv_toolchain_identity_and_version_are_required() -> None:
    value = profile()
    with pytest.raises(TEVVError, match="tevv_toolchain_ref"):
        replace(value, tevv_toolchain_ref="")
    with pytest.raises(TEVVError, match="tevv_toolchain_version"):
        replace(value, tevv_toolchain_version="")


def test_profile_rejects_unsupported_schema_version() -> None:
    value = profile()
    with pytest.raises(TEVVError, match="unsupported TEVV profile schema version"):
        replace(value, schema_version="9.9.9")


def test_case_reference_sets_are_digest_order_invariant() -> None:
    metric_a = metric("METRIC-A")
    metric_b = metric("METRIC-B")
    first_case = TEVVCaseSpec(
        case_id="CASE-ORDER",
        input_ref="input:order",
        test_set_ref="test-set:order",
        data_quality_ref="data-quality:order",
        contamination_check_ref="check:contamination",
        leakage_check_ref="check:leakage",
        scenario_ref="scenario:case-order",
        test_environment_ref="test-environment:case-order",
        test_approach=TEVVTestApproach.HYBRID,
        oracle_strategy=OracleStrategy.COMPOSITE,
        oracle_ref="oracle:composite",
        oracle_qualification_ref="qualification:composite-oracle-v1",
        expected_property_refs=("property:a", "property:b"),
        metric_ids=("METRIC-A", "METRIC-B"),
        slice_refs=("slice:a", "slice:b"),
        held_out=True,
    )
    second_case = replace(
        first_case,
        expected_property_refs=("property:b", "property:a"),
        metric_ids=("METRIC-B", "METRIC-A"),
        slice_refs=("slice:b", "slice:a"),
    )

    common = {
        "profile_id": "TEVV-CASE-ORDER",
        "profile_version": "0.1.0",
        "objective_ref": "objective:case-order",
        "intended_use_ref": "use:structural-test",
        "tevv_vocabulary_ref": "subjectivity-pipeline:TevvDefinition:v0.1.0",
        "tevv_vocabulary_sha256": "a" * 64,
        "lifecycle_stage": TEVVLifecycleStage.RESEARCH,
        "risk_refs": ("risk:bounded-model-quality",),
        "activities": (TEVVActivity.TEST,),
        "system": system(),
        "metrics": (metric_a, metric_b),
        "repetition_policy_ref": "policy:repeat-v1",
        "nondeterminism_policy_ref": "policy:nondeterminism-v1",
        "minimum_repetitions": 1,
        "stochastic_system": False,
        "aggregation_rule_ref": "aggregation:v1",
        "tevv_toolchain_ref": "tevv-toolchain:test-v1",
        "tevv_toolchain_version": "v1",
        "verification_requirement_refs": (),
        "evaluator_ref": "evaluator:v1",
        "evaluator_version": "v1",
        "evaluator_independence": EvaluatorIndependence.NON_INDEPENDENT,
        "target_context_ref": "context:test",
        "context_similarity_statement": "Structural comparison only.",
        "failure_action_ref": "reaction:hold",
        "preregistration_ref": "preregistration:case-order",
    }
    first = build_tevv_profile(cases=(first_case,), **common)
    second = build_tevv_profile(cases=(second_case,), **common)
    assert first.profile_sha256 == second.profile_sha256



def test_profile_binds_lifecycle_stage_and_metric_risks() -> None:
    value = profile()
    assert value.lifecycle_stage is TEVVLifecycleStage.RESEARCH
    assert value.risk_refs == ("risk:bounded-model-quality",)

    with pytest.raises(TEVVError, match="lifecycle_stage"):
        replace(value, lifecycle_stage="RESEARCH")

    outside_risk_metric = replace(
        metric(),
        risk_refs=("risk:not-declared-by-profile",),
    )
    with pytest.raises(TEVVError, match="outside profile risk_refs"):
        profile(metrics=(outside_risk_metric,))


def test_non_independent_evaluator_holds_execution_readiness() -> None:
    value = build_tevv_profile(
        profile_id="TEVV-NON-INDEPENDENT",
        profile_version="0.1.0",
        objective_ref="objective:independence-check",
        intended_use_ref="use:structural-test",
        tevv_vocabulary_ref="subjectivity-pipeline:TevvDefinition:v0.1.0",
        tevv_vocabulary_sha256="a" * 64,
        lifecycle_stage=TEVVLifecycleStage.RESEARCH,
        risk_refs=("risk:bounded-model-quality",),
        activities=(TEVVActivity.TEST,),
        system=system(),
        metrics=(metric(),),
        cases=(case(),),
        repetition_policy_ref="policy:repeat-v1",
        nondeterminism_policy_ref="policy:nondeterminism-v1",
        minimum_repetitions=1,
        stochastic_system=False,
        aggregation_rule_ref="aggregation:v1",
        tevv_toolchain_ref="tevv-toolchain:test-v1",
        tevv_toolchain_version="v1",
        verification_requirement_refs=(),
        evaluator_ref="evaluator:developer-self-review",
        evaluator_version="v1",
        evaluator_independence=EvaluatorIndependence.NON_INDEPENDENT,
        target_context_ref="context:test",
        context_similarity_statement="Structural test only.",
        failure_action_ref="reaction:hold",
        preregistration_ref="preregistration:non-independent",
    )
    assessment = AITEVVProfileGate().assess(value)
    assert assessment.disposition is TEVVProfileDisposition.HOLD
    assert "NON_INDEPENDENT_EVALUATOR_REQUIRES_REVIEW" in assessment.reasons



def test_builder_fails_closed_on_raw_lifecycle_or_activity_values() -> None:
    kwargs = {
        "profile_id": "TEVV-BUILDER-TYPES",
        "profile_version": "0.1.0",
        "objective_ref": "objective:builder-types",
        "intended_use_ref": "use:structural-test",
        "tevv_vocabulary_ref": "subjectivity-pipeline:TevvDefinition:v0.1.0",
        "tevv_vocabulary_sha256": "a" * 64,
        "lifecycle_stage": TEVVLifecycleStage.RESEARCH,
        "risk_refs": ("risk:bounded-model-quality",),
        "activities": (TEVVActivity.TEST,),
        "system": system(),
        "metrics": (metric(),),
        "cases": (case(),),
        "repetition_policy_ref": "policy:repeat-v1",
        "nondeterminism_policy_ref": "policy:nondeterminism-v1",
        "minimum_repetitions": 1,
        "stochastic_system": False,
        "aggregation_rule_ref": "aggregation:v1",
        "evaluator_ref": "evaluator:v1",
        "evaluator_version": "v1",
        "evaluator_independence": EvaluatorIndependence.INTERNAL_INDEPENDENT,
        "target_context_ref": "context:test",
        "context_similarity_statement": "Structural test only.",
        "failure_action_ref": "reaction:hold",
        "preregistration_ref": "preregistration:builder-types",
    }
    with pytest.raises(TEVVError, match="lifecycle_stage"):
        build_tevv_profile(**(kwargs | {"lifecycle_stage": "RESEARCH"}))
    with pytest.raises(TEVVError, match="activities"):
        build_tevv_profile(**(kwargs | {"activities": ("TESTING",)}))



def test_profile_requires_repository_tevv_vocabulary_reference() -> None:
    value = profile()
    assert value.tevv_vocabulary_ref == "subjectivity-pipeline:TevvDefinition:v0.1.0"
    assert value.tevv_vocabulary_sha256 == "a" * 64
    with pytest.raises(TEVVError, match="tevv_vocabulary_ref"):
        replace(value, tevv_vocabulary_ref="")
    with pytest.raises(TEVVError, match="tevv_vocabulary_sha256"):
        replace(value, tevv_vocabulary_sha256="not-a-digest")
