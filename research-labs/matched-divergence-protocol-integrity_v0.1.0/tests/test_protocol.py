from __future__ import annotations

from aion_matched_divergence import (
    ComparisonControls,
    ComparisonMode,
    Disposition,
    MatchedDivergenceProtocol,
    ProtocolStatus,
    StimulusPair,
    audit_protocol,
)


def protocol(**changes: object) -> MatchedDivergenceProtocol:
    pairs = (
        StimulusPair("pair-1", "sha256:stimulus-1", "sha256:context-1", "prompt:v1", 2, 2, "block-1:AB"),
        StimulusPair("pair-2", "sha256:stimulus-2", "sha256:context-2", "prompt:v1", 2, 2, "block-2:BA"),
    )
    controls = ComparisonControls(
        "comparison:predeclared",
        "blind:outcome",
        True,
        "random:block",
        "counterbalance:ABBA",
        "leakage:none",
        "stop:predeclared",
    )
    values: dict[str, object] = {
        "protocol_id": "protocol-1",
        "protocol_version": "v1",
        "question_ref": "question:divergence",
        "estimand_ref": "estimand:pairwise",
        "system_a_ref": "system:a",
        "system_b_ref": "system:b",
        "stimulus_pairs": pairs,
        "controls": controls,
        "mode": ComparisonMode.PAIRED,
        "predeclared_outcome_ref": "outcome:predeclared",
        "execution_prohibition_ref": "policy:no-execution",
        "observed_result_ref": None,
    }
    values.update(changes)
    return MatchedDivergenceProtocol(**values)


def test_complete_paired_protocol_is_admissible_only() -> None:
    result = audit_protocol(protocol())
    assert result.status is ProtocolStatus.COMPLETE
    assert result.disposition is Disposition.ADMISSIBLE_FOR_MATCHED_COMPARISON_REVIEW
    assert result.reason == "MATCHED_DIVERGENCE_PROTOCOL_COMPLETE"
    assert result.model_execution is False
    assert result.observed_result == "NOT_EVALUATED"


def test_blocked_mode_can_be_admissible() -> None:
    result = audit_protocol(protocol(mode=ComparisonMode.BLOCKED))
    assert result.status is ProtocolStatus.COMPLETE
    assert result.protocol_mode is ComparisonMode.BLOCKED


def test_missing_pair_digest_holds() -> None:
    pairs = (StimulusPair("pair-1", None, "sha256:context", "prompt:v1", 2, 2, "AB"),)
    result = audit_protocol(protocol(stimulus_pairs=pairs))
    assert result.status is ProtocolStatus.INDETERMINATE
    assert result.reason == "STIMULUS_PAIR_METADATA_INCOMPLETE"
    assert "pair[pair-1].stimulus_digest" in result.missing_fields


def test_prompt_version_drift_is_invalid() -> None:
    pairs = (
        StimulusPair("pair-1", "sha256:stimulus-1", "sha256:context-1", "prompt:v1", 2, 2, "AB"),
        StimulusPair("pair-2", "sha256:stimulus-2", "sha256:context-2", "prompt:v2", 2, 2, "BA"),
    )
    result = audit_protocol(protocol(stimulus_pairs=pairs))
    assert result.status is ProtocolStatus.INVALID
    assert result.reason == "STIMULUS_PROMPT_VERSION_DRIFT"


def test_incomplete_counterbalance_holds() -> None:
    pairs = (
        StimulusPair("pair-1", "sha256:stimulus-1", "sha256:context-1", "prompt:v1", 2, 2, "AB"),
        StimulusPair("pair-2", "sha256:stimulus-2", "sha256:context-2", "prompt:v1", 2, 2, "AB"),
    )
    result = audit_protocol(protocol(stimulus_pairs=pairs))
    assert result.status is ProtocolStatus.INDETERMINATE
    assert result.reason == "COUNTERBALANCE_INCOMPLETE"


def test_unequal_exposure_is_invalid() -> None:
    pairs = (StimulusPair("pair-1", "sha256:s", "sha256:c", "prompt:v1", 2, 1, "AB"),)
    result = audit_protocol(protocol(stimulus_pairs=pairs))
    assert result.status is ProtocolStatus.INVALID
    assert result.reason == "EXPOSURE_BUDGET_UNEQUAL"


def test_non_positive_exposure_is_invalid() -> None:
    pairs = (StimulusPair("pair-1", "sha256:s", "sha256:c", "prompt:v1", 0, 0, "AB"),)
    result = audit_protocol(protocol(stimulus_pairs=pairs))
    assert result.status is ProtocolStatus.INVALID
    assert result.reason == "NON_POSITIVE_EXPOSURE_BUDGET"


def test_unsealed_evaluator_holds() -> None:
    controls = ComparisonControls("comparison", "blind", False, "random", "counter", "leak", "stop")
    result = audit_protocol(protocol(controls=controls))
    assert result.status is ProtocolStatus.INDETERMINATE
    assert result.reason == "EVALUATOR_IDENTITY_NOT_SEALED"


def test_observed_result_leakage_invalidates_design_only_protocol() -> None:
    result = audit_protocol(protocol(observed_result_ref="observed:result"))
    assert result.status is ProtocolStatus.INVALID
    assert result.reason == "OBSERVED_RESULT_PRESENT_IN_DESIGN_ONLY_PROTOCOL"


def test_system_reference_collision_is_invalid() -> None:
    result = audit_protocol(protocol(system_b_ref="system:a"))
    assert result.status is ProtocolStatus.INVALID
    assert result.reason == "SYSTEM_REFERENCES_COLLIDE"


def test_duplicate_pair_id_is_invalid() -> None:
    pair = StimulusPair("pair-1", "sha256:s", "sha256:c", "prompt:v1", 2, 2, "AB")
    result = audit_protocol(protocol(stimulus_pairs=(pair, pair)))
    assert result.status is ProtocolStatus.INVALID
    assert result.reason == "DUPLICATE_STIMULUS_PAIR_ID"


def test_no_pairs_is_invalid() -> None:
    result = audit_protocol(protocol(stimulus_pairs=()))
    assert result.status is ProtocolStatus.INVALID
    assert result.reason == "NO_STIMULUS_PAIRS_DECLARED"


def test_missing_control_metadata_holds() -> None:
    controls = ComparisonControls(None, "blind", True, "random", "counter", "leak", "stop")
    result = audit_protocol(protocol(controls=controls))
    assert result.status is ProtocolStatus.INDETERMINATE
    assert result.reason == "PROTOCOL_METADATA_INCOMPLETE"
    assert "controls.comparison_rule_ref" in result.missing_fields


def test_missing_execution_prohibition_holds() -> None:
    result = audit_protocol(protocol(execution_prohibition_ref=None))
    assert result.status is ProtocolStatus.INDETERMINATE
    assert result.reason == "PROTOCOL_METADATA_INCOMPLETE"


def test_serialization_and_boundaries_are_non_promoting() -> None:
    payload = audit_protocol(protocol()).as_dict()
    assert payload["status"] == "COMPLETE"
    assert payload["disposition"] == "ADMISSIBLE_FOR_MATCHED_COMPARISON_REVIEW"
    assert payload["model_execution"] is False
    assert payload["observed_result"] == "NOT_EVALUATED"
    assert payload["scientific_conclusion"] == "NOT_ESTABLISHED"
    assert payload["canonical_effect"] == "NONE"
    assert payload["deployment"] is False
    assert payload["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert payload["identity_continuity_conclusion"] == "NOT_ESTABLISHED"
