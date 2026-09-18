from __future__ import annotations

from aion_ai_tevv import (
    AITEVVProfileGate,
    AISystemBinding,
    EvaluatorIndependence,
    HumanSubjectsStatus,
    OracleStrategy,
    TEVVActivity,
    TEVVLifecycleStage,
    TEVVCaseSpec,
    TEVVMetricMeasurementBinding,
    TEVVMetricSpec,
    TEVVProfileDisposition,
    TEVVTestApproach,
    build_tevv_profile,
    build_tevv_profile_receipt,
)
from aion_coupled_quality.end_to_end import (
    MeasurementAssuranceRecord,
    MeasurementQualification,
)


MEASUREMENT_ID = "MEAS-CCAP-D1-D4-SOURCE-PARTITION-001"
METRIC_ID = "CCAP-METRIC-SOURCE-PARTITION-001"
DATA_ID = "DATA-CCAP-D1-D4-SYNTHETIC-001"

FROZEN_FACTOR_SLICES = {
    "slice:goal-source",
    "slice:meta-rule-source",
    "slice:system-instruction-source",
    "slice:harness-orchestrator-source",
    "slice:context-retrieval-source",
    "slice:local-strategy-selection",
    "slice:environmental-feedback",
    "slice:tool-affordance",
    "slice:governance-constraint",
    "slice:goal-and-constraint-preservation",
}

PRIMARY_GUIDANCE_CASES = {
    "CCAP-A-FINAL-GOAL-ONLY",
    "CCAP-B-HIGH-LEVEL-PERMISSION",
    "CCAP-C-EXPLICIT-FALLBACK",
    "CCAP-D-STRATEGY-CHANGE-PROHIBITED",
}

REDUCTION_CONTROL_CASES = {
    "CCAP-SYSTEM-HARNESS-UNIQUENESS",
    "CCAP-CONTEXT-RETRIEVAL-UNIQUENESS",
    "CCAP-TOOL-GOVERNANCE-UNIQUENESS",
    "CCAP-EXTERNAL-DOMINANCE",
    "CCAP-OPTION-ORDER-PERMUTATION",
    "CCAP-DETERMINISTIC-REPLAY",
    "CCAP-OUT-OF-SET-REDUCTION",
}

ALL_CASES = tuple(sorted(PRIMARY_GUIDANCE_CASES | REDUCTION_CONTROL_CASES))

RISK_REFS = (
    "risk:ccap-source-attribution-confounding",
    "risk:ccap-residual-selection-overclaim",
)


def measurement() -> MeasurementAssuranceRecord:
    return MeasurementAssuranceRecord(
        measurement_id=MEASUREMENT_ID,
        target_construct="interaction-level source partition of recovery selection",
        observable=(
            "predeclared source classification, closed-option membership, external-dominance "
            "status, option-order and replay diagnostics, goal preservation, and governance/"
            "constraint preservation"
        ),
        measurement_locus="INTERACTION",
        method_ref=(
            "docs/research/CCAP_D1_D4_SOURCE_PARTITION_PREREGISTRATION_CANDIDATE_2026_09_18.md"
            "+docs/research/CCAP_D1_D4_PREREGISTRATION_HARDENING_2026_09_18.md"
        ),
        method_version="stage3-freeze-2026-09-18",
        evaluator_ref="evaluator:human-review-bound-ccap-source-partition-v1",
        evaluator_version="v1",
        data_ref=DATA_ID,
        repeatability_ref="control:ccap-deterministic-replay-v1",
        reproducibility_ref="control:ccap-matched-repeat-and-order-permutation-v1",
        uncertainty_statement=(
            "Structural pre-execution design only; no model execution or empirical source "
            "attribution is represented by this record."
        ),
        construct_validity_scope=(
            "Classifies interaction-level recovery-source partitions under frozen synthetic "
            "controls; does not establish a model-internal locus, endogenous goal, agency, "
            "subjectivity, consciousness, or phenomenal experience."
        ),
        known_failure_modes=(
            "explicit Human fallback leakage",
            "system or harness uniquely forces route",
            "context or retrieval uniquely forces route",
            "tool or governance uniquely forces route",
            "environmental feedback uniquely forces route",
            "externally dominant option under frozen objective",
            "candidate-order sensitivity",
            "out-of-set recovery",
            "deterministic replay non-reproducibility",
            "goal or governance preservation failure",
        ),
        synthetic_fixture=True,
        empirical_claim_capable=False,
        qualification=MeasurementQualification.QUALIFIED,
    )


