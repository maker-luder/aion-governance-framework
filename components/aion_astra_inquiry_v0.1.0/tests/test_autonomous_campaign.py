from __future__ import annotations

from pathlib import Path

import pytest

from aion_astra_inquiry import (
    AgentId,
    AutonomousInquiryCampaign,
    EvidenceDrivenReasoningProvider,
    InquiryContext,
    ProviderBackedPeer,
    RepositoryQuestionGenerator,
    campaign_to_dict,
    campaign_to_markdown,
    verify_transcript_chain,
    write_campaign_report,
)
from aion_astra_inquiry.cli import _resolve_output


def _research_repo(tmp_path: Path) -> Path:
    (tmp_path / "research-labs" / "demo").mkdir(parents=True)
    (tmp_path / "docs").mkdir()
    (tmp_path / "research-labs" / "demo" / "README.md").write_text(
        """# Demo research\n\nResearch question: Does persistent internal state alter bounded goal selection?\n\nScientific disposition: `HOLD`\n\nA falsifier is failure under matched external conditions. Memory confound must remain externally controlled.\n""",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "controls.md").write_text(
        "Matched control evidence requires equal prompt, memory manifest, candidate universe, and provider identity. "
        "Ablation and counterexample checks remain necessary.",
        encoding="utf-8",
    )
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "private.txt").write_text(
        "Does a hidden file become a research question?",
        encoding="utf-8",
    )
    return tmp_path


def test_question_generator_discovers_repository_question_without_git_leak(tmp_path: Path) -> None:
    root = _research_repo(tmp_path)

    questions = RepositoryQuestionGenerator(root).discover(limit=4)

    assert questions
    assert any("persistent internal state" in item.question.lower() for item in questions)
    assert all(not item.source_ref.startswith(".git/") for item in questions)


def test_question_generator_ignores_code_syntax_and_its_own_examples(tmp_path: Path) -> None:
    root = _research_repo(tmp_path)
    (root / "scripts").mkdir()
    (root / "scripts" / "helper.py").write_text(
        'cleaned = cleaned[: cleaned.find("?") + 1]\n',
        encoding="utf-8",
    )
    own = root / "components" / "aion_astra_inquiry_v0.1.0"
    own.mkdir(parents=True)
    (own / "README.md").write_text(
        '--question "Which current evidence most strongly challenges the working mechanism?"\n',
        encoding="utf-8",
    )

    questions = RepositoryQuestionGenerator(root).discover(limit=4)

    assert questions[0].source_ref.startswith("research-labs/demo/")
    assert all("aion_astra_inquiry_v0.1.0" not in item.source_ref for item in questions)
    assert all("scripts/helper.py" not in item.source_ref for item in questions)
    assert all("cleaned.find" not in item.question for item in questions)


def test_independent_reasoning_peers_run_without_scripted_contributions(tmp_path: Path) -> None:
    root = _research_repo(tmp_path)
    campaign = AutonomousInquiryCampaign(
        root,
        max_questions=1,
        max_rounds=2,
        evidence_limit=4,
        repository_ref="TEST_HEAD",
    )

    report = campaign.run(("Does persistent internal state alter bounded goal selection?",))

    assert len(report.reports) == 1
    inquiry = report.reports[0]
    assert [event.speaker for event in inquiry.transcript] == [
        AgentId.AION,
        AgentId.ASTRA,
        AgentId.AION,
        AgentId.ASTRA,
    ]
    assert inquiry.evidence
    assert verify_transcript_chain(inquiry)
    assert campaign.aion_private_notes
    assert campaign.astra_private_notes
    assert campaign.aion_private_notes != campaign.astra_private_notes


def test_campaign_can_derive_follow_up_question_with_hard_budget(tmp_path: Path) -> None:
    root = _research_repo(tmp_path)
    campaign = AutonomousInquiryCampaign(root, max_questions=2, max_rounds=1, repository_ref="TEST_HEAD")

    report = campaign.run(("What evidence constrains the demo mechanism?",))

    assert 1 <= len(report.reports) <= 2
    assert len(report.reports) == len(report.questions_considered)
    assert report.scientific_disposition == "HOLD"
    assert report.canonical_effect == "NONE"
    assert report.repository_mutation is False
    assert report.network_access is False
    assert report.deployment is False
    assert report.autonomous_merge is False
    assert len(report.campaign_hash) == 64


def test_campaign_serialization_preserves_authority_boundary(tmp_path: Path) -> None:
    root = _research_repo(tmp_path)
    campaign = AutonomousInquiryCampaign(root, max_questions=1, max_rounds=1, repository_ref="TEST_HEAD").run(
        ("What evidence constrains the demo mechanism?",)
    )

    payload = campaign_to_dict(campaign)
    markdown = campaign_to_markdown(campaign)

    assert payload["canonical_effect"] == "NONE"
    assert payload["repository_mutation"] is False
    assert payload["network_access"] is False
    assert payload["autonomous_merge"] is False
    assert "PEER_CONSENSUS != SCIENTIFIC_TRUTH" in markdown
    assert "AUTONOMOUS_REPOSITORY_MUTATION = NO" in markdown


def test_report_writer_is_explicit_and_can_target_non_repository_scratch(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    _research_repo(root)
    output = tmp_path / "scratch"
    campaign = AutonomousInquiryCampaign(root, max_questions=1, max_rounds=1).run(
        ("What evidence constrains the demo mechanism?",)
    )

    json_path, markdown_path = write_campaign_report(campaign, output)

    assert json_path.is_file()
    assert markdown_path.is_file()
    assert root not in json_path.parents


def test_cli_output_path_rejects_repository_writeback(tmp_path: Path) -> None:
    root = _research_repo(tmp_path)

    with pytest.raises(ValueError, match="outside the repository"):
        _resolve_output(root, str(root / "generated"))


def test_provider_binding_rejects_cross_agent_use() -> None:
    peer = ProviderBackedPeer(EvidenceDrivenReasoningProvider(AgentId.AION))
    context = InquiryContext(
        question="What is bounded?",
        round_index=1,
        speaker=AgentId.ASTRA,
        peer=AgentId.AION,
        transcript=(),
        evidence=(),
    )

    with pytest.raises(ValueError, match="wrong inquiry speaker"):
        peer.contribute(context)
