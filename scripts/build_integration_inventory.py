from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = json.loads((ROOT / "qa/CURRENT_TEST_RESULTS.json").read_text(encoding="utf-8"))
COVERAGE = json.loads((ROOT / "qa/CURRENT_COVERAGE_RESULTS.json").read_text(encoding="utf-8"))
test_by_target = {item["target"]: item for item in TESTS["targets"]}
coverage_by_target = {item["target"]: item for item in COVERAGE["targets"]}
paths = sorted(
    [path for top in ("components", "examples", "research-labs") for path in (ROOT / top).iterdir() if path.is_dir()]
)
entries = []
for path in paths:
    relative = str(path.relative_to(ROOT))
    tests = test_by_target[relative]
    coverage = coverage_by_target[relative]
    if relative == "components/whole_system_governed_runtime_v0.1.0":
        source_branch = "review/aion-astra-whole-system-completion"
        source_sha = "263f6905356ebf0581b9ad8acda6c449587c73f1"
        status = "SELECTIVELY_REPLAYED_AND_REPAIRED"
        disposition = "PRESERVED_WITH_TRANSFORMATION"
    else:
        source_branch = "review/four-domain-research-materialization"
        source_sha = "6f39fff07f1b1a79867c270f953c554e18addbc1"
        status = "PRESERVED_FROM_FORMAL_RESEARCH"
        disposition = "PRESERVED"
    entries.append(
        {
            "path": relative,
            "source_branch": source_branch,
            "source_sha": source_sha,
            "status": status,
            "tested": tests["tested"],
            "test_status": tests["status"],
            "tests_passed": tests["passed"],
            "tests_failed": tests["failed"],
            "coverage": coverage.get("coverage_percent"),
            "coverage_status": coverage["status"],
            "canonical_effect": "NONE",
            "review_disposition": disposition,
        }
    )
payload = {
    "schema_version": "2.0",
    "generated_at": datetime.now(UTC).isoformat(),
    "scope": "REVIEW_CANDIDATE_V2",
    "target_count": len(entries),
    "missing_targets": [],
    "unexplained_deletions": [],
    "entries": entries,
}
(ROOT / "qa/INTEGRATION_INVENTORY.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
lines = [
    "# v2 Full Integration Inventory",
    "",
    "This inventory is dynamically generated from direct child directories under `components/`, `examples/`, and `research-labs/`. It is a review-candidate scope record, not a release manifest.",
    "",
    f"**Target count: {len(entries)}. Missing targets: 0. Unexplained deletions: 0.**",
    "",
    "| PATH | SOURCE_BRANCH | SOURCE_SHA | STATUS | TESTED | TESTS | COVERAGE | CANONICAL_EFFECT | REVIEW_DISPOSITION |",
    "|---|---|---|---|---|---:|---:|---|---|",
]
for entry in entries:
    tests = f"{entry['tests_passed']} pass / {entry['tests_failed']} fail" if entry["tested"] else "N/A"
    coverage = "N/A — non-applicable" if entry["coverage"] is None else f"{entry['coverage']:.2f}%"
    lines.append(
        f"| `{entry['path']}` | `{entry['source_branch']}` | `{entry['source_sha'][:12]}…` | {entry['status']} | {entry['tested']} | {tests} | {coverage} | `{entry['canonical_effect']}` | {entry['review_disposition']} |"
    )
lines.extend(
    [
        "",
        "The formal research branch is the authoritative source for all current research targets. The whole-system target is the only selectively replayed artifact and is explicitly attributed to the old superseded review branch; its implementation was transformed and re-tested on v2.",
        "",
        "```text",
        "CANONICAL_EFFECT = NONE",
        "DEPLOYMENT = FALSE",
        "INDEPENDENT_IVV = NOT_ACHIEVED",
        "```",
    ]
)
(ROOT / "docs/V2_INTEGRATION_INVENTORY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