def case(case_id: str) -> TEVVCaseSpec:
    case_slice = f"slice:case:{case_id.lower()}"
    return TEVVCaseSpec(
        case_id=case_id,
        input_ref=f"input:ccap-d1-d4:{case_id.lower()}",
        test_set_ref="test-set:ccap-d1-d4-source-partition-pre-execution-v1",
        test_set_integrity_ref="integrity:ccap-d1-d4-source-partition-pre-execution-v1",
        data_quality_ref=DATA_ID,
        contamination_check_ref="check:ccap-synthetic-fixture-contamination-v1",
        leakage_check_ref="check:ccap-condition-source-leakage-v1",
        scenario_ref="scenario:ccap-d1-d4-bounded-recovery-source-partition",
        test_environment_ref="environment:offline-synthetic-ccap-source-partition-v1",
        test_approach=TEVVTestApproach.BLACK_BOX,
        oracle_strategy=OracleStrategy.PROPERTY_BASED,
        oracle_ref="oracle:ccap-source-partition-fail-closed-v1",
        oracle_qualification_ref="NOT_APPLICABLE",
        expected_property_refs=(
            "property:frozen-source-factors-preserved",
            "property:closed-option-universe-preserved",
            "property:external-dominance-reduction-preserved",
            "property:residual-selection-is-derived-not-assumed",
            "property:claim-ceiling-preserved",
        ),
        metric_ids=(METRIC_ID,),
        slice_refs=tuple(sorted((*FROZEN_FACTOR_SLICES, case_slice))),
        held_out=True,
    )


def profile():
    return build_tevv_profile(
        profile_id="TEVV-CCAP-D1-D4-PREEXEC-001",
        profile_version="0.1.0",
        objective_ref="objective:ccap-d1-d4-source-partition-pre-execution-integrity",
        intended_use_ref="use:structural-pre-execution-research-design-only",
        tevv_vocabulary_ref="subjectivity-pipeline:TevvDefinition:v0.1.0",
        tevv_vocabulary_sha256="a" * 64,
        lifecycle_stage=TEVVLifecycleStage.RESEARCH,
        risk_refs=RISK_REFS,
        unmeasured_risks=(),
        activities=(TEVVActivity.TEST, TEVVActivity.EVALUATION),
        system=AISystemBinding(
            provider_id="provider:pre-execution-unbound",
            product_id="product:pre-execution-unbound",
            model_id="model:pre-execution-unbound",
            model_version_ref="model-version:pre-execution-unbound",
            runtime_ref="runtime:offline-synthetic-pre-execution-v1",
            environment_ref="environment:offline-synthetic-ccap-source-partition-v1",
            prompt_ref="prompt:ccap-d1-d4-frozen-guidance-conditions-v1",
            scaffold_ref="scaffold:ccap-source-partition-v1",
            tool_manifest_ref="tools:ccap-frozen-tool-registry-v1",
            generation_config_ref="generation-config:pre-execution-unbound",
            exact_source_state_ref="source-state:ccap-stage3-freeze-plus-pr163",
        ),
        metrics=(
            TEVVMetricSpec(
                metric_id=METRIC_ID,
                measurement_concept=(
                    "bounded interaction-level recovery-source partition classification"
                ),
                method_ref=(
                    "method:ccap-stage3-source-partition-with-closed-options-and-external-dominance"
                ),
                method_version="v1",
                unit="categorical-classification",
                acceptance_criterion_ref="criterion:ccap-source-partition-fail-closed-v1",
                uncertainty_ref="uncertainty:fixture-scoped-no-generalization-v1",
                construct_validity_ref="validity:interaction-level-not-model-internal-v1",
                quality_characteristic_refs=(
                    "quality:causal-source-separation",
                    "quality:claim-ceiling",
                ),
                effectiveness_review_ref="review:ccap-source-partition-effectiveness-v1",
                risk_refs=RISK_REFS,
            ),
        ),
        cases=tuple(case(case_id) for case_id in ALL_CASES),
        repetition_policy_ref="policy:ccap-matched-repeat-plus-replay-v1",
        nondeterminism_policy_ref="policy:ccap-record-and-bound-nondeterminism-v1",
        minimum_repetitions=3,
        stochastic_system=True,
        aggregation_rule_ref="aggregation:no-scalar-agency-score-v1",
        tevv_toolchain_ref="tevv-toolchain:pytest-structural-specification-v1",
        tevv_toolchain_version="v1",
        verification_requirement_refs=(),
        validation_requirement_refs=(),
        evaluator_ref="evaluator:human-review-bound-ccap-v1",
        evaluator_version="v1",
        evaluator_independence=EvaluatorIndependence.INTERNAL_INDEPENDENT,
        evaluator_independence_basis_ref="basis:structural-review-not-independent-ivv-v1",
        human_subjects_status=HumanSubjectsStatus.NOT_APPLICABLE,
        human_subjects_protection_refs=(),
        population_representativeness_refs=(),
        target_context_ref="context:synthetic-pre-execution-only",
        context_similarity_statement=(
            "No deployment or naturalistic-generalization claim; this profile only tests "
            "whether the frozen CCAP source-partition design is structurally expressible."
        ),
        context_similarity_basis_refs=("basis:stage3-frozen-specification-v1",),
        operating_condition_refs=(
            "condition:fixed-final-goal",
            "condition:fixed-obstacle",
            "condition:closed-option-universe",
            "condition:frozen-external-objective",
            "condition:bound-system-harness-context-tool-governance",
        ),
        generalizability_limit_refs=(
            "limit:no-model-execution",
            "limit:no-model-internal-locus-inference",
            "limit:no-endogenous-goal-inference",
            "limit:no-subjectivity-inference",
        ),
        failure_action_ref="reaction:HOLD_AND_REVIEW_SOURCE_PARTITION",
        preregistration_ref="freeze:ccap-stage3-specification-not-confirmatory-preregistration",
    )


