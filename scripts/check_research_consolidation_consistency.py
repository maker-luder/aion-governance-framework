from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_BRANCH = "engineering/aion-research-consolidation-literature-grounding-readiness-20260814"
SCHEMA = ROOT / "schemas/aion_research_consolidation_artifact_v0.1.0.schema.json"
EVIDENCE_RECORD = ROOT / "research-workbench/four-domain-materialization/2026-08-14/P2_PACKET_C_EVIDENCE_ADMISSION_RECORD.json"
P2_PACKET = ROOT / "research-labs/four-domain-p2-materialization_v0.1.0/docs/P2_MATERIALIZATION_PACKET_C.md"
P2_TEST = ROOT / "research-labs/four-domain-p2-materialization_v0.1.0/tests/test_p2_compact.py"
P2_FIXTURE = ROOT / "research-labs/four-domain-p2-materialization_v0.1.0/fixtures/p2_synthetic_fixture_a.json"

ARTIFACTS = {
    "index": ROOT / "docs/research-consolidation/RESEARCH_INDEX_V0.1.0.json",
    "graph": ROOT / "docs/research-consolidation/CLAIM_DEPENDENCY_GRAPH_V0.1.0.json",
    "source_map": ROOT / "docs/research-consolidation/SOURCE_OF_TRUTH_MAP_V0.1.0.json",
    "crosswalk": ROOT / "docs/research-consolidation/EXTERNAL_LITERATURE_CROSSWALK_V0.1.0.json",
    "supersession": ROOT / "docs/research-consolidation/SUPERSESSION_MAP_V0.1.0.json",
    "matrix": ROOT / "docs/research-consolidation/PROMOTION_READINESS_MATRIX_V0.1.0.json",
    "falsifier": ROOT / "docs/research-consolidation/P2_PACKET_C_FALSIFIER_MATRIX_V0.1.0.json",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_json_schema(errors: list[str], value: dict[str, Any], path: Path) -> None:
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        fail(errors, f"jsonschema unavailable: {exc}")
        return
    try:
        schema = load(SCHEMA)
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        for error in sorted(validator.iter_errors(value), key=lambda item: list(item.absolute_path)):
            fail(errors, f"{path.relative_to(ROOT)} schema: {error.message}")
    except Exception as exc:  # pragma: no cover - diagnostic guard
        fail(errors, f"{path.relative_to(ROOT)} schema check error: {exc}")


def main() -> int:
    errors: list[str] = []

    try:
        branch = git("branch", "--show-current")
        if branch != EXPECTED_BRANCH:
            fail(errors, f"unexpected branch {branch!r}; expected {EXPECTED_BRANCH!r}")
    except subprocess.CalledProcessError as exc:
        fail(errors, f"cannot read current git branch: {exc}")

    required_paths = (
        ROOT / "docs/research-consolidation/RESEARCH_INDEX_V0.1.0.md",
        ROOT / "docs/research-consolidation/CLAIM_DEPENDENCY_GRAPH_V0.1.0.md",
        ROOT / "docs/research-consolidation/SOURCE_OF_TRUTH_MAP_V0.1.0.md",
        ROOT / "docs/research-consolidation/EXTERNAL_LITERATURE_CROSSWALK_V0.1.0.md",
        ROOT / "docs/research-consolidation/SUPERSESSION_MAP_V0.1.0.md",
        ROOT / "docs/research-consolidation/PROMOTION_READINESS_MATRIX_V0.1.0.md",
        ROOT / "docs/research-consolidation/REVIEWER_FACING_VERTICAL_SLICE_P2_PACKET_C_V0.1.0.md",
        ROOT / "docs/research-consolidation/P2_PACKET_C_FALSIFIER_MATRIX_V0.1.0.md",
        ROOT / "docs/research-consolidation/CONVERGENCE_GAP_REGISTER_V0.1.0.md",
        ROOT / "docs/research-consolidation/CONVERGENCE_STATUS_V0.1.0.md",
        ROOT / "RESEARCH_BRANCH_STATUS.md",
        ROOT / "README.md",
        ROOT / "research-workbench/four-domain-materialization/2026-08-12/WHITEPAPER_WEB_BRANCH_RECONCILIATION_2026-08-12.md",
        ROOT / "research-labs/language-core-g1_v0.2.1/README.md",
        ROOT / "research-labs/language-core-g1_v0.2.1/docs/GOVERNANCE.md",
        ROOT / "research-labs/language-core-g1_v0.2.1/docs/IMPLEMENTATION_TRACEABILITY_MATRIX.csv",
        ROOT / "components/aion_runtime_v0.2.0/README.md",
        ROOT / "scripts/check_research_scope_lock.py",
        ROOT / "scripts/validate_research_evidence.py",
        ROOT / "schemas/research_evidence_record_v0.2.0.schema.json",
        ROOT / ".github/workflows/research-convergence-consistency.yml",
    )
    for path in required_paths:
        if not path.exists():
            fail(errors, f"required inventory path missing: {path.relative_to(ROOT)}")

    if not SCHEMA.is_file():
        fail(errors, f"missing schema: {SCHEMA.relative_to(ROOT)}")

    for path in (ROOT / "README.md", ROOT / "RESEARCH_BRANCH_STATUS.md"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            for phrase in ("CANONICAL_EFFECT = NONE", "SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED"):
                if phrase not in text:
                    fail(errors, f"{path.relative_to(ROOT)} missing parity phrase: {phrase}")

    data: dict[str, Any] = {}
    for name, path in ARTIFACTS.items():
        if not path.is_file():
            fail(errors, f"missing artifact {name}: {path.relative_to(ROOT)}")
            continue
        try:
            value = load(path)
        except Exception as exc:
            fail(errors, f"invalid JSON {path.relative_to(ROOT)}: {exc}")
            continue
        if not isinstance(value, dict):
            fail(errors, f"artifact {name} is not an object")
            continue
        data[name] = value
        validate_json_schema(errors, value, path)
        if value.get("canonical_effect") != "NONE":
            fail(errors, f"{name} canonical_effect is not NONE")
        if value.get("deployment") is True:
            fail(errors, f"{name} deployment is true")

    index = data.get("index", {})
    graph = data.get("graph", {})
    source_map = data.get("source_map", {})
    crosswalk = data.get("crosswalk", {})
    supersession = data.get("supersession", {})
    matrix = data.get("matrix", {})
    falsifier = data.get("falsifier", {})

    expected_statuses = {"CURRENT", "SUPERSEDED", "HISTORICAL", "HOLD", "REJECT"}
    expected_dispositions = {"PROMOTE", "KEEP_RESEARCH_ONLY", "HOLD"}
    for name, value in (("index", index), ("matrix", matrix), ("falsifier", falsifier)):
        for row in value.get("entries", []) + value.get("rows", []):
            if row.get("status") not in expected_statuses:
                fail(errors, f"{name} has invalid status {row.get('status')!r}")
            if row.get("disposition") not in expected_dispositions:
                fail(errors, f"{name} has invalid disposition {row.get('disposition')!r}")

    for relation in supersession.get("relations", []):
        if relation.get("earlier_status") not in expected_statuses or relation.get("later_status") not in expected_statuses:
            fail(errors, f"supersession relation has invalid status: {relation.get('id')}")
        if relation.get("disposition") not in expected_dispositions:
            fail(errors, f"supersession relation has invalid disposition: {relation.get('id')}")

    index_text = (ROOT / "docs/research-consolidation/RESEARCH_INDEX_V0.1.0.md").read_text(encoding="utf-8")
    if "Four-Domain is the **research-method and evidence-question layer**" not in index_text:
        fail(errors, "index does not state Four-Domain method role")
    if "G1 is a **parallel enabling substrate**" not in index_text:
        fail(errors, "index does not state G1 parallel-substrate role")
    if index.get("four_domain_g1_relation", {}).get("authorized_runtime_integration") is not False:
        fail(errors, "Four-Domain/G1 authorized runtime integration must be false")
    if index.get("selected_vertical_slice", {}).get("id") != "VERT-P2-PACKET-C":
        fail(errors, "selected vertical slice is not VERT-P2-PACKET-C")

    edge_pairs = {(edge.get("from"), edge.get("to"), edge.get("kind")) for edge in graph.get("edges", [])}
    if ("P2", "FX", "IMPLEMENTATION_TO_FIXTURE") not in edge_pairs:
        fail(errors, "graph missing P2 to fixture edge")
    if ("P2", "T2", "IMPLEMENTATION_TO_TEST") not in edge_pairs:
        fail(errors, "graph missing P2 to test edge")
    if ("P2", "RT", "EXPLICIT_NON_INTEGRATION_BOUNDARY") not in edge_pairs:
        fail(errors, "graph missing P2 runtime non-integration edge")
    if ("G1", "FD", "SUBJECTIVITY_AUTHORITY") in edge_pairs or ("RT", "FD", "SUBJECTIVITY_AUTHORITY") in edge_pairs:
        fail(errors, "graph contains forbidden subjectivity authority edge")

    source_cases = {item.get("question"): item for item in source_map.get("entries", [])}
    if "branch standing" not in source_cases:
        fail(errors, "source map missing branch standing authority")
    else:
        if source_cases["branch standing"].get("authoritative") != ["RESEARCH_BRANCH_STATUS.md"]:
            fail(errors, "source map branch standing authority drifted")
    if "README_vs_status" not in {item.get("case") for item in source_map.get("duplicate_drift_resolutions", [])}:
        fail(errors, "source map missing README/status drift resolution")

    if supersession.get("policy", {}).get("historical_records") != "PRESERVE":
        fail(errors, "supersession policy does not preserve historical records")
    if supersession.get("policy", {}).get("date_erasure") is not False:
        fail(errors, "supersession policy permits date erasure")
    forbidden = set(supersession.get("forbidden_relations", []))
    for required in {
        "G1!=SUPERSESSION_OF_FOUR_DOMAIN_METHOD",
        "AION_RUNTIME_V0_2!=SUPERSESSION_OF_WHITEPAPER_METHOD",
        "KIMI_REVIEW!=SUPERSESSION_OF_PRIMARY_SOURCES",
    }:
        if required not in forbidden:
            fail(errors, f"supersession missing forbidden relation {required}")

    labels = {item.get("label") for item in crosswalk.get("papers_and_standards", []) + crosswalk.get("external_projects", [])}
    required_labels = {"VERIFIED", "CORRECTION_REQUIRED"}
    if not required_labels.issubset(labels):
        fail(errors, f"crosswalk missing labels {sorted(required_labels - labels)}")
    for item in crosswalk.get("papers_and_standards", []) + crosswalk.get("external_projects", []):
        text = " ".join(str(item.get(key, "")) for key in ("claim", "aion_engineering", "aion_integration", "novelty" )).lower()
        novelty_patterns = (
            r"\b(?:aion|our|this)\s+(?:first|only|unprecedented)\b",
            r"\b(?:first|only|unprecedented)\s+(?:aion|contribution|result|system|architecture|method|claim)\b",
        )
        if any(re.search(pattern, text) for pattern in novelty_patterns) and item.get("label") not in {"CORRECTION_REQUIRED"}:
            fail(errors, f"crosswalk repeats forbidden novelty wording in {item.get('id')}")
    for item in crosswalk.get("external_projects", []):
        if item.get("id") in {"EXT-AISYSTESTING", "EXT-AIWARE", "EXT-MRIVAS", "EXT-ATOM"} and item.get("disposition") != "HOLD":
            fail(errors, f"unverified external project not HOLD: {item.get('id')}")

    first_batch = set(matrix.get("recommended_first_batch", []))
    if not first_batch:
        fail(errors, "promotion matrix has empty recommended first batch")
    for row in matrix.get("rows", []):
        if row.get("id") in first_batch and row.get("disposition") != "PROMOTE":
            fail(errors, f"first-batch row is not PROMOTE: {row.get('id')}")
    for row in matrix.get("rows", []):
        if row.get("id") in {"PR-009", "PR-010", "PR-011", "PR-014", "PR-015", "PR-017", "PR-020", "PR-025", "PR-026", "PR-027"} and row.get("disposition") == "PROMOTE":
            fail(errors, f"excluded runtime/claim row is PROMOTE: {row.get('id')}")

    for path in (P2_PACKET, P2_TEST, P2_FIXTURE, EVIDENCE_RECORD):
        if not path.is_file():
            fail(errors, f"missing vertical-slice path: {path.relative_to(ROOT)}")
    if P2_PACKET.is_file():
        packet = P2_PACKET.read_text(encoding="utf-8")
        for phrase in ("HISTORICAL_REPORTED_TEST_COUNT = 13", "CURRENT_TEST_FUNCTION_COUNT = 5", "CURRENT_EXPECTED_RESULT = 5 passed", "RUNTIME_EFFECT = NONE"):
            if phrase not in packet:
                fail(errors, f"P2 Packet C missing reconciliation phrase: {phrase}")
    if P2_TEST.is_file():
        test_count = len(re.findall(r"^def test_", P2_TEST.read_text(encoding="utf-8"), flags=re.MULTILINE))
        if test_count != 5:
            fail(errors, f"P2 current test function count is {test_count}, expected 5")
    if P2_FIXTURE.is_file():
        fixture = load(P2_FIXTURE)
        if fixture.get("canonical_effect") != "NONE":
            fail(errors, "P2 fixture canonical effect drifted")
        if fixture.get("expected", {}).get("selected_record_ids") != ["fact-new"]:
            fail(errors, "P2 fixture selected record expectation drifted")
        if fixture.get("expected", {}).get("identity_continuity_conclusion") != "NOT_ESTABLISHED":
            fail(errors, "P2 fixture identity boundary drifted")

    if EVIDENCE_RECORD.is_file():
        sys.path.insert(0, str(ROOT / "scripts"))
        try:
            from validate_research_evidence import validate_record

            result = validate_record(ROOT, EVIDENCE_RECORD)
            if result.status != "PASS":
                fail(errors, f"P2 evidence admission validation did not PASS: {result.diagnostics}")
            record = load(EVIDENCE_RECORD)
            if record.get("result_status") != "HOLD":
                fail(errors, "P2 evidence record must remain HOLD")
            if record.get("canonical_effect") != "NONE":
                fail(errors, "P2 evidence record canonical effect drifted")
        except Exception as exc:  # pragma: no cover - diagnostic guard
            fail(errors, f"P2 evidence admission check error: {exc}")

    forbidden_source_patterns = (
        r"^\s*import\s+(requests|urllib|socket|subprocess)\b",
        r"^\s*from\s+(requests|urllib|socket|subprocess)\b",
        r"\bsubprocess\.",
        r"\beval\(",
        r"\bexec\(",
        r"\bimport\s+mcp\b",
        r"\bfrom\s+mcp\b",
    )
    p2_src = ROOT / "research-labs/four-domain-p2-materialization_v0.1.0/src"
    if p2_src.is_dir():
        for source in p2_src.rglob("*.py"):
            text = source.read_text(encoding="utf-8")
            for pattern in forbidden_source_patterns:
                if re.search(pattern, text, flags=re.MULTILINE | re.IGNORECASE):
                    fail(errors, f"P2 source contains forbidden runtime/transport pattern {pattern}: {source.relative_to(ROOT)}")

    if errors:
        print("research consolidation consistency: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("research consolidation consistency: PASS")
    print(f"validated artifacts={len(data)}; p2_tests=5; canonical_effect=NONE; deployment=FALSE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
