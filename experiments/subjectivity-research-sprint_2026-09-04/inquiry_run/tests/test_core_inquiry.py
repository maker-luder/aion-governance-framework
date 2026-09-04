from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "components/aion_astra_inquiry_v0.1.0/src"))

from aion_astra_inquiry import AgentId, campaign_to_dict  # noqa: E402
from run_core_inquiry import (  # noqa: E402
    QUESTION,
    build_peers,
    execution_receipt,
    resolve_source_tree_ref,
    run_campaign,
    write_derived_artifacts,
)

FIXED_REF = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


def _tiny_repo(tmp_path: Path) -> Path:
    docs = tmp_path / "docs"
    docs.mkdir(parents=True)
    (docs / "SUBJECTIVITY_EVIDENCE_PROTOCOL.md").write_text(
        "FACTUAL_CONTINUITY PROJECT_CONTINUITY ROLE_CONTINUITY "
        "INTERPRETIVE_CONTINUITY RELATIONAL_STYLE_CONTINUITY CORRECTION_RECOVERY "
        "AION_ROLE != ASTRA_ROLE NOT_ESTABLISHED HOLD falsifier confound correction.",
        encoding="utf-8",
    )
    return tmp_path


def test_distinct_providers() -> None:
    aion, astra = build_peers()
    assert aion.agent_id is AgentId.AION
    assert astra.agent_id is AgentId.ASTRA
    assert aion.agent_id is not astra.agent_id


def test_ref_must_be_exact_hex() -> None:
    try:
        resolve_source_tree_ref(Path("/tmp"), "UNSPECIFIED")
    except ValueError:
        return
    raise AssertionError("UNSPECIFIED must be rejected")


def test_report_ref_matches_execution_ref(tmp_path: Path) -> None:
    root = _tiny_repo(tmp_path / "repo")
    campaign = run_campaign(root, source_tree_ref=FIXED_REF, max_rounds=2)
    assert campaign.repository_ref == FIXED_REF
    receipt = execution_receipt(campaign, source_tree_ref=FIXED_REF)
    assert receipt["RUNNER_DECLARED_REF"] == receipt["REPORT_REF"] == FIXED_REF
    assert receipt["CANONICAL_EFFECT"] == "NONE"
    payload = campaign_to_dict(campaign)
    report = payload["reports"][0]
    speakers = [event["speaker"] for event in report["transcript"]]
    assert speakers == ["AION", "ASTRA", "AION", "ASTRA"]
    assert all(item["retrieval_agent"] for item in report["evidence"])
    assert report["final_chain_hash"] == receipt["TRANSCRIPT_CHAIN"]
    out = tmp_path / "out"
    json_path, md_path, receipt_path = write_derived_artifacts(campaign, out)
    written = json.loads(json_path.read_text(encoding="utf-8"))
    assert written["repository_ref"] == FIXED_REF
    assert "Question:" in md_path.read_text(encoding="utf-8")
    assert json.loads(receipt_path.read_text(encoding="utf-8"))["SOURCE_TREE_REF"] == FIXED_REF
    assert QUESTION in written["reports"][0]["question"]
    event = written["reports"][0]["transcript"][0]
    for key in ("claim", "challenge", "evidence_query", "evidence_refs", "event_hash", "speaker"):
        assert key in event


def test_mismatched_ref_is_rejected_by_integrity_check(tmp_path: Path) -> None:
    root = _tiny_repo(tmp_path / "repo")
    campaign = run_campaign(root, source_tree_ref=FIXED_REF, max_rounds=2)
    from run_core_inquiry import _require_campaign_integrity

    try:
        _require_campaign_integrity(campaign, "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
    except ValueError as exc:
        assert "REPORT_REF" in str(exc)
        return
    raise AssertionError("mismatched ref must fail")
