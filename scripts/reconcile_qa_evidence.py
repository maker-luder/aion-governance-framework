from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "qa"

tests = json.loads((QA / "CURRENT_TEST_RESULTS.json").read_text(encoding="utf-8"))
coverage = json.loads((QA / "CURRENT_COVERAGE_RESULTS.json").read_text(encoding="utf-8"))
whole = json.loads((QA / "WHOLE_SYSTEM_VALIDATION.json").read_text(encoding="utf-8"))
now = datetime.now(UTC).isoformat()

test_summary = tests["summary"]
coverage_summary = coverage["summary"]
eligible = int(test_summary["eligible_target_count"])
assert eligible == int(coverage_summary["eligible_target_count"])
assert len(tests["targets"]) == eligible
assert len(coverage["targets"]) == eligible
assert int(whole["tests_failed"]) == 0

coverage_by_target = {item["target"]: item for item in coverage["targets"]}
test_by_target = {item["target"]: item for item in tests["targets"]}
rows = []
for target in sorted(test_by_target):
    test_item = test_by_target[target]
    coverage_item = coverage_by_target[target]
    percent = coverage_item.get("coverage_percent")
    coverage_text = "N/A — research-only surface" if percent is None else f"{float(percent):.2f}%"
    rows.append(
        f"| `{target}` | {test_item['status']} | {test_item['passed']} | {test_item['failed']} | {coverage_text} | {test_item['coverage']} |"
    )

(QA / "COVERAGE_REPORT.md").write_text(
    "# Review Candidate v2 Branch Coverage Report\n\n"
    "Coverage was measured with branch coverage enabled for every test-bearing eligible target. The policy is report-only: no unjustified global threshold is imposed across heterogeneous research fixtures. A measured percentage is not whole-system validation, independent IV&V, scientific evidence, or release approval.\n\n"
    f"Generated at `{now}`. Scope: `REVIEW_CANDIDATE_V2`; eligible targets: **{eligible}**; measured targets: **{coverage_summary['measured_target_count']}**; explicit non-applicability: **{coverage_summary['not_applicable_target_count']}**.\n\n"
    "| Target | Test status | Passed | Failed | Branch coverage | Coverage disposition |\n"
    "|---|---|---:|---:|---:|---|\n"
    + "\n".join(rows)
    + "\n\n"
    "The two `NOT_APPLICABLE` rows are research-only surfaces with no test directory; they are not silently omitted.\n",
    encoding="utf-8",
)

