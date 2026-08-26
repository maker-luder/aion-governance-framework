from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from aion_astra_inquiry import AgentId, AutonomousInquiryCampaign, EvidenceItem, campaign_to_dict, campaign_to_markdown


class StubExternalEvidence:
    def __init__(self) -> None:
        self.requesters: list[AgentId | None] = []

    def search(
        self,
        query: str,
        limit: int = 5,
        requester: AgentId | None = None,
    ) -> tuple[EvidenceItem, ...]:
        self.requesters.append(requester)
        if limit <= 0 or not query.strip():
            return ()
        agent = requester.value if requester else "UNSPECIFIED"
        body = f"External matched-control evidence for {agent}: {query}".encode()
        return (
            EvidenceItem(
                ref=f"external:https://evidence.example/{agent.lower()}",
                excerpt="[UNTRUSTED_EXTERNAL_EVIDENCE] matched controls are reported externally",
                content_sha256=sha256(body).hexdigest(),
                source_class="EXTERNAL_WEB",
                source_url=f"https://evidence.example/{agent.lower()}",
                publisher="evidence.example",
                retrieved_at="2026-08-26T00:00:00+00:00",
                retrieval_agent=agent,
                trust="UNTRUSTED_EXTERNAL",
            ),
        )


def test_campaign_federates_independent_aion_and_astra_external_retrieval(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "evidence.md").write_text(
        "Persistent internal state requires matched controls and counterexample checks.",
        encoding="utf-8",
    )
    external = StubExternalEvidence()
    campaign = AutonomousInquiryCampaign(
        tmp_path,
        max_questions=1,
        max_rounds=1,
        evidence_limit=4,
        repository_ref="TEST_HEAD",
        external_evidence_source=external,
    ).run(("Does persistent internal state alter goal selection under matched controls?",))

    assert campaign.network_access is True
    assert campaign.external_network_mode == "GOVERNED_READ_ONLY"
    assert campaign.run_mode == "FEDERATED_READ_ONLY"
    assert AgentId.AION in external.requesters
    assert AgentId.ASTRA in external.requesters
    external_items = [item for item in campaign.reports[0].evidence if item.source_class == "EXTERNAL_WEB"]
    assert {item.retrieval_agent for item in external_items} == {"AION", "ASTRA"}
    payload = campaign_to_dict(campaign)
    markdown = campaign_to_markdown(campaign)
    assert payload["repository_mutation"] is False
    assert payload["autonomous_merge"] is False
    assert "AUTONOMOUS_EXTERNAL_WEB_READ = GOVERNED" in markdown
    assert "EXTERNAL_TEXT != AUTHORITY" in markdown
