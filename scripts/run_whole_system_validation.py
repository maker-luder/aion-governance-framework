from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "components" / "whole_system_governed_runtime_v0.1.0"
SOURCE_ROOTS = list(
    dict.fromkeys(
        [TARGET / "src"]
        + sorted(ROOT.glob("components/*/src"))
        + sorted(ROOT.glob("examples/*/src"))
        + sorted(ROOT.glob("research-labs/*/src"))
    )
)

REQUIREMENT_METADATA = {
    "test_semantic_recall_payload_reaches_language_core": ("WS-MEM-001", "semantic_memory_recall"),
    "test_cross_session_semantic_recall_preserves_content_authority_and_provenance": ("WS-MEM-002", "semantic_memory_recall"),
    "test_cross_namespace_secret_never_reaches_adapter_input": ("WS-MEM-003", "namespace_isolation"),
    "test_superseded_and_conflicting_memory_are_excluded": ("WS-MEM-004", "memory_state_policy"),
    "test_claimed_provenance_without_registry_is_denied": ("WS-PROV-001", "provenance_verification"),
    "test_approval_forgery_and_scope_negative_cases": ("WS-AUTH-001", "authorization_trust_boundary"),
    "test_trusted_owner_approval_permits_exact_surface_only": ("WS-AUTH-002", "authorization_trust_boundary"),
    "test_hung_provider_returns_within_hard_bounded_tolerance": ("WS-TIME-001", "hard_timeout"),
    "test_midflight_cancellation_terminates_generation_and_prevents_writeback": ("WS-CANCEL-001", "midflight_cancellation"),
    "test_hung_tool_is_hard_bounded_by_global_deadline": ("WS-TIME-002", "hard_timeout"),
    "test_audit_failure_after_writeback_is_not_completed_and_is_recoverable": ("WS-DUR-001", "writeback_audit_consistency"),
    "test_checkpoint_failure_without_writeback_fails_closed": ("WS-DUR-002", "writeback_audit_consistency"),
    "test_restart_reconciliation_resolves_pending_writeback_deterministically": ("WS-DUR-003", "restart_reconciliation"),
    "test_identity_namespace_binding_and_initial_cancellation": ("WS-ID-001", "identity_namespace_binding"),
    "test_transient_generation_retries_and_fallback_is_audited": ("WS-RES-001", "retry_fallback"),
}


def _sanitize_output(text: str) -> str:
    sanitized = text.replace(str(ROOT), "<CANDIDATE_ROOT>")
    return re.sub(r"/home/[^/\\s]+/[^/\\s]+/aion-governance-framework", "<RUNNER_ROOT>", sanitized)


def _environment() -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(str(path) for path in SOURCE_ROOTS)
    return env


def _collect_nodes(env: dict[str, str]) -> list[str]:
    process = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", "-o", "addopts=", str(TARGET / "tests")],
        cwd=TARGET,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if process.returncode != 0:
        raise RuntimeError(f"pytest collection failed:\n{_sanitize_output(process.stdout)}")
    return [line.strip() for line in process.stdout.splitlines() if line.startswith("tests/") and "::" in line]


def _base_test_name(node_id: str) -> str:
    name = node_id.split("::", 1)[1]
    return name.split("[", 1)[0]


def _run_node(node_id: str, env: dict[str, str]) -> tuple[str, str]:
    process = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-o", "addopts=", node_id],
        cwd=TARGET,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return ("PASS" if process.returncode == 0 else "FAIL", _sanitize_output(process.stdout))


def main() -> int:
    env = _environment()
    nodes = _collect_nodes(env)
    if not nodes:
        raise RuntimeError("no whole-system pytest nodes were collected")
    records: list[dict[str, object]] = []
    for node_id in nodes:
        base_name = _base_test_name(node_id)
        requirement_id, scenario_class = REQUIREMENT_METADATA.get(
            base_name,
            ("WS-UNMAPPED", "unmapped"),
        )
        actual, output = _run_node(node_id, env)
        records.append(
            {
                "scenario_id": f"{scenario_class}:{node_id.rsplit('::', 1)[-1]}",
                "scenario_class": scenario_class,
                "pytest_node_id": node_id,
                "requirement_ids": [requirement_id],
                "expected_disposition": "PASS",
                "actual_disposition": actual,
                "pass": actual == "PASS",
                "evidence_reference": node_id,
                "canonical_effect": "NONE",
                "pytest_output": output if actual != "PASS" else "",
            }
        )
    passed = sum(1 for record in records if record["pass"])
    failed = len(records) - passed
    payload = {
        "schema_version": "2.0",
        "generated_at": datetime.now(UTC).isoformat(),
        "source_code_scope": "REVIEW_CANDIDATE_V2",
        "review_branch": "review/aion-astra-whole-system-completion-v2",
        "TEST_CASE_COUNT": len(records),
        "SCENARIO_CLASS_COUNT": len({str(record["scenario_class"]) for record in records}),
        "tests_passed": passed,
        "tests_failed": failed,
        "test_returncode": 0 if failed == 0 else 1,
        "scenarios": records,
        "implemented_boundaries": {
            "semantic_memory_context": "IMPLEMENTED_VERIFIED_BY_SENTINEL",
            "authorization_trust_boundary": "IMPLEMENTED_VERIFIED",
            "provenance_verification": "IMPLEMENTED_VERIFIED",
            "hard_timeout": "IMPLEMENTED_PROCESS_TERMINATION",
            "midflight_cancellation": "IMPLEMENTED_PROCESS_TERMINATION",
            "writeback_audit_consistency": "IMPLEMENTED_FAIL_CLOSED_WITH_INTENT",
            "restart_reconciliation": "IMPLEMENTED_DETERMINISTIC",
            "network_mcp": "NOT_IMPLEMENTED",
            "canonical_effect": "NONE",
            "deployment": False,
            "independent_ivv": "NOT_ACHIEVED",
        },
        "remaining_blockers": [
            "Network MCP transport is intentionally not enabled in this candidate.",
            "No foundation-model checkpoint or GPU training evidence exists.",
            "Independent IV&V requires a reviewer separate from the implementer.",
        ],
        "evidence_sha_semantics": {
            "SOURCE_CODE_COMMIT_SHA": "filled by final handoff from git HEAD",
            "VALIDATED_TREE_SHA": "filled by final handoff from git write-tree",
            "EVIDENCE_SUBJECT_SHA": "the tree tested by this local runner",
            "EVIDENCE_COMMIT_SHA": "filled after evidence files are committed",
            "REVIEW_BRANCH_HEAD_SHA": "filled by final handoff after push",
            "CI_HEAD_SHA": "filled from GitHub Actions exact head",
        },
    }
    output = ROOT / "qa" / "WHOLE_SYSTEM_VALIDATION.json"
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: payload[key] for key in ("TEST_CASE_COUNT", "SCENARIO_CLASS_COUNT", "tests_passed", "tests_failed", "test_returncode")}, ensure_ascii=False))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
