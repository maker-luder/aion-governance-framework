from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "research-workbench/autonomous-growth/AUTONOMOUS_GROWTH_CONTRACT.json"
CYCLE_DIR = ROOT / "research-workbench/autonomous-growth/cycles"
MARKER_PATH = ROOT / "AUTONOMOUS_RESEARCH_GROWTH.md"
CHARTER_PATH = ROOT / "research-workbench/four-domain-materialization/2026-08-12/AUTONOMOUS_RESEARCH_GROWTH_CHARTER_2026-08-12.md"
LEDGER_PATH = ROOT / "research-workbench/autonomous-growth/AUTONOMOUS_GROWTH_LEDGER.md"
RESEARCH_BRANCH = "review/four-domain-research-materialization"
WORKFLOWS = (
    ROOT / ".github/workflows/research-scope-lock.yml",
    ROOT / ".github/workflows/research-workbench-ci.yml",
)


def _fail(message: str) -> None:
    raise ValueError(message)


def _load(path: Path) -> dict:
    if not path.is_file():
        _fail(f"missing required JSON: {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        _fail(f"expected JSON object: {path.relative_to(ROOT)}")
    return value


def _require_text(path: Path, needles: tuple[str, ...]) -> None:
    if not path.is_file():
        _fail(f"missing required document: {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        _fail(f"{path.relative_to(ROOT)} missing invariants: {missing}")


def validate_contract(contract: dict) -> None:
    if contract.get("schema_version") != "1.1.0":
        _fail("autonomous growth contract schema drift")
    if contract.get("base_branch") != RESEARCH_BRANCH:
        _fail("autonomous base branch drift")
    if contract.get("protected_branches") != ["main"]:
        _fail("main must remain the protected autonomous-growth boundary")
    expected_roles = {"HYPOTHESIS", "MEASUREMENT", "FALSIFIER", "EXPERIMENTAL_SUBSTRATE", "ENABLING_ONLY"}
    if set(contract.get("permitted_epistemic_roles", [])) != expected_roles:
        _fail("permitted epistemic roles drift")

    premerge = contract.get("premerge_policy")
    expected_premerge = {
        "target_branch": RESEARCH_BRANCH,
        "required_workflows": ["Research Scope Lock", "Research Workbench CI"],
        "require_green_before_integration": True,
        "pull_request_target_event": False,
    }
    if premerge != expected_premerge:
        _fail("autonomous premerge policy drift")

    effects = contract.get("effects")
    if effects != {"main": "NONE", "canonical": "NONE", "runtime": "NONE", "deployment": "NONE"}:
        _fail("autonomous effects must all remain NONE")
    promotions = contract.get("automatic_promotions", {})
    if not promotions or any(value is not False for value in promotions.values()):
        _fail("all automatic promotions must remain false")


def validate_cycle(record: dict, contract: dict, path: Path) -> None:
    required = set(contract["required_cycle_fields"])
    if set(record) != required:
        _fail(f"{path.name} fields differ from contract: expected {sorted(required)}")
    try:
        timestamp = datetime.fromisoformat(record["started_at"].replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{path.name} started_at is not ISO-8601") from exc
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        _fail(f"{path.name} started_at must include timezone")
    if not re.fullmatch(r"[0-9a-f]{40}", record["starting_research_sha"]):
        _fail(f"{path.name} starting_research_sha must be a full commit SHA")
    if record["epistemic_role"] not in contract["permitted_epistemic_roles"]:
        _fail(f"{path.name} has unsupported epistemic role")
    if record["result_class"] not in contract["allowed_result_classes"]:
        _fail(f"{path.name} has unsupported result class")
    if record["integration_status"] not in contract["allowed_integration_statuses"]:
        _fail(f"{path.name} has unsupported integration status")
    if not record["candidate_branch"].startswith(contract["candidate_branch_prefix"]):
        _fail(f"{path.name} candidate branch must use autogrow/ prefix")
    for field in ("source_refs", "changed_paths", "hold_items"):
        value = record[field]
        if not isinstance(value, list) or len(value) != len(set(value)):
            _fail(f"{path.name} {field} must be a unique list")
    if not record["source_refs"]:
        _fail(f"{path.name} requires at least one source reference")
    validation = record["validation"]
    if set(validation) != {"commands", "outcomes"}:
        _fail(f"{path.name} validation must contain commands and outcomes")
    if not validation["commands"] or not validation["outcomes"]:
        _fail(f"{path.name} validation cannot be empty")
    if any(Path(item).is_absolute() or ".." in Path(item).parts for item in record["changed_paths"]):
        _fail(f"{path.name} changed paths must be repository-relative")
    if any(item == "main" or item.startswith("refs/heads/main") for item in record["changed_paths"]):
        _fail(f"{path.name} cannot describe main mutation")


def validate_workflows(contract: dict) -> None:
    pin_pattern = re.compile(r"uses:\s+actions/(checkout|setup-python)@([0-9a-f]{40})")
    floating_pattern = re.compile(r"uses:\s+actions/(checkout|setup-python)@v\d+")
    required_names = set(contract["premerge_policy"]["required_workflows"])
    observed_names: set[str] = set()

    for path in WORKFLOWS:
        text = path.read_text(encoding="utf-8")
        first_line = text.splitlines()[0] if text else ""
        if not first_line.startswith("name: "):
            _fail(f"{path.relative_to(ROOT)} must declare workflow name")
        observed_names.add(first_line.removeprefix("name: ").strip())

        if "pull_request_target:" in text:
            _fail(f"{path.relative_to(ROOT)} must not use pull_request_target")
        if "pull_request:" not in text:
            _fail(f"{path.relative_to(ROOT)} must run for pull requests")
        if text.count(RESEARCH_BRANCH) < 2:
            _fail(f"{path.relative_to(ROOT)} must cover both research-branch push and PR target")
        if floating_pattern.search(text):
            _fail(f"{path.relative_to(ROOT)} contains a floating first-party action tag")
        kinds = {match.group(1) for match in pin_pattern.finditer(text)}
        if kinds != {"checkout", "setup-python"}:
            _fail(f"{path.relative_to(ROOT)} must pin checkout and setup-python to full SHAs")
        if "persist-credentials: false" not in text:
            _fail(f"{path.relative_to(ROOT)} must disable checkout credential persistence")
        if "permissions:\n  contents: read" not in text:
            _fail(f"{path.relative_to(ROOT)} must keep contents read-only")

    if observed_names != required_names:
        _fail(f"required premerge workflow set drift: {sorted(observed_names)}")


def main() -> int:
    contract = _load(CONTRACT_PATH)
    validate_contract(contract)
    _require_text(
        MARKER_PATH,
        (
            "BASE_BRANCH = review/four-domain-research-materialization",
            "MAIN_WRITE = PROHIBITED",
            "CANONICAL_PROMOTION = PROHIBITED",
            "DEPLOYMENT = PROHIBITED",
        ),
    )
    _require_text(
        CHARTER_PATH,
        (
            "MAIN_TARGET = PROHIBITED",
            "FORCE_PUSH = PROHIBITED",
            "HISTORY_REWRITE = PROHIBITED",
            "LATER_HUMAN_REVIEW = REQUIRED_FOR_PROMOTION",
            "PREMERGE_RESEARCH_GATES = REQUIRED",
        ),
    )
    _require_text(
        LEDGER_PATH,
        (
            "starting research-branch SHA",
            "negative/null/contradictory results",
            "unresolved HOLD items",
            "No cycle entry is a scientific promotion record.",
        ),
    )
    validate_workflows(contract)
    cycle_count = 0
    if CYCLE_DIR.is_dir():
        for path in sorted(CYCLE_DIR.glob("*.json")):
            validate_cycle(_load(path), contract, path)
            cycle_count += 1
    print(
        json.dumps(
            {
                "status": "PASS",
                "base_branch": contract["base_branch"],
                "premerge_target": contract["premerge_policy"]["target_branch"],
                "required_premerge_workflows": contract["premerge_policy"]["required_workflows"],
                "protected_branches": contract["protected_branches"],
                "validated_cycle_records": cycle_count,
                "main_effect": contract["effects"]["main"],
                "canonical_effect": contract["effects"]["canonical"],
                "runtime_effect": contract["effects"]["runtime"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ValueError as exc:
        print(f"AUTONOMOUS_GROWTH_CONTRACT_FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
