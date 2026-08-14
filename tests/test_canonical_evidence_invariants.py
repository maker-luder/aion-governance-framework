from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
RECORD_PATH = ROOT / "docs/promotion/CSOMI_CANONICAL_EVIDENCE_GUARD_RECORD_V0.1.0.json"
SCHEMA_PATH = ROOT / "schemas/aion_canonical_evidence_invariants_v0.1.0.schema.json"
INVENTORY_PATH = ROOT / "docs/promotion/CSOMI_SELECTIVE_PROMOTION_INVENTORY_V0.1.0.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def errors_for(record):
    schema = load_json(SCHEMA_PATH)
    return list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record))


def test_positive_guard_record_schema_and_checker_pass():
    record = load_json(RECORD_PATH)
    assert errors_for(record) == []
    assert record["claim_type"] == "RESEARCH_TOPIC"
    assert record["claim_status"] == "DESIGN_GUARD"
    assert record["promotion_state"]["deployment"] is False
    assert record["promotion_state"]["test_ci_is_subjectivity_evidence"] is False
    assert record["promotion_state"]["subjectivity_conclusion"] == "NOT_ESTABLISHED"


def test_inventory_has_only_four_includes_and_three_owner_reviews():
    inventory = load_json(INVENTORY_PATH)
    decisions = [row["decision"] for row in inventory["inventory"]]
    assert decisions.count("INCLUDE") == 4
    assert decisions.count("OWNER_REVIEW") == 3
    assert "EXCLUDE" not in decisions
    assert inventory["promotion_state"]["canonical_effect"] == "PENDING_OWNER_PROMOTION"


def test_ci_success_is_not_subjectivity_evidence():
    record = load_json(RECORD_PATH)
    ci_channel = next(row for row in record["evidence_channels"] if row["id"] == "EVID-CI-NON-EVIDENCE")
    assert ci_channel["direction"] == "NOT_EVIDENCE"
    falsifier = next(row for row in record["falsifiers"] if row["id"] == "FALS-TEST-CI-SUBJECTIVITY")
    assert falsifier["effect"] == "MACHINE_REJECT"


def test_schema_rejects_category_collapse():
    record = load_json(RECORD_PATH)
    invalid = copy.deepcopy(record)
    invalid["claim_type"] = "SCIENTIFIC_CONCLUSION"
    invalid["claim_status"] = "CURRENT"
    assert errors_for(invalid)


def test_schema_rejects_missing_alternative():
    record = load_json(RECORD_PATH)
    invalid = copy.deepcopy(record)
    invalid["alternative_explanations"] = []
    assert errors_for(invalid)


def test_schema_rejects_missing_disanalogy():
    record = load_json(RECORD_PATH)
    invalid = copy.deepcopy(record)
    invalid["disanalogies"] = []
    assert errors_for(invalid)


def test_schema_rejects_ci_channel_as_support():
    record = load_json(RECORD_PATH)
    invalid = copy.deepcopy(record)
    ci_channel = next(row for row in invalid["evidence_channels"] if row["id"] == "EVID-CI-NON-EVIDENCE")
    ci_channel["direction"] = "SUPPORTS_METHOD"
    assert errors_for(invalid)
