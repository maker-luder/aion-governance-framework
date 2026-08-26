from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "evidence" / "external_sources_v0.1.0.json"
DISCOVERY_NOTE = ROOT / "docs" / "LATENT_REGULATORY_STATE_DISCOVERY.md"


def _catalog() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def test_evidence_catalog_contains_regulation_sources():
    source_ids = {item["source_id"] for item in _catalog()["sources"]}
    assert {
        "LEE_ET_AL_INTEROCEPTIVE_AI_2026",
        "CANDIA_RIVERA_INTEROCEPTIVE_MACHINE_2026",
        "STEVENSON_PHYSIOLOGICAL_STABILITY_2024",
        "PLANT_INTERCELLULAR_REGULATION_2010",
    } <= source_ids


def test_external_research_inputs_are_not_vendored_by_default():
    assert all(item["vendored"] is False for item in _catalog()["sources"])


def test_discovery_protocol_keeps_functional_nonclaims():
    text = DISCOVERY_NOTE.read_text(encoding="utf-8")
    assert "DISCOVERED_REGULATORY_VARIABLE != FELT_NEED" in text
    assert "FUNCTIONAL_SELF_REGULATION != SELF_AWARENESS" in text
    assert "INTERNAL_STATE_DISCOVERY != SUBJECTIVITY" in text
    assert "Status: `DOCUMENTED / NOT IMPLEMENTED`" in text
