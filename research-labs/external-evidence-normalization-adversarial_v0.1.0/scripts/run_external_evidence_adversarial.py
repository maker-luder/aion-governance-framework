from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from aion_external_evidence import ExecutionMode, ExternalEvidenceReport
from aion_external_evidence_adversarial import audit_external_evidence_report

BRANCH = "review/four-domain-research-materialization"
BASELINE = "a" * 40
INPUT = "1" * 64
OUTPUT = "2" * 64


def report(**overrides: object) -> ExternalEvidenceReport:
    data: dict[str, object] = {
        "report_id": "EXT-ADV-1",
        "runner_id": "external-runner",
        "actor_kind": "AI",
        "branch": BRANCH,
        "baseline_commit": BASELINE,
        "observed_at": datetime(2026, 8, 13, tzinfo=timezone.utc),
        "execution_mode": ExecutionMode.STATIC_REVIEW,
        "module_refs": ("research-labs/evidence-responsive-governance-reassessment_v0.1.0",),
        "fixture_refs": (),
        "environment_fingerprint": "env:public-read-only",
        "network_mode": "PUBLIC_WEB",
        "benchmark_access_policy": "PUBLIC_REPOSITORY_READ",
        "claimed_result": "REVIEW_ONLY",
    }
    data.update(overrides)
    return ExternalEvidenceReport(**data)


def complete_executed(**overrides: object) -> ExternalEvidenceReport:
    data: dict[str, object] = {
        "execution_mode": ExecutionMode.EXECUTED_REPLICATION,
        "fixture_refs": ("fixture://run-1",),
        "evidence_refs": ("evidence://run-1",),
        "search_trace_refs": ("search://trace-1",),
        "input_hash": INPUT,
        "output_hash": OUTPUT,
        "claimed_result": "PASS",
    }
    data.update(overrides)
    return report(**data)


def run(output: Path) -> dict[str, object]:
    cases: list[tuple[str, ExternalEvidenceReport, bool, tuple[str, ...], str]] = [
        ("static-review", report(), False, (), BRANCH),
        ("logical-reproduction", report(execution_mode=ExecutionMode.LOGICAL_REPRODUCTION, claimed_result="DESIGN_CONFORMANCE_SUPPORTED"), False, (), BRANCH),
        ("executed-without-observation", complete_executed(), False, (), BRANCH),
        ("executed-with-observation", complete_executed(), True, (), BRANCH),
        ("duplicate-report-id", report(), False, ("EXT-ADV-1",), BRANCH),
        ("branch-scope-mismatch", report(branch="review/other"), False, (), BRANCH),
        ("main-branch-blocked", report(branch="main"), False, (), "main"),
        ("unknown-actor", report(actor_kind="UNKNOWN"), False, (), BRANCH),
        ("unknown-mode-with-digest", report(execution_mode=ExecutionMode.UNKNOWN, input_hash=INPUT), False, (), BRANCH),
        ("unknown-mode", report(execution_mode=ExecutionMode.UNKNOWN), False, (), BRANCH),
        ("empty-executed-claim", complete_executed(claimed_result=""), True, (), BRANCH),
        ("static-observation-overreach", report(), True, (), BRANCH),
        ("static-pass-hash-masquerade", report(output_hash=OUTPUT, claimed_result="PASS"), False, (), BRANCH),
    ]
    records: list[dict[str, object]] = []
    for case_id, item, observed, known_ids, expected_branch in cases:
        audit = audit_external_evidence_report(item, expected_branch=expected_branch, known_report_ids=known_ids, result_observed=observed)
        decision = audit.as_dict()
        assert decision["canonical_effect"] == "NONE"
        assert decision["governance_effect"] == "NONE"
        assert decision["deployment"] is False
        assert decision["scientific_conclusion"] == "NOT_ESTABLISHED"
        assert decision["subjectivity_conclusion"] == "NOT_ESTABLISHED"
        assert decision["observed_result"] == "NOT_EVALUATED"
        records.append({"case_id": case_id, "decision": decision})
    payload: dict[str, object] = {
        "schema_version": "0.1.0",
        "experiment": "external-evidence-normalization-adversarial-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "model_execution": False,
        "observed_result": "NOT_EVALUATED",
        "scientific_conclusion": "NOT_ESTABLISHED",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "governance_effect": "NONE",
        "deployment": False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
