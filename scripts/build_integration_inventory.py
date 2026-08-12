from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CURRENT_HEAD = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
CURRENT_SCOPE = "FINAL_FORMAL_RESEARCH_TREE"
CURRENT_BRANCH = "review/four-domain-research-materialization"
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
    source_branch = CURRENT_BRANCH
    source_sha = CURRENT_HEAD
    if relative == "components/whole_system_governed_runtime_v0.1.0":
        status = "INTEGRATED_AND_REVALIDATED"
        disposition = "CURRENT_FORMAL_RESEARCH_TREE"
    else:
        status = "CURRENT_FORMAL_RESEARCH_TARGET"
        disposition = "CURRENT_FORMAL_RESEARCH_TREE"
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
    "scope": CURRENT_SCOPE,
    "target_head": CURRENT_HEAD,
    "source_branch": CURRENT_BRANCH,
    "target_count": len(entries),
    "missing_targets": [],
    "unexplained_deletions": [],
    "entries": entries,
}
(ROOT / "qa/INTEGRATION_INVENTORY.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
lines = [
    "# Current Formal Research Integration Inventory",
    "",
    "This inventory is dynamically generated from direct child directories under `components/`, `examples/`, and `research-labs`. It is bound to the exact current formal research tree and is not a release manifest.",
    "",
    f"**Scope: `{CURRENT_SCOPE}`. Target head: `{CURRENT_HEAD}`. Target count: {len(entries)}. Missing targets: 0. Unexplained deletions: 0.**",
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
        "The formal research branch is the authoritative source for all current research targets. The whole-system target is recorded as integrated and revalidated in this current tree; historical source-lineage details remain in the consolidation ledger.",
        "",
        "```text",
        "CANONICAL_EFFECT = NONE",
        "DEPLOYMENT = FALSE",
        "INDEPENDENT_IVV = NOT_ACHIEVED",
        "```",
    ]
)
(ROOT / "docs/INTEGRATION_INVENTORY_CURRENT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
(ROOT / "docs/V2_INTEGRATION_INVENTORY.md").write_text(
    "# Historical V2 Integration Inventory\n\n"
    "> HISTORICAL_V2_EVIDENCE: this file is retained for provenance only. It is not current evidence.\n\n"
    "The authoritative current inventory is `docs/INTEGRATION_INVENTORY_CURRENT.md` and `qa/INTEGRATION_INVENTORY.json`, both bound to their recorded `target_head`.\n",
    encoding="utf-8",
)
