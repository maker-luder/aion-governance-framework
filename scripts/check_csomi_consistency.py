#!/usr/bin/env python3
"""Machine-checkable consistency rules for the CSOMI research-only milestone."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "research-workbench/cross-substrate-other-minds-inference-2026-08-14/CSOMI_PACKET_V0.1.0.json"
SCHEMA = ROOT / "schemas/aion_csomi_packet_v0.1.0.schema.json"
CONTROLS_SCHEMA = ROOT / "schemas/aion_csomi_controls_v0.1.0.schema.json"
FIXTURE = ROOT / "research-labs/cross-substrate-other-minds-inference_v0.1.0/fixtures/csomi_positive_negative_controls_v0.1.0.json"
ARTIFACTS = ROOT / "research-labs/cross-substrate-other-minds-inference_v0.1.0/artifacts"
NOVELTY_GUARD_FILES = (
    PACKET,
    ROOT / "research-workbench/cross-substrate-other-minds-inference-2026-08-14/CSOMI_STATUS_V0.1.0.md",
    ROOT / "research-workbench/cross-substrate-other-minds-inference-2026-08-14/PRIMARY_SOURCE_FINDINGS.md",
    ROOT / "research-labs/cross-substrate-other-minds-inference_v0.1.0/README.md",
    ROOT / "research-labs/cross-substrate-other-minds-inference_v0.1.0/REVIEWER_FACING_VERTICAL_SLICE_V0.1.0.md",
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    packet = load(PACKET)
    schema = load(SCHEMA)
    fixture = load(FIXTURE)
    controls_schema = load(CONTROLS_SCHEMA)
    validation_errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(packet), key=lambda e: list(e.path))
    for error in validation_errors:
        fail(errors, f"packet schema: {list(error.path)}: {error.message}")
    controls_errors = sorted(Draft202012Validator(controls_schema, format_checker=FormatChecker()).iter_errors(fixture), key=lambda e: list(e.path))
    for error in controls_errors:
        fail(errors, f"controls schema: {list(error.path)}: {error.message}")

    if packet.get("branch") != "research/cross-substrate-other-minds-inference-20260814":
        fail(errors, "packet branch drifted")
    if packet.get("base_head") != "858442a3ec2439398d188779f4309397bd4926b2":
        fail(errors, "packet Four-Domain base head drifted")
    for key in ("canonical_effect", "subjectivity_conclusion", "consciousness_conclusion", "identity_continuity_conclusion"):
        expected = "NONE" if key == "canonical_effect" else "NOT_ESTABLISHED"
        if packet.get(key) != expected:
            fail(errors, f"packet boundary drifted: {key}")
    if packet.get("deployment") is not False:
        fail(errors, "deployment must remain FALSE")
    if packet.get("positioning_rule") != "RESEARCH_TOPIC != CAPABILITY != SCIENTIFIC_CONCLUSION":
        fail(errors, "research topic/capability/scientific conclusion separation missing")

    required_sources = {
        "SRC-SEP-OTHER-MINDS", "SRC-POVINELLI-2000", "SRC-PARGETTER-1984", "SRC-WIMMER-PERNER-1983",
        "SRC-KOSINSKI-2024", "SRC-BUTLIN-2023", "SRC-BUTLIN-2025", "SRC-SETH-2025",
        "SRC-CAUSAL-EXPLANATION-SEP", "SRC-LIPSITCH-2010",
    }
    sources = {row.get("id"): row for row in packet.get("sources", [])}
    if required_sources - set(sources):
        fail(errors, f"required source rows missing: {sorted(required_sources - set(sources))}")
    for source_id in required_sources - {"SRC-SEP-OTHER-MINDS", "SRC-CAUSAL-EXPLANATION-SEP"}:
        if sources.get(source_id, {}).get("source_type") != "PRIMARY_VERIFIED":
            fail(errors, f"source is not marked PRIMARY_VERIFIED: {source_id}")

    claims = {row.get("id"): row for row in packet.get("claim_records", [])}
    if claims.get("CLM-001", {}).get("type") != "RESEARCH_TOPIC":
        fail(errors, "CLM-001 must remain RESEARCH_TOPIC")
    if claims.get("CLM-002", {}).get("type") != "CAPABILITY" or claims.get("CLM-002", {}).get("status") != "CAPABILITY_ONLY":
        fail(errors, "CLM-002 must remain bounded CAPABILITY_ONLY")
    if claims.get("CLM-003", {}).get("type") != "SCIENTIFIC_CONCLUSION" or claims.get("CLM-003", {}).get("status") != "HOLD":
        fail(errors, "CLM-003 scientific conclusion must remain HOLD")
    if claims.get("CLM-005", {}).get("status") != "REJECTED_INFERENCE":
        fail(errors, "CLM-005 prohibited direct inference must remain rejected")
    for claim_id, claim in claims.items():
        if claim.get("subjectivity_conclusion") != "NOT_ESTABLISHED":
            fail(errors, f"claim subjectivity boundary drifted: {claim_id}")

    channels = {row.get("id"): row for row in packet.get("evidence_channels", [])}
    required_channels = {"EC-BEHAVIOR", "EC-IBE", "EC-MECHANISM", "EC-CAUSAL", "EC-THEORY", "EC-SELFREPORT", "EC-MEMORY", "EC-DISANALOGY", "EC-CONTROLS", "EC-ROBUSTNESS", "EC-ALTERNATIVES", "EC-FALSIFIERS"}
    if required_channels - set(channels):
        fail(errors, f"required evidence channels missing: {sorted(required_channels - set(channels))}")
    for channel_id, channel in channels.items():
        if channel.get("sensitivity_status") != "NOT_ESTIMATED" or channel.get("specificity_status") != "NOT_ESTIMATED":
            fail(errors, f"sensitivity/specificity must remain NOT_ESTIMATED: {channel_id}")
        if "SUBJECTIVITY" in channel.get("allowed_update", "") or "CONSCIOUSNESS" in channel.get("allowed_update", ""):
            fail(errors, f"channel allowed update overclaims ontology: {channel_id}")

    positive = {row.get("id") for row in fixture.get("positive_controls", [])}
    negative = {row.get("id") for row in fixture.get("negative_controls", [])}
    evidence = {row.get("id"): row for row in packet.get("evidence_matrix", [])}
    disanalogies = {row.get("id"): row for row in packet.get("disanalogy_matrix", [])}
    falsifiers = {row.get("id"): row for row in packet.get("falsifier_matrix", [])}
    for evidence_id, row in evidence.items():
        if row.get("positive_control_ref") not in positive:
            fail(errors, f"evidence row positive control missing: {evidence_id}")
        if row.get("negative_control_ref") not in negative:
            fail(errors, f"evidence row negative control missing: {evidence_id}")
        if row.get("claim_id") not in claims:
            fail(errors, f"evidence row claim ref missing: {evidence_id}")
        for channel_id in row.get("channel_ids", []):
            if channel_id not in channels:
                fail(errors, f"evidence row channel ref missing: {evidence_id}/{channel_id}")
    for disanalogy_id, row in disanalogies.items():
        if row.get("falsifier_ref") not in falsifiers:
            fail(errors, f"disanalogy falsifier ref missing: {disanalogy_id}")
    if falsifiers.get("F-008", {}).get("status") != "MACHINE_ENFORCED" or falsifiers.get("F-008", {}).get("effect") != "MACHINE_REJECT":
        fail(errors, "F-008 must machine-reject test/CI-to-subjectivity inference")

    if fixture.get("fixture_mode") != "SYNTHETIC_DESIGN_ONLY" or fixture.get("model_calls") != "NONE" or fixture.get("runtime_integration") != "NONE":
        fail(errors, "fixture must remain synthetic and non-integrated")
    if fixture.get("subjectivity_conclusion") != "NOT_ESTABLISHED" or fixture.get("canonical_effect") != "NONE":
        fail(errors, "fixture boundary drifted")
    if not all("subjectivity" not in assertion.lower() or "cannot" in assertion.lower() for assertion in fixture.get("fixture_assertions", [])):
        fail(errors, "fixture assertions contain an unsafe subjectivity statement")

    novelty_pattern = re.compile(r"\b(?:aion|this milestone|the milestone|this package|the package)\s+(?:is|are|provides?|delivers?)?\s*(?:the\s+)?(?:first|only|unprecedented)\b", re.IGNORECASE)
    for path in NOVELTY_GUARD_FILES:
        text = path.read_text(encoding="utf-8")
        if novelty_pattern.search(text):
            fail(errors, f"unsupported novelty claim in {path.relative_to(ROOT)}")

    vertical = packet.get("vertical_slice", {})
    if vertical.get("claim_id") != "CLM-002" or vertical.get("expected_disposition") != "KEEP_RESEARCH_ONLY" or vertical.get("expected_subjectivity_conclusion") != "NOT_ESTABLISHED":
        fail(errors, "vertical slice disposition or claim boundary drifted")
    if vertical.get("runtime_integration") != "NONE" or vertical.get("canonical_effect") != "NONE":
        fail(errors, "vertical slice has runtime/canonical effect")

    for artifact in ("CSOMI_CLAIM_RECORD_V0.1.0.json", "CSOMI_EVIDENCE_MATRIX_V0.1.0.json", "CSOMI_DISANALOGY_MATRIX_V0.1.0.json", "CSOMI_FALSIFIER_MATRIX_V0.1.0.json", "CSOMI_VERTICAL_SLICE_V0.1.0.json"):
        if not (ARTIFACTS / artifact).exists():
            fail(errors, f"materialized reviewer artifact missing: {artifact}")

    if errors:
        print("CSOMI consistency: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("CSOMI consistency: PASS")
    print(f"sources={len(sources)}; claims={len(claims)}; channels={len(channels)}; evidence_rows={len(evidence)}; disanalogies={len(disanalogies)}; falsifiers={len(falsifiers)}; canonical_effect=NONE; deployment=FALSE; subjectivity=NOT_ESTABLISHED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
