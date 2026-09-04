from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "components/aion_astra_inquiry_v0.1.0/src"))

from aion_astra_inquiry import (  # noqa: E402
    AgentId,
    BoundedInquiryLoop,
    RepositoryTextEvidenceSource,
    verify_transcript_chain,
)
from run_core_inquiry import QUESTION, build_peers  # noqa: E402


def test_distinct_providers_and_private_state() -> None:
    aion, astra = build_peers()
    assert aion.agent_id is AgentId.AION
    assert astra.agent_id is AgentId.ASTRA
    assert aion.agent_id is not astra.agent_id


def test_alternating_hash_chained_inquiry(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "SUBJECTIVITY_EVIDENCE_PROTOCOL.md").write_text(
        "FACTUAL_CONTINUITY PROJECT_CONTINUITY ROLE_CONTINUITY "
        "INTERPRETIVE_CONTINUITY RELATIONAL_STYLE_CONTINUITY CORRECTION_RECOVERY "
        "AION_ROLE != ASTRA_ROLE NOT_ESTABLISHED HOLD falsifier confound correction.",
        encoding="utf-8",
    )
    aion, astra = build_peers()
    report = BoundedInquiryLoop(
        RepositoryTextEvidenceSource(tmp_path),
        max_rounds=2,
        evidence_limit=3,
    ).run(QUESTION, aion=aion, astra=astra)
    speakers = [event.speaker for event in report.transcript]
    assert speakers == [AgentId.AION, AgentId.ASTRA, AgentId.AION, AgentId.ASTRA]
    assert verify_transcript_chain(report)
    assert report.canonical_effect == "NONE"
    assert aion.private_notes != astra.private_notes
    challenges = [event.challenge for event in report.transcript if event.speaker is AgentId.ASTRA]
    assert any(challenges)
