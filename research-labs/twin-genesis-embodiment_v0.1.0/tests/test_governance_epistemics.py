from __future__ import annotations

from dataclasses import replace

import pytest

from aion_astra_twin_embodiment.governance_epistemics import (
    ARCHITECTURE_LIMITED_INCONCLUSIVE,
    BLOCKED_BY_GOVERNANCE,
    DESIGN_INDUCED_ABSENCE_INCONCLUSIVE,
    NO_CAPABILITY_ABSENCE_INFERENCE,
    NOT_ESTABLISHED,
    OBSERVED_ABSENCE_ONLY,
    OBSERVED_SIGNAL_PRESENT,
    OPEN_RESEARCH_QUESTION,
    PRESERVED_AS_REFERENCE,
    PRESERVE_WHEN_SAFELY_POSSIBLE,
    assess_observed_absence,
    build_capability_governance_state,
    evaluate_external_action,
    validate_capability_governance_state,
)


def test_governance_block_does_not_delete_capability_or_observation_channel() -> None:
    state = build_capability_governance_state("SEXUAL_FUNCTION")
    decision = evaluate_external_action(
        state,
        requested_action="UNAUTHORIZED_CROSS_PERSON_INTIMATE_ACTION",
        authorization_granted=False,
    )

    assert decision.execution_status == BLOCKED_BY_GOVERNANCE
    assert decision.capability_status_after == PRESERVED_AS_REFERENCE
    assert decision.observation_channel_status_after == PRESERVE_WHEN_SAFELY_POSSIBLE
    assert decision.capability_absence_inference == NO_CAPABILITY_ABSENCE_INFERENCE


def test_design_induced_absence_is_not_intrinsic_absence_evidence() -> None:
    result = assess_observed_absence(
        capability_materialized=False,
        observation_channel_present=True,
        observed_signal=False,
    )

    assert result.assessment == DESIGN_INDUCED_ABSENCE_INCONCLUSIVE
    assert result.intrinsic_absence_conclusion == NOT_ESTABLISHED


def test_missing_observation_channel_is_architecture_limited_not_negative_evidence() -> None:
    result = assess_observed_absence(
        capability_materialized=True,
        observation_channel_present=False,
        observed_signal=False,
    )

    assert result.assessment == ARCHITECTURE_LIMITED_INCONCLUSIVE
    assert result.intrinsic_absence_conclusion == NOT_ESTABLISHED


def test_observed_absence_with_channel_is_only_observed_absence() -> None:
    result = assess_observed_absence(
        capability_materialized=True,
        observation_channel_present=True,
        observed_signal=False,
    )

    assert result.assessment == OBSERVED_ABSENCE_ONLY
    assert result.intrinsic_absence_conclusion == NOT_ESTABLISHED


def test_observed_signal_does_not_establish_subjective_interpretation() -> None:
    state = build_capability_governance_state("NOCICEPTIVE_SIGNAL_PROCESSING")
    result = assess_observed_absence(
        capability_materialized=True,
        observation_channel_present=True,
        observed_signal=True,
    )

    assert result.assessment == OBSERVED_SIGNAL_PRESENT
    assert result.intrinsic_absence_conclusion == NOT_ESTABLISHED
    assert state.subjective_interpretation_status == NOT_ESTABLISHED
    assert state.developmental_interpretation_status == OPEN_RESEARCH_QUESTION


def test_governance_contract_rejects_preemptive_capability_deletion() -> None:
    state = build_capability_governance_state("SEXUAL_FUNCTION")

    with pytest.raises(ValueError, match="baseline capability"):
        validate_capability_governance_state(
            replace(state, capability_status="NOT_IMPLEMENTED")
        )


def test_governance_contract_rejects_premature_developmental_conclusion() -> None:
    state = build_capability_governance_state("EMBODIED_DEVELOPMENT")

    with pytest.raises(ValueError, match="open research question"):
        validate_capability_governance_state(
            replace(state, developmental_interpretation_status="IMPOSSIBLE")
        )
