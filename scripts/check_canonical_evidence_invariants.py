#!/usr/bin/env python3
"""Fail-closed validation for the selective-promotion canonical evidence guard."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/promotion/CSOMI_CANONICAL_EVIDENCE_GUARD_RECORD_V0.1.0.json"
SCHEMA = ROOT / "schemas/aion_canonical_evidence_invariants_v0.1.0.schema.json"
INVENTORY = ROOT / "docs/promotion/CSOMI_SELECTIVE_PROMOTION_INVENTORY_V0.1.0.json"


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))

    schema_errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record))
    for error in schema_errors:
        fail(errors, f"schema: {list(error.path)}: {error.message}")

    if record.get("claim_type") != "RESEARCH_TOPIC":
        fail(errors, "record must remain a RESEARCH_TOPIC design guard")
    if record.get("claim_status") != "DESIGN_GUARD":
        fail(errors, "record must remain DESIGN_GUARD")
    if record.get("promotion_state") != {
        "canonical_effect": "PENDING_OWNER_PROMOTION",
        "deployment": False,
        "test_ci_is_subjectivity_evidence": False,
        "subjectivity_conclusion": "NOT_ESTABLISHED",
    }:
        fail(errors, "promotion/no-deployment/subjectivity boundary drifted")

    locks = set(record.get("semantic_locks", []))
    required_locks = {
        "RESEARCH_TOPIC != CAPABILITY != SCIENTIFIC_CONCLUSION",
        "TEST_OR_CI_PASS != SUBJECTIVITY_EVIDENCE",
        "SOURCE_PROVENANCE_LEVEL != SCIENTIFIC_TRUTH",
        "CANONICAL_CANDIDATE != CANONICAL_PROMOTION",
    }
    if not required_locks <= locks:
        fail(errors, f"semantic locks missing: {sorted(required_locks - locks)}")

    channels = {row.get("id"): row for row in record.get("evidence_channels", [])}
    ci_channel = channels.get("EVID-CI-NON-EVIDENCE", {})
    if ci_channel.get("direction") != "NOT_EVIDENCE" or ci_channel.get("kind") != "REPOSITORY_VALIDATION":
        fail(errors, "test/CI channel must be machine-marked NOT_EVIDENCE")

    falsifiers = {row.get("id"): row for row in record.get("falsifiers", [])}
    ci_falsifier = falsifiers.get("FALS-TEST-CI-SUBJECTIVITY", {})
    if ci_falsifier.get("effect") != "MACHINE_REJECT" or ci_falsifier.get("status") != "MACHINE_ENFORCED":
        fail(errors, "test/CI subjectivity falsifier must be MACHINE_REJECT")

    if not record.get("alternative_explanations"):
        fail(errors, "alternative explanations are required")
    if not record.get("disanalogies"):
        fail(errors, "disanalogies are required")
    if not falsifiers:
        fail(errors, "falsifiers are required")

    provenance = record.get("provenance", {})
    for role in ("HUMAN_OWNER", "CHATGPT", "MANUS", "OWNER_APPROVAL"):
        if role not in provenance:
            fail(errors, f"provenance role missing: {role}")
    if provenance.get("source_commit_locks") != {
        "main": "e079fb7dfe7a04be7dcb94b8a059951a003caa94",
        "research": "87405c1877c6f016c303971da13923a1ab690aae",
    }:
        fail(errors, "source commit locks drifted")

    decisions = {row.get("id"): row.get("decision") for row in inventory.get("inventory", [])}
    expected_decisions = {
        "PROM-001": "INCLUDE",
        "PROM-002": "INCLUDE",
        "PROM-003": "INCLUDE",
        "PROM-004": "INCLUDE",
        "PROM-005": "OWNER_REVIEW",
        "PROM-006": "OWNER_REVIEW",
        "PROM-007": "OWNER_REVIEW",
        "PROM-008": "EXCLUDE",
        "PROM-009": "EXCLUDE",
        "PROM-010": "EXCLUDE",
        "PROM-011": "EXCLUDE",
        "PROM-012": "EXCLUDE",
        "PROM-013": "EXCLUDE",
    }
    if decisions != expected_decisions:
        fail(errors, f"promotion decisions drifted: {decisions}")
    expected_locks = {"main": "e079fb7dfe7a04be7dcb94b8a059951a003caa94", "research": "87405c1877c6f016c303971da13923a1ab690aae"}
    required_roles = {"HUMAN_OWNER", "CHATGPT", "MANUS", "OWNER_APPROVAL"}
    for item in inventory.get("inventory", []):
        if item.get("source_commit_locks") != expected_locks:
            fail(errors, f"source commit locks drifted for {item.get('id')}")
        if set(item.get("provenance_refs", [])) != required_roles:
            fail(errors, f"provenance roles drifted for {item.get('id')}")
    if inventory.get("candidate_base", {}).get("sha") != "e079fb7dfe7a04be7dcb94b8a059951a003caa94":
        fail(errors, "candidate base is not authoritative main SHA")
    if inventory.get("research_source", {}).get("sha") != "87405c1877c6f016c303971da13923a1ab690aae":
        fail(errors, "research source lock drifted")
    if inventory.get("promotion_state", {}).get("deployment") is not False:
        fail(errors, "inventory deployment must remain false")
    if inventory.get("promotion_state", {}).get("main_merge") != "PROHIBITED":
        fail(errors, "inventory main merge must remain prohibited")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("canonical evidence invariants: PASS")
    print("included=4; owner_review=3; deployment=FALSE; canonical_effect=PENDING_OWNER_PROMOTION; subjectivity=NOT_ESTABLISHED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
