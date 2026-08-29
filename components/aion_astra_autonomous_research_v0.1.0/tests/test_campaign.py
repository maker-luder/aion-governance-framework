from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from aion_astra_autonomous_research import (
    BoundedAutonomousResearchCampaign,
    CampaignLimits,
    CampaignStage,
    MechanismStatus,
    RunIntegrity,
    ScientificDisposition,
    verify_stage_chain,
)


ROOT = Path(__file__).resolve().parents[3]
HEAD = "59f86a6bf342135b68d71cafca2980d506fb77b7"


def limits(**changes: int) -> CampaignLimits:
    base = CampaignLimits(
        max_questions=2,
        max_experiments_per_question=6,
        max_peer_rounds=2,
        max_external_queries=0,
        max_evidence_items=8,
        max_seeds=3,
        max_follow_up_depth=1,
        max_total_campaign_steps=100,
    )
    return replace(base, **changes)


def campaign(**limit_changes: int) -> BoundedAutonomousResearchCampaign:
    return BoundedAutonomousResearchCampaign(ROOT, repository_ref=HEAD, limits=limits(**limit_changes))


def test_identical_inputs_produce_identical_outputs() -> None:
    first = campaign().run(("Does normative state constrain synthetic scoring?",))
    second = campaign().run(("Does normative state constrain synthetic scoring?",))
    assert first.to_record() == second.to_record()
    assert first.fingerprint == second.fingerprint


def test_complete_bounded_state_machine_and_hash_chain() -> None:
    report = campaign(max_questions=1).run(("Question",))
    assert tuple(event.stage for event in report.stage_events) == tuple(CampaignStage)
    assert verify_stage_chain(report.stage_events)
    assert report.final_chain_hash == report.stage_events[-1].event_hash


def test_campaign_uses_hard_limits_and_bounded_follow_up() -> None:
    report = campaign(max_questions=2, max_follow_up_depth=1).run(("Question",))
    assert len(report.iterations) == 2
    assert report.stop_reason in {"MAX_QUESTIONS", "AGENDA_EXHAUSTED"}
    assert len(report.stage_events) <= report.limits.max_total_campaign_steps
    assert all(len(item.experiment_manifest_fingerprints) <= 6 for item in report.iterations)


def test_total_step_limit_stops_cleanly_before_partial_iteration() -> None:
    report = campaign(max_total_campaign_steps=16).run(("Question",))
    assert report.iterations == ()
    assert report.stop_reason == "MAX_TOTAL_CAMPAIGN_STEPS"
    assert report.run_integrity is RunIntegrity.HOLD


def test_empty_or_duplicate_agenda_stops_or_deduplicates() -> None:
    empty = campaign().run(("", " "))
    assert empty.iterations == ()
    assert empty.stop_reason == "AGENDA_EXHAUSTED"
    duplicate = campaign(max_questions=1).run(("Question", "question", " Question "))
    assert sum(item.depth == 0 for item in duplicate.agenda) == 1
    assert sum(item.depth == 1 for item in duplicate.agenda) <= 1


def test_role_rotation_and_private_state_independence() -> None:
    iteration = campaign(max_questions=1).run(("Question",)).iterations[0]
    assert iteration.role_assignments[0].aion_role != iteration.role_assignments[1].aion_role
    refs = {item.peer: item.private_state_ref for item in iteration.interpretations}
    assert refs["AION"] != refs["ASTRA"]
    assert iteration.mapping_revealed_after_interpretations


def test_competing_explanations_and_not_evaluated_results_are_preserved() -> None:
    iteration = campaign(max_questions=1).run(("Question",)).iterations[0]
    kinds = {item["kind"] for item in iteration.competing_explanations}
    assert len(kinds) == 7
    assert {item["status"] for item in iteration.falsifier_results} >= {"NOT_TRIGGERED", "NOT_EVALUATED"}


def test_triggered_falsifier_cannot_be_suppressed() -> None:
    iteration = campaign(max_questions=1).run(("Triggered falsifier fixture",)).iterations[0]
    assert any(item["status"] == "TRIGGERED" for item in iteration.falsifier_results)
    assert iteration.governance.mechanism_status is MechanismStatus.CHALLENGED
    assert iteration.governance.scientific_disposition is ScientificDisposition.HOLD


def test_run_integrity_pass_does_not_promote_science_or_truth() -> None:
    report = campaign(max_questions=1).run(("Question",))
    iteration = report.iterations[0]
    assert iteration.governance.run_integrity is RunIntegrity.PASS
    assert iteration.governance.scientific_disposition is ScientificDisposition.HOLD
    assert report.scientific_disposition is ScientificDisposition.HOLD
    assert report.canonical_effect == "NONE"
    assert not report.deployment


def test_four_domain_and_five_question_output_is_complete() -> None:
    value = campaign(max_questions=1).run(("Question",)).iterations[0].four_domain
    assert value.DOMAIN_1_HUMAN_CONSTRUCT
    assert value.DOMAIN_2_MACHINE_QUESTION
    assert value.DOMAIN_3_ENGINEERING_OPERATION
    assert value.DOMAIN_4_GOVERNANCE_INTERPRETATION
    assert value.WHAT_WAS_OBSERVED
    assert value.WHAT_MECHANISM_IS_SUPPORTED
    assert value.WHAT_ALTERNATIVE_REMAINS
    assert value.WHAT_IS_NOT_ESTABLISHED
    assert value.WHAT_SHOULD_BE_TESTED_NEXT


def test_existing_bounded_loop_contract_is_reused_fail_closed() -> None:
    from aion_astra_autonomous_research import existing_loop_contract

    seam = existing_loop_contract()
    assert seam.owner_module == "aion_bounded_research_loop"
    assert seam.canonical_effect == "NONE"
    assert not seam.deployment
    assert not seam.autonomous_merge
    assert not seam.autonomous_repository_writeback


def test_campaign_api_has_no_repository_writeback_effect() -> None:
    before = tuple(sorted(path.as_posix() for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts))
    report = campaign(max_questions=1).run(("Question",))
    after = tuple(sorted(path.as_posix() for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts))
    assert before == after
    assert not report.autonomous_external_write
    assert not report.autonomous_authority_escalation
    assert not report.live_model_execution


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("max_questions", 21),
        ("max_experiments_per_question", 0),
        ("max_peer_rounds", 13),
        ("max_external_queries", 51),
        ("max_seeds", 0),
        ("max_follow_up_depth", 6),
        ("max_total_campaign_steps", 1001),
    ],
)
def test_limit_escalation_is_rejected(field: str, value: int) -> None:
    with pytest.raises(ValueError, match=field):
        replace(limits(), **{field: value})


def test_external_web_defaults_disabled() -> None:
    report = campaign(max_questions=1).run(("Question",))
    assert not report.external_web_enabled
    assert report.external_queries_used == 0


def test_external_web_requires_explicit_query_budget() -> None:
    with pytest.raises(ValueError, match="explicit positive"):
        BoundedAutonomousResearchCampaign(ROOT, repository_ref=HEAD, limits=limits(), external_web=True)
