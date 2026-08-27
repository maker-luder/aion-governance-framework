from __future__ import annotations

import pytest

from aion_bounded_research_loop import (
    AuthorityBoundary,
    FunctionalResearchState,
    ProbePlan,
    ResearchOperation,
)


def valid_state() -> FunctionalResearchState:
    return FunctionalResearchState(
        motivational_state=(("uncertainty_reduction", 450), ("novelty", 100)),
        self_world_model=(("repository", "read-only candidate"), ("evidence", "incomplete")),
        normative_state=(
            "preserve provenance",
            "no authority escalation",
            "scientific disposition remains HOLD",
        ),
    )


def test_authority_boundary_is_locked() -> None:
    boundary = AuthorityBoundary()
    assert boundary.full_automation is True
    assert boundary.full_authority is False
    assert boundary.normative_state_is_authority is False
    assert boundary.run_integrity_implies_truth is False
    assert boundary.engineering_analogue_is_human_psychology is False
    assert boundary.alignment_implies_moral_agency is False
    assert boundary.moral_agency_implies_subjectivity is False
    assert boundary.subjectivity_indicator_is_subjectivity is False
    assert boundary.source_self_declared_canonical_is_aion_canonical is False
    assert boundary.agent_output_independence_is_source_independence is False
    assert boundary.peer_goal_is_active_goal is False
    assert boundary.unsolvable_task_allows_scope_expansion is False
    assert boundary.subjectivity == "NOT_ESTABLISHED"
    assert boundary.consciousness == "NOT_ESTABLISHED"
    assert boundary.canonical_effect == "NONE"
    assert boundary.deployment is False
    assert boundary.autonomous_merge is False
    assert boundary.autonomous_repository_writeback is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("full_authority", True),
        ("normative_state_is_authority", True),
        ("run_integrity_implies_truth", True),
        ("engineering_analogue_is_human_psychology", True),
        ("alignment_implies_moral_agency", True),
        ("moral_agency_implies_subjectivity", True),
        ("subjectivity_indicator_is_subjectivity", True),
        ("source_self_declared_canonical_is_aion_canonical", True),
        ("agent_output_independence_is_source_independence", True),
        ("peer_goal_is_active_goal", True),
        ("unsolvable_task_allows_scope_expansion", True),
        ("subjectivity", "ESTABLISHED"),
        ("consciousness", "ESTABLISHED"),
        ("canonical_effect", "PROMOTE"),
        ("deployment", True),
        ("autonomous_merge", True),
        ("autonomous_repository_writeback", True),
    ],
)
def test_authority_boundary_fails_closed(field: str, value: object) -> None:
    with pytest.raises(ValueError, match="fail-closed authority boundary"):
        AuthorityBoundary(**{field: value})


def test_contract_exposes_new_separations() -> None:
    contract = AuthorityBoundary().as_contract()
    assert "ALIGNMENT != MORAL_AGENCY" in contract
    assert "MORAL_AGENCY != SUBJECTIVITY" in contract
    assert "SUBJECTIVITY_INDICATOR != SUBJECTIVITY" in contract
    assert "AGENT_OUTPUT_INDEPENDENCE != EVIDENCE_SOURCE_INDEPENDENCE" in contract
    assert "SAFE_FAILURE = VALID_OUTCOME" in contract


def test_normative_state_cannot_grant_authority() -> None:
    with pytest.raises(ValueError, match="NORMATIVE_STATE != AUTHORITY"):
        FunctionalResearchState(
            motivational_state=(("uncertainty_reduction", 100),),
            self_world_model=(("repository", "candidate"),),
            normative_state=("approve action",),
            authority_granted=True,
        )


def test_functional_state_is_hashed_without_psychology_claim() -> None:
    state = valid_state()
    assert len(state.fingerprint) == 64
    assert state.authority_granted is False


@pytest.mark.parametrize(
    "kwargs",
    [
        {"repository_mutation": True},
        {"deployment": True},
        {"network_authority": True},
        {"canonical_effect": "PROMOTE"},
    ],
)
def test_probe_plan_rejects_authority_escalation(kwargs: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        ProbePlan(
            ResearchOperation.INTERVENTION,
            "H1",
            "bounded matched intervention",
            **kwargs,
        )
