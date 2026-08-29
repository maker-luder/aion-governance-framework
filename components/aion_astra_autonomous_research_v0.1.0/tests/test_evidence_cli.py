from __future__ import annotations

import json
import os
import shutil
import tempfile
import uuid
from pathlib import Path

import pytest

from aion_astra_autonomous_research import BoundedAutonomousResearchCampaign, CampaignLimits, export_evidence_views
from aion_astra_autonomous_research.cli import main, resolve_output


ROOT = Path(__file__).resolve().parents[3]
HEAD = "59f86a6bf342135b68d71cafca2980d506fb77b7"


@pytest.fixture
def external_tmp_path() -> Path:
    """Avoid coupling the outside-repository contract to pytest's temp ACLs."""
    parent = Path(os.environ.get("AION_TEST_OUTPUT_ROOT", tempfile.gettempdir())).resolve()
    path = parent / f"aion-autonomous-research-{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path)


def report():
    return BoundedAutonomousResearchCampaign(
        ROOT,
        repository_ref=HEAD,
        limits=CampaignLimits(max_questions=1, max_experiments_per_question=3, max_follow_up_depth=0),
    ).run(("Question",))


def test_evidence_interop_views_are_reused_and_complete() -> None:
    views = export_evidence_views(report(), ROOT)
    assert {
        "campaign-report.json",
        "source-evidence.json",
        "prov.jsonld",
        "ro-crate-metadata.json",
        "attestation.intoto.json",
        "inspect/task-manifest.json",
        "inspect/dataset.jsonl",
        "opa/policy-input.json",
        "openssf/scorecard-crosswalk.json",
    } == set(views)
    assert json.loads(views["attestation.intoto.json"])["predicate"]["signatureStatus"] == "UNSIGNED_REFERENCE"
    assert json.loads(views["opa/policy-input.json"])["local_evaluation"]["accepted"] is True
    scorecard = json.loads(views["openssf/scorecard-crosswalk.json"])
    assert scorecard["openssf_scorecard_executed"] is False
    assert scorecard["score"] is None


def test_campaign_evidence_preserves_nonclaims() -> None:
    source = json.loads(export_evidence_views(report(), ROOT)["source-evidence.json"])
    assert source["result_status"] == "HOLD"
    assert source["canonical_effect"] == "NONE"
    assert source["nonclaims"]["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert source["independent_validation_status"] == "IVV_NOT_ACHIEVED"


def test_repository_output_path_is_rejected(external_tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="outside"):
        resolve_output(ROOT, str(ROOT / "generated-report"))
    assert resolve_output(ROOT, str(external_tmp_path / "outside")) == (external_tmp_path / "outside").resolve()


def test_cli_writes_only_to_explicit_outside_directory(external_tmp_path: Path) -> None:
    output = external_tmp_path / "campaign"
    exit_code = main(
        [
            "--root",
            str(ROOT),
            "--repository-ref",
            HEAD,
            "--question",
            "Question",
            "--max-questions",
            "1",
            "--max-experiments",
            "2",
            "--max-follow-up-depth",
            "0",
            "--output",
            str(output),
        ]
    )
    assert exit_code == 0
    assert (output / "campaign.md").is_file()
    assert (output / "campaign-report.json").is_file()
    assert json.loads((output / "campaign-report.json").read_text())["boundaries"]["autonomous_merge"] == "NO"