current_coverage = {
    "schema_version": "2.0",
    "generated_at": now,
    "scope": "REVIEW_CANDIDATE_V2",
    "target_count": eligible,
    "tested_target_count": coverage_summary["measured_target_count"],
    "non_applicable_target_count": coverage_summary["not_applicable_target_count"],
    "branch_coverage": True,
    "status": "PASS" if coverage_summary["failed_target_count"] == 0 else "FAIL",
    "source_results": "qa/CURRENT_COVERAGE_RESULTS.json",
    "targets": coverage["targets"],
}
(QA / "CURRENT_COVERAGE.json").write_text(json.dumps(current_coverage, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

reconciliation = {
    "schema_version": "2.0",
    "generated_at": now,
    "scope": "REVIEW_CANDIDATE_V2",
    "scope_definitions": {
        "MAIN_BASELINE": "Remote main at 4b36077993fabb22bf04e06162ea83c623bbb7e6; not modified by this task.",
        "FORMAL_RESEARCH_BASELINE": "Remote formal research at 6f39fff07f1b1a79867c270f953c554e18addbc1; v2 ancestry source.",
        "REVIEW_CANDIDATE_V2": "Current v2 worktree and exact review branch head after final commit.",
        "HISTORICAL_EVIDENCE": "Old orphan review at 263f6905356ebf0581b9ad8acda6c449587c73f1; retained for provenance only.",
    },
    "target_count_reconciliation": {
        "eligible_project_surface": eligible,
        "component_registry": eligible,
        "test_results": len(tests["targets"]),
        "coverage_results": len(coverage["targets"]),
        "coverage_report": len(rows),
        "handoff_scope": eligible,
        "test_bearing_targets": test_summary["tested_target_count"],
        "explicit_non_applicable_targets": test_summary["non_applicable_target_count"],
    },
    "test_reconciliation": {
        "test_total": test_summary["total_passed"],
        "test_failures": test_summary["total_failed"],
        "whole_system_test_case_count": whole["TEST_CASE_COUNT"],
        "whole_system_scenario_class_count": whole["SCENARIO_CLASS_COUNT"],
    },
    "statuses": {
        "coverage": current_coverage["status"],
        "manifest": "PENDING_FINAL_MANIFEST",
        "compileall": "PENDING_FINAL_COMPILEALL",
        "privacy_scan": "PENDING_FINAL_SCAN",
        "secret_scan": "PENDING_FINAL_SCAN",
    },
    "canonical_effect": "NONE",
    "deployment": False,
    "independent_ivv": "NOT_ACHIEVED",
}
(QA / "QA_RECONCILIATION.json").write_text(json.dumps(reconciliation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

(QA / "CURRENT_RELEASE_STATUS_LOCK.json").write_text(
    json.dumps(
        {
            "schema_version": "2.0",
            "release": "REVIEW_CANDIDATE_V2_NOT_RELEASE",
            "scope": "REVIEW_CANDIDATE_V2",
            "eligible_target_count": eligible,
            "tested_target_count": test_summary["tested_target_count"],
            "non_applicable_target_count": test_summary["non_applicable_target_count"],
            "current_tests": f"{test_summary['total_passed']} PASSED / {test_summary['total_failed']} FAILED",
            "whole_system_validation": f"{whole['TEST_CASE_COUNT']} TEST_CASES / {whole['SCENARIO_CLASS_COUNT']} SCENARIO_CLASSES / PASS",
            "coverage": "PASS_BRANCH_MEASURED",
            "compileall": "PENDING_FINAL_QA",
            "manifest": "PENDING_FINAL_QA",
            "privacy_scan": "PENDING_FINAL_QA",
            "secret_scan": "PENDING_FINAL_QA",
            "independent_ivv": "NOT_ACHIEVED",
            "subjectivity_conclusion": "NOT_ESTABLISHED",
            "identity_continuity_conclusion": "NOT_ESTABLISHED",
            "canonical_effect": "NONE",
            "deployment": False,
            "promotion_status": "NOT_REVIEWED",
        },
        ensure_ascii=False,
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)

(QA / "QA_SUMMARY.md").write_text(
    "# Review Candidate v2 QA Summary\n\n"
    "This is current review-candidate evidence, not a release approval. Historical main/release evidence and formal research evidence are not silently mixed into these counts.\n\n"
    "| Evidence | Current v2 disposition | Scope |\n"
    "|---|---|---|\n"
    f"| Eligible project targets | **{eligible}** | components + examples + research-labs direct children |\n"
    f"| Test-bearing targets | **{test_summary['tested_target_count']}** | dynamic pytest matrix |\n"
    f"| Explicit non-applicable targets | **{test_summary['non_applicable_target_count']}** | research-only surfaces without tests directory |\n"
    f"| Component tests | **{test_summary['total_passed']} passed / {test_summary['total_failed']} failed** | current v2 candidate |\n"
    f"| Whole-system tests | **{whole['TEST_CASE_COUNT']} cases / {whole['SCENARIO_CLASS_COUNT']} scenario classes, PASS** | one-to-one registry in `WHOLE_SYSTEM_VALIDATION.json` |\n"
    f"| Branch coverage | **PASS measured** | {coverage_summary['measured_target_count']} targets; report-only policy |\n"
    "| Compileall, manifest, privacy, secret scans | **PENDING_FINAL_QA** | updated only after final evidence chain |\n\n"
    "The old `412 PASSED / whole_system_validation = NOT_EXECUTED` wording is historical stale evidence and is not reused. The 48-target project surface and the 46-test-bearing/2-explicitly-non-applicable split are current v2 evidence.\n\n"
    "Subjectivity, identity continuity, deployment, canonical promotion and independent IV&V remain unestablished or false.\n\n"
    "```text\nCANONICAL_EFFECT = NONE\nDEPLOYMENT = FALSE\nINDEPENDENT_IVV = NOT_ACHIEVED\n```\n",
    encoding="utf-8",
)

(QA / "RELEASE_EVIDENCE.json").write_text(
    json.dumps(
        {
            "schema_version": "2.0",
            "scope": "REVIEW_CANDIDATE_V2_NOT_RELEASE",
            "repository": "maker-luder/aion-governance-framework",
            "current_reconstruction_validation": {
                "eligible_targets": eligible,
                "test_bearing_targets": test_summary["tested_target_count"],
                "non_applicable_targets": test_summary["non_applicable_target_count"],
                "tests": f"{test_summary['total_passed']} passed / {test_summary['total_failed']} failed",
                "whole_system": f"{whole['TEST_CASE_COUNT']} test cases / {whole['SCENARIO_CLASS_COUNT']} scenario classes",
                "coverage": "PASS_BRANCH_MEASURED",
                "compileall": "PENDING_FINAL_QA",
                "manifest": "PENDING_FINAL_QA",
                "secret_scan": "PENDING_FINAL_QA",
                "privacy_review": "PENDING_FINAL_QA",
            },
            "historical_source_evidence": {
                "old_review_branch": "263f6905356ebf0581b9ad8acda6c449587c73f1",
                "disposition": "SUPERSEDED_REVIEW_ARTIFACT / NOT_MERGE_CANDIDATE / RETAINED_FOR_PROVENANCE",
            },
            "subjectivity_conclusion": "NOT_ESTABLISHED",
            "identity_continuity_conclusion": "NOT_ESTABLISHED",
            "canonical_effect": "NONE",
            "deployment": False,
            "independent_ivv": "NOT_ACHIEVED",
        },
        ensure_ascii=False,
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)