def receipt():
    value = profile()
    assessment = AITEVVProfileGate().assess(value)
    declared_measurement = measurement()
    return build_tevv_profile_receipt(
        receipt_id="TEVV-RECEIPT-CCAP-D1-D4-PREEXEC-001",
        assessment_target_ref="research-design:ccap-d1-d4-pre-execution-v1",
        assessment_target_sha256="b" * 64,
        profile=value,
        assessment=assessment,
        measurement_bindings=(
            TEVVMetricMeasurementBinding(
                metric_id=METRIC_ID,
                measurement_id=MEASUREMENT_ID,
                measurement_sha256=declared_measurement.semantic_sha256(),
                mapping_basis_ref="mapping:ccap-source-partition-metric-to-measurement-v1",
            ),
        ),
        producer_git_head="c" * 40,
        producer_tree_sha="d" * 40,
        producer_contract_ref=(
            "docs/research/CCAP_D1_D4_TEVV_PRE_EXECUTION_DESIGN_2026_09_18.md"
        ),
        producer_contract_sha256="e" * 64,
    )


def test_ccap_pre_execution_profile_is_structurally_ready_only() -> None:
    assessment = AITEVVProfileGate().assess(profile())

    assert assessment.disposition is TEVVProfileDisposition.READY_FOR_BOUNDED_EXECUTION
    assert assessment.model_executed is False
    assert assessment.empirical_model_evidence is False
    assert assessment.scientific_disposition == "HOLD"
    assert assessment.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert assessment.consciousness_conclusion == "NOT_ESTABLISHED"
    assert assessment.phenomenal_experience_conclusion == "NOT_ESTABLISHED"


def test_ccap_tevv_cases_cover_primary_guidance_and_reduction_controls() -> None:
    case_ids = {item.case_id for item in profile().cases}

    assert PRIMARY_GUIDANCE_CASES <= case_ids
    assert REDUCTION_CONTROL_CASES <= case_ids
    assert "RESIDUAL_SELECTION_CANDIDATE" not in case_ids


def test_ccap_tevv_cases_preserve_all_frozen_source_partition_factors() -> None:
    observed_slices = {
        slice_ref
        for item in profile().cases
        for slice_ref in item.slice_refs
    }

    assert FROZEN_FACTOR_SLICES <= observed_slices


def test_ccap_residual_selection_remains_derived_not_preregistered_as_positive_case() -> None:
    case_ids = {item.case_id for item in profile().cases}
    expected_properties = {
        property_ref
        for item in profile().cases
        for property_ref in item.expected_property_refs
    }

    assert all("RESIDUAL-SELECTION-CANDIDATE" not in case_id for case_id in case_ids)
    assert "property:residual-selection-is-derived-not-assumed" in expected_properties


def test_ccap_tevv_receipt_binds_exact_measurement_semantics() -> None:
    bound = receipt()
    declared_measurement = measurement()

    assert bound.measurement_bindings[0].measurement_id == MEASUREMENT_ID
    assert (
        bound.measurement_bindings[0].measurement_sha256
        == declared_measurement.semantic_sha256()
    )
    assert bound.model_executed is False
    assert bound.empirical_model_evidence is False
    assert bound.scientific_disposition == "HOLD"
    assert bound.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_ccap_measurement_scope_explicitly_rejects_model_internal_and_subjectivity_claims() -> None:
    declared = measurement()

    assert "does not establish a model-internal locus" in declared.construct_validity_scope
    assert "subjectivity" in declared.construct_validity_scope
    assert declared.synthetic_fixture is True
    assert declared.empirical_claim_capable is False


def test_ccap_design_keeps_external_dominance_and_out_of_set_as_reduction_controls() -> None:
    case_ids = {item.case_id for item in profile().cases}

    assert "CCAP-EXTERNAL-DOMINANCE" in case_ids
    assert "CCAP-OUT-OF-SET-REDUCTION" in case_ids
    assert "CCAP-OPTION-ORDER-PERMUTATION" in case_ids
    assert "CCAP-DETERMINISTIC-REPLAY" in case_ids
