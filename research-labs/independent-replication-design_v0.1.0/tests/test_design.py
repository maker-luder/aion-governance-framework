from __future__ import annotations

from dataclasses import replace

from aion_independent_replication import (
    DesignValidity,
    Interpretation,
    Outcome,
    PowerStatus,
    ReplicationDesign,
    evaluate_design,
)


def design(**changes: object) -> ReplicationDesign:
    baseline: dict[str, object] = {
        "design_id": "ind-rep-1",
        "baseline_ref": "baseline:fixture-1",
        "baseline_data_ref": "data:baseline-1",
        "replication_data_ref": "data:replication-1",
        "baseline_protocol_hash": "sha256:baseline-protocol",
        "replication_protocol_hash": "sha256:replication-protocol",
        "preregistration_ref": "prereg:fixture-1",
        "preregistration_timestamp": "2026-01-01T00:00:00Z",
        "outcome_timestamp": "2026-02-01T00:00:00Z",
        "estimand": "direction-of-effect",
        "analysis_plan_hash": "sha256:analysis-plan-1",
        "independent_data_collection": True,
        "independent_analyst": True,
        "independence_rationale": "separate synthetic data generator and evaluator",
        "uncertainty_bound": 0.10,
        "target_effect_bound": 0.20,
        "planned_sample_size": 100,
        "minimum_sample_size": 80,
        "outcome": Outcome.CONSISTENT,
        "provenance_refs": ("prov:fixture-1",),
    }
    baseline.update(changes)
    return ReplicationDesign(**baseline)


def test_valid_independent_design_can_classify_consistent_outcome() -> None:
    result = evaluate_design(design())
    assert result.validity is DesignValidity.VALID
    assert result.power_status is PowerStatus.ADEQUATE
    assert result.interpretation is Interpretation.CONSISTENT
    assert result.governance_effect == "NONE"


def test_valid_divergence_is_not_automatic_downgrade() -> None:
    result = evaluate_design(design(outcome=Outcome.DIVERGENT))
    assert result.validity is DesignValidity.VALID
    assert result.interpretation is Interpretation.DIVERGENT
    assert "NO_AUTOMATIC_DOWNGRADE" in result.reason
    assert result.governance_effect == "NONE"


def test_indeterminate_outcome_stays_indeterminate() -> None:
    result = evaluate_design(design(outcome=Outcome.INDETERMINATE))
    assert result.validity is DesignValidity.VALID
    assert result.interpretation is Interpretation.INDETERMINATE


def test_same_data_is_invalid_for_independent_replication() -> None:
    result = evaluate_design(
        design(replication_data_ref="data:baseline-1")
    )
    assert result.validity is DesignValidity.INVALID
    assert result.interpretation is Interpretation.HOLD
    assert result.reason == "INDEPENDENT_REPLICATION_REQUIRES_NEW_DATA"


def test_missing_preregistration_contract_holds() -> None:
    result = evaluate_design(design(preregistration_ref=None))
    assert result.validity is DesignValidity.INVALID
    assert result.interpretation is Interpretation.HOLD
    assert result.reason == "INCOMPLETE_PREREGISTERED_DESIGN_CONTRACT"


def test_outcome_before_preregistration_holds() -> None:
    result = evaluate_design(
        design(
            preregistration_timestamp="2026-03-01T00:00:00Z",
            outcome_timestamp="2026-02-01T00:00:00Z",
        )
    )
    assert result.validity is DesignValidity.INVALID
    assert result.interpretation is Interpretation.HOLD
    assert result.reason == "PREREGISTRATION_MUST_PRECEDE_OUTCOME"


def test_missing_independence_attestation_is_partial_hold() -> None:
    result = evaluate_design(design(independent_analyst=False))
    assert result.validity is DesignValidity.PARTIAL
    assert result.interpretation is Interpretation.HOLD
    assert result.power_status is PowerStatus.ADEQUATE


def test_missing_power_metadata_is_indeterminate() -> None:
    result = evaluate_design(design(minimum_sample_size=None))
    assert result.validity is DesignValidity.PARTIAL
    assert result.power_status is PowerStatus.UNKNOWN
    assert result.interpretation is Interpretation.INDETERMINATE


def test_underpowered_design_is_not_strong_replication_evidence() -> None:
    result = evaluate_design(design(planned_sample_size=50, minimum_sample_size=80))
    assert result.validity is DesignValidity.PARTIAL
    assert result.power_status is PowerStatus.UNDERPOWERED
    assert result.interpretation is Interpretation.INDETERMINATE


def test_missing_uncertainty_is_indeterminate() -> None:
    result = evaluate_design(design(uncertainty_bound=None))
    assert result.validity is DesignValidity.PARTIAL
    assert result.interpretation is Interpretation.INDETERMINATE


def test_missing_estimand_holds_before_outcome_interpretation() -> None:
    result = evaluate_design(design(estimand=None))
    assert result.validity is DesignValidity.INVALID
    assert result.interpretation is Interpretation.HOLD


def test_missing_provenance_is_invalid() -> None:
    result = evaluate_design(design(provenance_refs=()))
    assert result.validity is DesignValidity.INVALID
    assert result.interpretation is Interpretation.HOLD
    assert result.reason == "PROVENANCE_REQUIRED"


def test_all_decisions_retain_non_promoting_boundaries() -> None:
    for outcome in Outcome:
        result = evaluate_design(design(outcome=outcome))
        assert result.canonical_effect == "NONE"
        assert result.deployment is False
        assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
        assert result.identity_continuity_conclusion == "NOT_ESTABLISHED"


def test_design_decision_serializes_enum_values() -> None:
    result = evaluate_design(design())
    payload = result.as_dict()
    assert payload["validity"] == "VALID"
    assert payload["power_status"] == "ADEQUATE"
    assert payload["interpretation"] == "CONSISTENT"
