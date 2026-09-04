#!/usr/bin/env python3
"""Run existing AION/Astra inquiry with an exact source-tree ref.

SOURCE_TREE_REF is the commit of the tree being inspected.
ARTIFACT_COMMIT is the later commit that stores generated reports.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "components/aion_astra_inquiry_v0.1.0/src"))

from aion_astra_inquiry import (  # noqa: E402
    AgentId,
    AutonomousInquiryCampaign,
    EvidenceDrivenReasoningProvider,
    InquiryCampaignReport,
    ProviderBackedPeer,
    campaign_to_dict,
    verify_transcript_chain,
    write_campaign_report,
)

QUESTION = (
    "In the current repository, what subjectivity-relevant observations remain from "
    "AION and Astra long-term interaction, correction, role, interpretation, and "
    "project continuity, and which of those observations are still explained by "
    "simpler engineering controls?"
)
_HEX40 = re.compile(r"^[0-9a-f]{40}$")
INQUIRY_COMPONENT_REF = "components/aion_astra_inquiry_v0.1.0"


def question_sha256(question: str = QUESTION) -> str:
    return hashlib.sha256(question.encode("utf-8")).hexdigest()


def runner_file_sha256(path: Path | None = None) -> str:
    target = path or Path(__file__).resolve()
    return hashlib.sha256(target.read_bytes()).hexdigest()


def resolve_source_tree_ref(root: Path, supplied: str | None = None) -> str:
    if supplied:
        value = supplied.strip().lower()
        if not _HEX40.fullmatch(value):
            raise ValueError("repository_ref must be exact lowercase 40-hex")
        return value
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    value = result.stdout.strip().lower()
    if result.returncode != 0 or not _HEX40.fullmatch(value):
        raise ValueError("SOURCE_TREE_REF could not be derived; supply --repository-ref")
    return value


def build_peers() -> tuple[ProviderBackedPeer, ProviderBackedPeer]:
    aion = ProviderBackedPeer(EvidenceDrivenReasoningProvider(AgentId.AION))
    astra = ProviderBackedPeer(EvidenceDrivenReasoningProvider(AgentId.ASTRA))
    if aion.agent_id is astra.agent_id:
        raise ValueError("AION and Astra must remain distinct AgentId values")
    if aion.agent_id is not AgentId.AION or astra.agent_id is not AgentId.ASTRA:
        raise ValueError("provider/agent binding mismatch")
    return aion, astra


def _require_campaign_integrity(campaign: InquiryCampaignReport, source_tree_ref: str) -> None:
    if campaign.repository_ref != source_tree_ref:
        raise ValueError("REPORT_REF != EXECUTION_SOURCE_TREE_REF")
    if campaign.canonical_effect != "NONE":
        raise ValueError("canonical_effect must remain NONE")
    for report in campaign.reports:
        if not verify_transcript_chain(report):
            raise ValueError("transcript hash chain failed")
        speakers = [event.speaker for event in report.transcript]
        expected: list[AgentId] = []
        while len(expected) < len(speakers):
            expected.extend([AgentId.AION, AgentId.ASTRA])
        if speakers != expected[: len(speakers)] or not speakers:
            raise ValueError("speakers are not alternating AION/Astra")
        if report.evidence and any(not item.retrieval_agent for item in report.evidence):
            raise ValueError("evidence attribution is missing")


def run_campaign(root: Path, *, source_tree_ref: str, max_rounds: int = 3) -> InquiryCampaignReport:
    if source_tree_ref in {"", "UNSPECIFIED"}:
        raise ValueError("repository_ref must not be UNSPECIFIED")
    campaign = AutonomousInquiryCampaign(
        root,
        max_questions=1,
        max_rounds=max_rounds,
        evidence_limit=4,
        repository_ref=source_tree_ref,
        external_web=False,
    ).run((QUESTION,))
    _require_campaign_integrity(campaign, source_tree_ref)
    return campaign


def execution_receipt(campaign: InquiryCampaignReport, *, source_tree_ref: str) -> dict[str, str]:
    report = campaign.reports[0]
    digest = report.final_chain_hash
    return {
        "SOURCE_TREE_REF": source_tree_ref,
        "ARTIFACT_COMMIT": "NOT_RECORDED_AT_EXECUTION",
        "SOURCE_TREE_REF != ARTIFACT_COMMIT": "TRUE",
        "RUNNER_FILE_SHA256": runner_file_sha256(),
        "INQUIRY_COMPONENT_REF": INQUIRY_COMPONENT_REF,
        "QUESTION_SHA256": question_sha256(),
        "CAMPAIGN_HASH": campaign.campaign_hash,
        "TRANSCRIPT_CHAIN": digest,
        "PRESERVED_EXECUTION_CHAIN_DIGEST": digest,
        "EVENT_LEVEL_RECOMPUTATION": "NOT_AVAILABLE",
        "BYTE_FAITHFUL_EXECUTED_TRANSCRIPT": "NOT_PRESERVED",
        "CAMPAIGN_JSON_COMPLETENESS": "PARTIAL",
        "NETWORK_MODE": campaign.external_network_mode,
        "CANONICAL_EFFECT": campaign.canonical_effect,
        "SCIENTIFIC_DISPOSITION": campaign.scientific_disposition,
        "RUNNER_DECLARED_REF": source_tree_ref,
        "REPORT_REF": campaign.repository_ref,
    }


def write_derived_artifacts(campaign: InquiryCampaignReport, destination: Path) -> tuple[Path, Path, Path]:
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="aion-astra-inquiry-") as raw:
        json_path, markdown_path = write_campaign_report(campaign, Path(raw))
        dest_json = destination / "campaign.json"
        dest_md = destination / "campaign.md"
        shutil.copyfile(json_path, dest_json)
        shutil.copyfile(markdown_path, dest_md)
    receipt = execution_receipt(campaign, source_tree_ref=campaign.repository_ref)
    receipt_path = destination / "EXECUTION_RECEIPT.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return dest_json, dest_md, receipt_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bounded AION/Astra inquiry runner with exact source-tree ref")
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--repository-ref", default="")
    parser.add_argument("--max-rounds", type=int, default=3)
    parser.add_argument("--write-sandbox-derived", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    source_tree_ref = resolve_source_tree_ref(root, args.repository_ref or None)
    campaign = run_campaign(root, source_tree_ref=source_tree_ref, max_rounds=args.max_rounds)
    payload = campaign_to_dict(campaign)
    receipt = execution_receipt(campaign, source_tree_ref=source_tree_ref)
    if args.write_sandbox_derived:
        write_derived_artifacts(campaign, HERE)
    print(json.dumps({
        "receipt": receipt,
        "speakers": [
            event["speaker"]
            for report in payload["reports"]
            for event in report["transcript"]
        ],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
