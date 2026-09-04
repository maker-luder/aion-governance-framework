#!/usr/bin/env python3
"""Run the existing AION/Astra inquiry machinery. Does not invent a second loop."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "components/aion_astra_inquiry_v0.1.0/src"))

from aion_astra_inquiry import (  # noqa: E402
    AgentId,
    AutonomousInquiryCampaign,
    EvidenceDrivenReasoningProvider,
    ProviderBackedPeer,
    campaign_to_dict,
    verify_transcript_chain,
)

QUESTION = (
    "In the current repository, what subjectivity-relevant observations remain from "
    "AION and Astra long-term interaction, correction, role, interpretation, and "
    "project continuity, and which of those observations are still explained by "
    "simpler engineering controls?"
)


def build_peers() -> tuple[ProviderBackedPeer, ProviderBackedPeer]:
    aion = ProviderBackedPeer(EvidenceDrivenReasoningProvider(AgentId.AION))
    astra = ProviderBackedPeer(EvidenceDrivenReasoningProvider(AgentId.ASTRA))
    if aion.agent_id is astra.agent_id:
        raise ValueError("AION and Astra must remain distinct AgentId values")
    if aion.agent_id is not AgentId.AION or astra.agent_id is not AgentId.ASTRA:
        raise ValueError("provider/agent binding mismatch")
    return aion, astra


def run_campaign(root: Path, *, max_rounds: int = 3) -> dict:
    campaign = AutonomousInquiryCampaign(
        root,
        max_questions=1,
        max_rounds=max_rounds,
        evidence_limit=4,
        repository_ref="UNSPECIFIED",
        external_web=False,
    ).run((QUESTION,))
    payload = campaign_to_dict(campaign)
    reports = getattr(campaign, "reports", ())
    if reports and not verify_transcript_chain(reports[0]):
        raise ValueError("transcript hash chain failed")
    return payload


def main() -> int:
    payload = run_campaign(ROOT)
    print(json.dumps({
        "campaign_hash": payload.get("campaign_hash"),
        "scientific_disposition": payload.get("scientific_disposition"),
        "canonical_effect": payload.get("canonical_effect"),
        "speakers": [
            event["speaker"]
            for report in payload.get("reports", [])
            for event in report.get("transcript", [])
        ],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
