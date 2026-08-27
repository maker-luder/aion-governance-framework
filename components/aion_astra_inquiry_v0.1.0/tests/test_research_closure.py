from __future__ import annotations

from pathlib import Path

from aion_astra_inquiry.automation import AutonomousInquiryCampaign
from aion_astra_inquiry.research_campaign import (
    BoundedAutonomousResearchCampaign,
    research_campaign_to_dict,
    research_campaign_to_markdown,
    write_research_campaign_report,
)
from aion_astra_inquiry.research_closure import (
    BoundedResearchClosure,
    ResearchOperationKind,
    closure_to_dict,
    verify_research_closure,
)


def _research_repo(tmp_path: Path) -> Path:
    (tmp_path / "research-labs" / "closure-demo").mkdir(parents=True)
    (tmp_path / "docs").mkdir()
    (tmp_path / "research-labs" / "closure-demo" / "README.md").write_text(
        """# Closure demo

Research question: Does a persistent bounded state alter later goal selection?

The mechanism hypothesis is that persistent state can alter later selection under matched external conditions.
A falsifier is no reproducible difference under matched replay or state ablation.
""",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "counterevidence.md").write_text(
        "Counterexample evidence must test retrieval confounds, matched controls, replay, ablation, "
        "and alternative explanations before stronger interpretation.",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "replication.md").write_text(
        "Independent replication should hold prompt and external conditions fixed while changing only "
        "the candidate state or evidence partition.",
        encoding="utf-8",
    )
    return tmp_path


def _inquiry(tmp_path: Path):
    root = _research_repo(tmp_path)
    campaign = AutonomousInquiryCampaign(
        root,
        max_questions=1,
        max_rounds=2,
        evidence_limit=4,
        repository_ref="TEST_HEAD",
    ).run(("Does a persistent bounded state alter later goal selection?",))
    return root, campaign.reports[0]


def test_research_closure_executes_all_four_operation_types(tmp_path: Path) -> None:
    _, inquiry = _inquiry(tmp_path)
    closure = BoundedResearchClosure().close(inquiry)

    assert {item.kind for item in closure.operations} == {
        ResearchOperationKind.INTERVENTION,
        ResearchOperationKind.ABLATION,
        ResearchOperationKind.REPLAY,
        ResearchOperationKind.COUNTERFACTUAL,
    }
    assert len(closure.operations) == 4
    assert verify_research_closure(closure)
    assert closure.statistics.transcript_replay_passed is True
    assert closure.scientific_disposition == "HOLD"
    assert closure.canonical_effect == "NONE"
    assert closure.repository_mutation is False
    assert closure.deployment is False
    assert closure.autonomous_merge is False


def test_research_closure_materializes_four_domain_refs_and_statistics(tmp_path: Path) -> None:
    _, inquiry = _inquiry(tmp_path)
    closure = BoundedResearchClosure().close(inquiry)
    payload = closure_to_dict(closure)

    assert payload["statistics"]["evidence_count"] >= 1
    assert 0.0 <= payload["statistics"]["mean_lexical_overlap"] <= 1.0
    assert closure.four_domain.observation
    assert closure.four_domain.mechanism
    assert closure.four_domain.interpretation
    assert closure.four_domain.alternative_explanations
    assert closure.four_domain.robustness_refs
    assert closure.follow_up_question
    assert len(closure.closure_hash) == 64


def test_closed_loop_campaign_feeds_closure_follow_up_into_next_cycle(tmp_path: Path) -> None:
    root = _research_repo(tmp_path)
    campaign = BoundedAutonomousResearchCampaign(
        root,
        max_cycles=2,
        max_questions_per_cycle=1,
        max_rounds=1,
        evidence_limit=4,
        repository_ref="TEST_HEAD",
    ).run(("Does a persistent bounded state alter later goal selection?",))

    assert 1 <= len(campaign.cycles) <= 2
    assert campaign.cycles[0].closures
    if len(campaign.cycles) == 2:
        expected = campaign.cycles[0].closures[0].follow_up_question
        assert campaign.cycles[1].seed_questions == (expected,)
    assert campaign.full_automation is True
    assert campaign.full_authority is False
    assert campaign.repository_mutation is False
    assert campaign.network_access is False
    assert campaign.canonical_effect == "NONE"
    assert len(campaign.campaign_hash) == 64


def test_closed_loop_serialization_preserves_locked_boundaries(tmp_path: Path) -> None:
    root = _research_repo(tmp_path)
    campaign = BoundedAutonomousResearchCampaign(
        root,
        max_cycles=1,
        max_questions_per_cycle=1,
        max_rounds=1,
        repository_ref="TEST_HEAD",
    ).run(("Does a persistent bounded state alter later goal selection?",))

    payload = research_campaign_to_dict(campaign)
    markdown = research_campaign_to_markdown(campaign)

    assert payload["full_automation"] is True
    assert payload["full_authority"] is False
    assert payload["canonical_effect"] == "NONE"
    assert payload["repository_mutation"] is False
    assert "FULL_AUTOMATION != FULL_AUTHORITY" in markdown
    assert "RUN_INTEGRITY_PASS != SCIENTIFIC_TRUTH" in markdown
    assert "ENGINEERING_ANALOGUE != HUMAN_PSYCHOLOGY" in markdown
    assert "AUTONOMOUS_REPOSITORY_MUTATION = NO" in markdown


def test_closed_loop_report_writer_can_target_external_scratch(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    _research_repo(root)
    output = tmp_path / "scratch"
    campaign = BoundedAutonomousResearchCampaign(
        root,
        max_cycles=1,
        max_questions_per_cycle=1,
        max_rounds=1,
    ).run(("Does a persistent bounded state alter later goal selection?",))

    json_path, markdown_path = write_research_campaign_report(campaign, output)

    assert json_path.is_file()
    assert markdown_path.is_file()
    assert root not in json_path.parents
