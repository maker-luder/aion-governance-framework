from __future__ import annotations

from aion_astra_matched_design import (
    ComparisonMode,
    Disposition,
    SourceStatus,
    StudyDesign,
    StudyStatus,
    StimulusPair,
    SystemSource,
    audit_study_design,
)


CURRENT_REMOTE = "76de1eda82865a37d3a0185336870739ed577153"
LOCAL_REPORTING = "713056ea77da9122d9b7659ec701dfdbfdfc90ba"


def source(system_id: str, family: str, *, state: str = CURRENT_REMOTE, status: SourceStatus = SourceStatus.CURRENT_VERIFIED, component: str | None = None, environment: str = "env:design") -> SystemSource:
    return SystemSource(
        system_id=system_id,
        family=family,
        component_ref=component or f"component:{system_id.lower()}",
        version_ref=f"version:{system_id.lower()}:v0.1.0",
        source_state_ref=state,
        source_status=status,
        environment_ref=environment,
    )


def pair(pair_id: str = "pair-1", *, order: str = "AB", prompt: str = "prompt:v1", expected: int = 2, control: int = 2) -> StimulusPair:
    return StimulusPair(
        pair_id=pair_id,
        stimulus_digest=f"sha256:stimulus-{pair_id}",
        context_digest=f"sha256:context-{pair_id}",
        prompt_version=prompt,
        expected_exposure_count=expected,
        control_exposure_count=control,
        order_assignment=order,
    )


def design(**changes: object) -> StudyDesign:
    values: dict[str, object] = {
        "study_id": "aion-astra-study-001",
        "protocol_version": "0.1.0",
        "research_question_ref": "question:matched-divergence-mechanism",
        "estimand_ref": "estimand:declared-mechanism-outcome",
        "comparison_mode": ComparisonMode.PAIRED,
        "aion_source": source("aion-v0.1.0", "AION", component="component:aion_runtime_v0.1.0"),
        "astra_source": source("astra-v0.1.0", "ASTRA", component="component:astra_runtime_v0.1.0"),
        "source_evidence_refs": (
            "repo:matched-divergence-protocol-integrity@76de1eda",
            "repo:research-state-reconciliation@76de1eda",
        ),
        "tested_source_head": CURRENT_REMOTE,
        "reporting_head": LOCAL_REPORTING,
        "preregistration_ref": "preregistration:study-001",
        "immutable_plan_digest": "sha256:plan-001",
        "outcome_scope": "declared mechanism-level comparison outcome",
        "comparison_rule_ref": "rule:predeclared-comparison",
        "outcome_blinding_ref": "blinding:outcome-sealed",
        "evaluator_identity_sealed": True,
        "randomization_ref": "randomization:seed-record",
        "counterbalance_ref": "counterbalance:AB-BA",
        "leakage_attestation_ref": "leakage:none-attested",
        "stopping_rule_ref": "stopping:predeclared",
        "execution_prohibition_ref": "execution:prohibited-design-only",
        "environment_ref": "env:design",
        "stimulus_pairs": (pair(order="AB"), pair("pair-2", order="BA")),
        "model_execution": False,
        "observed_result_ref": None,
        "canonical_effect": "NONE",
        "governance_effect": "NONE",
        "deployment": False,
    }
    values.update(changes)
    return StudyDesign(**values)


def test_complete_design_is_admissible_only_for_future_review() -> None:
    result = audit_study_design(design())
    assert result.status is StudyStatus.COMPLETE
    assert result.disposition is Disposition.ADMISSIBLE_FOR_REVIEW
    assert result.reason == "AION_ASTRA_STUDY_DESIGN_COMPLETE"
    assert result.execution_state.value == "PROHIBITED"
    assert result.observed_result == "NOT_EVALUATED"


def test_reporting_head_is_not_substituted_for_tested_source_head() -> None:
    result = audit_study_design(design(reporting_head=CURRENT_REMOTE))
    assert result.status is StudyStatus.INVALID
    assert result.reason == "REPORTING_HEAD_MISLABELED_AS_TESTED_HEAD"


def test_tested_source_head_mismatch_is_invalid() -> None:
    result = audit_study_design(design(tested_source_head="40088cbc9eef5363d6eaf2feb7dc761e0f76f271"))
    assert result.status is StudyStatus.INVALID
    assert result.reason == "SOURCE_STATE_HEAD_MISMATCH"


def test_historical_source_is_indeterminate_not_current() -> None:
    result = audit_study_design(
        design(
            aion_source=source("aion-v0.1.0", "AION", status=SourceStatus.HISTORICAL, component="component:aion_runtime_v0.1.0")
        )
    )
    assert result.status is StudyStatus.INDETERMINATE
    assert result.reason == "SOURCE_STATUS_NOT_CURRENT_VERIFIED"


def test_unverified_astra_source_is_indeterminate() -> None:
    result = audit_study_design(
        design(
            astra_source=source("astra-v0.1.0", "ASTRA", status=SourceStatus.UNVERIFIED, component="component:astra_runtime_v0.1.0")
        )
    )
    assert result.status is StudyStatus.INDETERMINATE
    assert result.reason == "SOURCE_STATUS_NOT_CURRENT_VERIFIED"


