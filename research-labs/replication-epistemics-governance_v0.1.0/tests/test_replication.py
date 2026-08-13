from aion_replication_epistemics import (
    Interpretation,
    Outcome,
    ReplicationAttempt,
    StudyKind,
    Validity,
    evaluate_attempt,
)


def attempt(**kwargs: object) -> ReplicationAttempt:
    defaults: dict[str, object] = {
        "attempt_id": "rep-1",
        "study_kind": StudyKind.REPLICABILITY,
        "baseline_ref": "baseline:1",
        "protocol_hash": "sha256:protocol-1",
        "preregistration_ref": "prereg:1",
        "baseline_data_ref": "data:baseline",
        "replication_data_ref": "data:replication",
        "independent_evaluator": True,
        "provenance_refs": ("prov:1",),
        "outcome": Outcome.CONSISTENT,
        "uncertainty_bound": 0.1,
        "attribute_of_interest": "direction-of-effect",
        "power_review_ref": "power:1",
    }
    defaults.update(kwargs)
    return ReplicationAttempt(**defaults)


def test_valid_consistent_independent_replication() -> None:
    result = evaluate_attempt(attempt())
    assert result.validity is Validity.VALID
    assert result.interpretation is Interpretation.CONSISTENT
    assert result.governance_effect == "NONE"


def test_valid_failed_replication_is_divergent_not_automatic_downgrade() -> None:
    result = evaluate_attempt(attempt(outcome=Outcome.FAILED))
    assert result.validity is Validity.VALID
    assert result.interpretation is Interpretation.DIVERGENT
    assert "NOT_AUTOMATIC_DOWNGRADE" in result.reason
    assert result.governance_effect == "NONE"


def test_null_result_remains_indeterminate() -> None:
    result = evaluate_attempt(attempt(outcome=Outcome.NULL))
    assert result.validity is Validity.VALID
    assert result.interpretation is Interpretation.INDETERMINATE


def test_inconclusive_result_remains_indeterminate() -> None:
    result = evaluate_attempt(attempt(outcome=Outcome.INCONCLUSIVE))
    assert result.validity is Validity.VALID
    assert result.interpretation is Interpretation.INDETERMINATE


def test_same_data_cannot_be_called_independent_replicability() -> None:
    result = evaluate_attempt(
        attempt(
            baseline_data_ref="data:same",
            replication_data_ref="data:same",
        )
    )
    assert result.validity is Validity.INVALID
    assert result.interpretation is Interpretation.HOLD
    assert result.reason == "REPLICABILITY_REQUIRES_INDEPENDENT_DATA"


def test_missing_provenance_holds() -> None:
    result = evaluate_attempt(attempt(provenance_refs=()))
    assert result.validity is Validity.INVALID
    assert result.interpretation is Interpretation.HOLD


def test_missing_protocol_holds() -> None:
    result = evaluate_attempt(attempt(protocol_hash=None))
    assert result.validity is Validity.INVALID
    assert result.interpretation is Interpretation.HOLD


def test_missing_independent_evaluator_is_partial_hold() -> None:
    result = evaluate_attempt(attempt(independent_evaluator=False))
    assert result.validity is Validity.PARTIAL
    assert result.interpretation is Interpretation.HOLD


def test_missing_uncertainty_is_indeterminate() -> None:
    result = evaluate_attempt(attempt(uncertainty_bound=None))
    assert result.validity is Validity.PARTIAL
    assert result.interpretation is Interpretation.INDETERMINATE


def test_reproducibility_can_use_same_data_when_kind_is_explicit() -> None:
    result = evaluate_attempt(
        attempt(
            study_kind=StudyKind.REPRODUCIBILITY,
            baseline_data_ref="data:same",
            replication_data_ref="data:same",
        )
    )
    assert result.validity is Validity.VALID
    assert result.interpretation is Interpretation.CONSISTENT


def test_all_results_keep_non_promoting_boundaries() -> None:
    for outcome in Outcome:
        result = evaluate_attempt(attempt(outcome=outcome))
        assert result.canonical_effect == "NONE"
        assert result.deployment is False
        assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
        assert result.identity_continuity_conclusion == "NOT_ESTABLISHED"
