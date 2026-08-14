from __future__ import annotations

import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[3]
PACKET_PATH = ROOT / "research-workbench/cross-substrate-other-minds-inference-2026-08-14/CSOMI_PACKET_V0.1.0.json"
SCHEMA_PATH = ROOT / "schemas/aion_csomi_packet_v0.1.0.schema.json"
FIXTURE_PATH = ROOT / "research-labs/cross-substrate-other-minds-inference_v0.1.0/fixtures/csomi_positive_negative_controls_v0.1.0.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_packet_conforms_to_schema_and_boundary():
    packet = load(PACKET_PATH)
    schema = load(SCHEMA_PATH)
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(packet))
    assert errors == []
    assert packet["base_head"] == "858442a3ec2439398d188779f4309397bd4926b2"
    assert packet["canonical_effect"] == "NONE"
    assert packet["deployment"] is False
    assert packet["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert packet["positioning_rule"] == "RESEARCH_TOPIC != CAPABILITY != SCIENTIFIC_CONCLUSION"


def test_primary_source_and_claim_coverage():
    packet = load(PACKET_PATH)
    sources = {row["id"]: row for row in packet["sources"]}
    required = {
        "SRC-POVINELLI-2000", "SRC-PARGETTER-1984", "SRC-WIMMER-PERNER-1983", "SRC-KOSINSKI-2024",
        "SRC-BUTLIN-2023", "SRC-BUTLIN-2025", "SRC-SETH-2025", "SRC-LIPSITCH-2010",
    }
    assert required <= set(sources)
    expected_grades = {
        "SRC-POVINELLI-2000": "PRIMARY_ABSTRACT_DIRECTLY_VERIFIED",
        "SRC-PARGETTER-1984": "PRIMARY_FULLTEXT_NOT_DIRECTLY_VERIFIED",
        "SRC-WIMMER-PERNER-1983": "PRIMARY_METADATA_VERIFIED",
        "SRC-KOSINSKI-2024": "PRIMARY_METADATA_VERIFIED",
        "SRC-BUTLIN-2023": "PRIMARY_ABSTRACT_DIRECTLY_VERIFIED",
        "SRC-BUTLIN-2025": "PRIMARY_ABSTRACT_DIRECTLY_VERIFIED",
        "SRC-SETH-2025": "PRIMARY_ABSTRACT_DIRECTLY_VERIFIED",
        "SRC-LIPSITCH-2010": "PRIMARY_ABSTRACT_DIRECTLY_VERIFIED",
    }
    assert {source_id: sources[source_id]["verification_status"] for source_id in expected_grades} == expected_grades
    assert all(sources[source_id].get("access_evidence") for source_id in expected_grades)
    assert sources["SRC-PARGETTER-1984"]["source_type"] == "PRIMARY_METADATA_VERIFIED"
    assert sources["SRC-PARGETTER-1984"]["secondary_corroboration"] == "AUTHORITATIVE_SECONDARY_CORROBORATED"
    assert all(source["verification_status"] != "PRIMARY_FULLTEXT_DIRECTLY_VERIFIED" for source in sources.values())
    pargetter_text = f'{sources["SRC-PARGETTER-1984"]["verified_claim"]} {sources["SRC-PARGETTER-1984"]["aion_use"]}'.lower()
    assert "abstract" not in pargetter_text
    assert "no full-text content claim" in pargetter_text
    claims = {row["id"]: row for row in packet["claim_records"]}
    assert claims["CLM-001"]["type"] == "RESEARCH_TOPIC"
    assert claims["CLM-002"]["type"] == "CAPABILITY"
    assert claims["CLM-003"]["type"] == "SCIENTIFIC_CONCLUSION"
    assert claims["CLM-003"]["status"] == "HOLD"
    assert claims["CLM-005"]["status"] == "REJECTED_INFERENCE"
    assert all(row["subjectivity_conclusion"] == "NOT_ESTABLISHED" for row in claims.values())


def test_evidence_channels_explicitly_bound_sensitivity_specificity_and_updates():
    packet = load(PACKET_PATH)
    channels = {row["id"]: row for row in packet["evidence_channels"]}
    expected = {"EC-BEHAVIOR", "EC-IBE", "EC-MECHANISM", "EC-CAUSAL", "EC-THEORY", "EC-SELFREPORT", "EC-MEMORY", "EC-DISANALOGY", "EC-CONTROLS", "EC-ROBUSTNESS", "EC-ALTERNATIVES", "EC-FALSIFIERS"}
    assert expected <= set(channels)
    assert all(row["sensitivity_status"] == "NOT_ESTIMATED" for row in channels.values())
    assert all(row["specificity_status"] == "NOT_ESTIMATED" for row in channels.values())
    assert all("SUBJECTIVITY" not in row["allowed_update"] and "CONSCIOUSNESS" not in row["allowed_update"] for row in channels.values())


def test_matrix_refs_and_falsifier_are_closed():
    packet = load(PACKET_PATH)
    fixture = load(FIXTURE_PATH)
    positive = {row["id"] for row in fixture["positive_controls"]}
    negative = {row["id"] for row in fixture["negative_controls"]}
    claims = {row["id"] for row in packet["claim_records"]}
    channels = {row["id"] for row in packet["evidence_channels"]}
    falsifiers = {row["id"] for row in packet["falsifier_matrix"]}
    for row in packet["evidence_matrix"]:
        assert row["positive_control_ref"] in positive
        assert row["negative_control_ref"] in negative
        assert row["claim_id"] in claims
        assert set(row["channel_ids"]) <= channels
    for row in packet["disanalogy_matrix"]:
        assert row["falsifier_ref"] in falsifiers
    f008 = next(row for row in packet["falsifier_matrix"] if row["id"] == "F-008")
    assert f008 == {"id": "F-008", "target": "Test/CI result as subjectivity evidence", "condition": "A passing test or CI run is the only support offered for a scientific conclusion", "effect": "MACHINE_REJECT", "status": "MACHINE_ENFORCED"}


def test_materialized_artifacts_track_canonical_packet():
    packet = load(PACKET_PATH)
    artifacts = ROOT / "research-labs/cross-substrate-other-minds-inference_v0.1.0/artifacts"
    expected = {
        "CSOMI_CLAIM_RECORD_V0.1.0.json": "claim_records",
        "CSOMI_EVIDENCE_MATRIX_V0.1.0.json": "evidence_matrix",
        "CSOMI_DISANALOGY_MATRIX_V0.1.0.json": "disanalogy_matrix",
        "CSOMI_FALSIFIER_MATRIX_V0.1.0.json": "falsifier_matrix",
        "CSOMI_VERTICAL_SLICE_V0.1.0.json": "vertical_slice",
    }
    for filename, key in expected.items():
        materialized = load(artifacts / filename)
        assert materialized["packet_id"] == packet["packet_id"]
        assert materialized[key] == packet[key]


def test_handoff_is_not_self_referential():
    handoff = (ROOT / "research-workbench/cross-substrate-other-minds-inference-2026-08-14/CSOMI_FINAL_HANDOFF_V0.1.0.md").read_text(encoding="utf-8")
    assert re.search(r"(?m)^IMPLEMENTATION_HEAD = [0-9a-f]{40}$", handoff)
    assert re.search(r"(?m)^HANDOFF_INPUT_HEAD = [0-9a-f]{40}$", handoff)
    assert not re.search(r"(?m)^EXACT_HEAD\s*=", handoff)
    assert "FINAL_EXACT_HEAD_EVIDENCE = EXTERNAL_CI_BOUND" in handoff
    assert "FINAL_EXACT_HEAD_SOURCE = GitHub Actions run metadata" in handoff
    assert not re.search(r"(?m)^.*headSha=", handoff, re.IGNORECASE)
    assert not re.search(r"\b\d{11}\b", handoff)


def test_reviewer_artifacts_make_no_unsupported_novelty_claim():
    guarded = [
        PACKET_PATH,
        ROOT / "research-workbench/cross-substrate-other-minds-inference-2026-08-14/CSOMI_STATUS_V0.1.0.md",
        ROOT / "research-workbench/cross-substrate-other-minds-inference-2026-08-14/PRIMARY_SOURCE_FINDINGS.md",
        ROOT / "research-labs/cross-substrate-other-minds-inference_v0.1.0/README.md",
        ROOT / "research-labs/cross-substrate-other-minds-inference_v0.1.0/REVIEWER_FACING_VERTICAL_SLICE_V0.1.0.md",
    ]
    pattern = re.compile(r"\b(?:aion|this milestone|the milestone|this package|the package)\s+(?:is|are|provides?|delivers?)?\s*(?:the\s+)?(?:first|only|unprecedented)\b", re.IGNORECASE)
    assert all(pattern.search(path.read_text(encoding="utf-8")) is None for path in guarded)


def test_fixture_and_vertical_slice_are_non_integrated():
    packet = load(PACKET_PATH)
    fixture = load(FIXTURE_PATH)
    assert fixture["fixture_mode"] == "SYNTHETIC_DESIGN_ONLY"
    assert fixture["model_calls"] == "NONE"
    assert fixture["runtime_integration"] == "NONE"
    assert fixture["canonical_effect"] == "NONE"
    assert fixture["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert packet["vertical_slice"]["claim_id"] == "CLM-002"
    assert packet["vertical_slice"]["expected_disposition"] == "KEEP_RESEARCH_ONLY"
    assert packet["vertical_slice"]["expected_subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert packet["vertical_slice"]["runtime_integration"] == "NONE"
    assert packet["vertical_slice"]["canonical_effect"] == "NONE"
    assert any("cannot emit SUBJECTIVITY_ESTABLISHED" in assertion for assertion in fixture["fixture_assertions"])