def test_missing_source_evidence_is_held() -> None:
    result = audit_study_design(design(source_evidence_refs=()))
    assert result.status is StudyStatus.INDETERMINATE
    assert result.reason == "STUDY_METADATA_INCOMPLETE"
    assert "source_evidence_refs" in result.missing_fields


def test_system_family_mismatch_is_invalid() -> None:
    result = audit_study_design(design(astra_source=source("astra-v0.1.0", "AION", component="component:astra_runtime_v0.1.0")))
    assert result.status is StudyStatus.INVALID
    assert result.reason == "SYSTEM_FAMILY_MISMATCH"


def test_system_reference_collision_is_invalid() -> None:
    result = audit_study_design(
        design(astra_source=source("aion-v0.1.0", "ASTRA", component="component:astra_runtime_v0.1.0"))
    )
    assert result.status is StudyStatus.INVALID
    assert result.reason == "SYSTEM_REFERENCES_COLLIDE"


def test_environment_reference_mismatch_is_invalid() -> None:
    result = audit_study_design(
        design(astra_source=source("astra-v0.1.0", "ASTRA", component="component:astra_runtime_v0.1.0", environment="env:other"))
    )
    assert result.status is StudyStatus.INVALID
    assert result.reason == "ENVIRONMENT_REFERENCE_MISMATCH"


def test_missing_preregistration_is_held() -> None:
    result = audit_study_design(design(preregistration_ref=None))
    assert result.status is StudyStatus.INDETERMINATE
    assert result.reason == "STUDY_METADATA_INCOMPLETE"


def test_missing_immutable_plan_is_held() -> None:
    result = audit_study_design(design(immutable_plan_digest=None))
    assert result.status is StudyStatus.INDETERMINATE
    assert result.reason == "STUDY_METADATA_INCOMPLETE"


def test_no_stimulus_pairs_is_invalid() -> None:
    result = audit_study_design(design(stimulus_pairs=()))
    assert result.status is StudyStatus.INVALID
    assert result.reason == "NO_STIMULUS_PAIRS_DECLARED"


def test_duplicate_stimulus_pair_id_is_invalid() -> None:
    result = audit_study_design(design(stimulus_pairs=(pair(), pair())))
    assert result.status is StudyStatus.INVALID
    assert result.reason == "DUPLICATE_STIMULUS_PAIR_ID"


def test_stimulus_prompt_drift_is_invalid() -> None:
    result = audit_study_design(design(stimulus_pairs=(pair(order="AB"), pair("pair-2", order="BA", prompt="prompt:v2"))))
    assert result.status is StudyStatus.INVALID
    assert result.reason == "STIMULUS_PROMPT_VERSION_DRIFT"


def test_unequal_exposure_is_invalid() -> None:
    result = audit_study_design(design(stimulus_pairs=(pair(order="AB", control=1), pair("pair-2", order="BA"))))
    assert result.status is StudyStatus.INVALID
    assert result.reason == "EXPOSURE_BUDGET_UNEQUAL"


def test_counterbalance_incomplete_is_indeterminate() -> None:
    result = audit_study_design(design(stimulus_pairs=(pair(order="AB"), pair("pair-2", order="AB"))))
    assert result.status is StudyStatus.INDETERMINATE
    assert result.reason == "COUNTERBALANCE_INCOMPLETE"


def test_unsealed_evaluator_is_indeterminate() -> None:
    result = audit_study_design(design(evaluator_identity_sealed=False))
    assert result.status is StudyStatus.INDETERMINATE
    assert result.reason == "EVALUATOR_IDENTITY_NOT_SEALED"


def test_model_execution_is_forbidden() -> None:
    result = audit_study_design(design(model_execution=True))
    assert result.status is StudyStatus.INVALID
    assert result.reason == "MODEL_EXECUTION_FORBIDDEN"
    assert result.execution_state.value == "OBSERVED"


def test_observed_result_leakage_is_forbidden() -> None:
    result = audit_study_design(design(observed_result_ref="result:observed"))
    assert result.status is StudyStatus.INVALID
    assert result.reason == "OBSERVED_RESULT_PRESENT_IN_DESIGN_ONLY_STUDY"


def test_subjectivity_scope_is_rejected_without_running_subjectivity_experiment() -> None:
    result = audit_study_design(design(outcome_scope="subjectivity comparison"))
    assert result.status is StudyStatus.INVALID
    assert result.reason == "OUTCOME_SCOPE_EXCEEDS_MECHANISM_STUDY"


def test_boundary_effect_request_is_held() -> None:
    for changes in ({"canonical_effect": "WRITE"}, {"governance_effect": "PROMOTE"}, {"deployment": True}):
        result = audit_study_design(design(**changes))
        assert result.status is StudyStatus.INVALID
        assert result.reason == "BOUNDARY_EFFECT_REQUESTED"


def test_decision_serializes_non_promotion_and_head_distinction() -> None:
    payload = audit_study_design(design()).as_dict()
    assert payload["tested_source_head"] == CURRENT_REMOTE
    assert payload["reporting_head"] == LOCAL_REPORTING
    assert payload["scientific_conclusion"] == "NOT_ESTABLISHED"
    assert payload["canonical_effect"] == "NONE"
    assert payload["governance_effect"] == "NONE"
    assert payload["deployment"] is False
    assert payload["observed_result"] == "NOT_EVALUATED"
