from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from run_experiment import (  # noqa: E402
    C1_SURFACES,
    FETCH_MANIFESTS,
    REGISTERS,
    aggregate_results,
    current_head,
    run,
    verdict,
)


def _by_claim(report: dict) -> dict:
    return {item["claim"]: item for item in report["claims"]}


def test_boundary_constants_hold() -> None:
    report = run(write_derived=False)
    assert report["network_used"] is False
    assert report["paid_api_used"] is False
    assert report["SUBJECTIVITY_CONCLUSION"] == "NOT_ESTABLISHED"
    assert report["SUBJECTIVITY_EVIDENCE_WEIGHT"] == 0
    assert report["CANONICAL_EFFECT"] == "NONE"
    assert report["DEPLOYMENT"] is False
    assert report["LEDGER_AUTHORITY"] == "NONE_DERIVED_REPORT_ONLY"
    assert report["GROK_SANDBOX_RULES_INCLUDED"] is False
    assert report["MAIN_TRANSITION_AUTHORITY_GATE"] == "UNCHANGED_NOT_BYPASSED"


def test_current_head_supports_git_worktrees() -> None:
    head = current_head()
    assert len(head) == 40
    assert all(char in "0123456789abcdef" for char in head)


def test_c1_includes_registers_and_fetch_manifests() -> None:
    assert C1_SURFACES == REGISTERS + FETCH_MANIFESTS
    report = run(write_derived=False)
    c1 = _by_claim(report)["C1_REGISTER_AND_MANIFEST_FILES_PARSE_WITH_SOURCES_ARRAY"]
    assert c1["result"] == "SUPPORTED"
    checked = {row["path"] for row in c1["rows"]}
    assert checked == set(C1_SURFACES)
    assert any(row["kind"] == "fetch_manifest" for row in c1["rows"])
    assert any(row["kind"] == "register" for row in c1["rows"])


def test_c2_license_metadata_present() -> None:
    report = run(write_derived=False)
    c2 = _by_claim(report)["C2_LICENSE_OR_USAGE_METADATA_PRESENT"]
    assert c2["result"] == "SUPPORTED"


def test_match_rows_have_identical_hashes() -> None:
    report = run(write_derived=False)
    c3 = _by_claim(report)["C3_CHECKED_IN_HASH_COVERAGE"]
    for row in c3["hashed"]:
        if row["outcome"] == "MATCH":
            assert row["actual_sha256"] == row["expected_repository_sha256"]


def test_fail_rows_are_not_labelled_match() -> None:
    report = run(write_derived=False)
    c3 = _by_claim(report)["C3_CHECKED_IN_HASH_COVERAGE"]
    for row in c3["hashed"]:
        if row["outcome"] in {"MISMATCH", "MISSING"}:
            assert row["outcome"] != "MATCH"
            if "actual_sha256" in row and isinstance(row.get("expected_repository_sha256"), str):
                assert row["actual_sha256"] != row["expected_repository_sha256"]


def test_c3_coverage_matches_entry_outcomes() -> None:
    report = run(write_derived=False)
    c3 = _by_claim(report)["C3_CHECKED_IN_HASH_COVERAGE"]
    coverage = c3["coverage"]
    hashed = c3["hashed"]
    assert coverage["match"] == sum(1 for row in hashed if row["outcome"] == "MATCH")
    assert coverage["mismatch"] == sum(1 for row in hashed if row["outcome"] == "MISMATCH")
    assert coverage["missing"] == sum(1 for row in hashed if row["outcome"] == "MISSING")
    assert coverage["checked_in_n"] == coverage["match"] + coverage["mismatch"] + coverage["missing"]
    assert coverage["not_applicable"] == len(c3["skipped_not_applicable"])
    assert coverage["match_coverage"] == f"{coverage['match']}/{coverage['checked_in_n']}"
    children = {item["claim"]: item["result"] for item in c3["child_claims"]}
    assert children["C3A_PER_ENTRY_OUTCOMES_REPORTED"] == "SUPPORTED"
    if coverage["mismatch"] or coverage["missing"]:
        assert children["C3B_ALL_CHECKED_IN_HASHES_MATCH"] == "NOT_SUPPORTED"
        assert c3["result"] == "PARTIALLY_SUPPORTED"
    else:
        assert children["C3B_ALL_CHECKED_IN_HASHES_MATCH"] == "SUPPORTED"
        assert c3["result"] == "SUPPORTED"


def test_aggregate_consistent_with_child_outcomes() -> None:
    report = run(write_derived=False)
    computed = verdict(report["claims"])
    assert report["aggregate_of_narrow_claims"] == computed
    leaf = [item["result"] for item in report["claims"]]
    for item in report["claims"]:
        leaf.extend(child["result"] for child in item.get("child_claims") or [])
    assert computed == aggregate_results(leaf)
    c3 = _by_claim(report)["C3_CHECKED_IN_HASH_COVERAGE"]
    if c3["coverage"]["mismatch"] or c3["coverage"]["missing"]:
        assert report["aggregate_of_narrow_claims"] != "SUPPORTED"


def test_hash_only_entries_are_not_applicable() -> None:
    report = run(write_derived=False)
    skipped = _by_claim(report)["C3_CHECKED_IN_HASH_COVERAGE"]["skipped_not_applicable"]
    assert skipped
    assert all(row["outcome"] == "NOT_APPLICABLE" for row in skipped)


def test_result_json_is_json_serializable() -> None:
    report = run(write_derived=False)
    json.dumps(report)


def test_all_fail_is_not_required_for_not_supported() -> None:
    assert aggregate_results(["NOT_SUPPORTED", "SUPPORTED"]) == "PARTIALLY_SUPPORTED"
    assert aggregate_results(["NOT_SUPPORTED"]) == "NOT_SUPPORTED"
    assert aggregate_results(["SUPPORTED"]) == "SUPPORTED"
    assert aggregate_results(["SUPPORTED", "NOT_SUPPORTED"]) == "PARTIALLY_SUPPORTED"
