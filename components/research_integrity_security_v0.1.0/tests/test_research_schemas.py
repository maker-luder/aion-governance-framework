from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def load_schema(name: str) -> dict[str, object]:
    path = ROOT / "schemas" / name
    return json.loads(path.read_text(encoding="utf-8"))


def test_research_evidence_schema_is_valid_json_and_locks_canonical_effect() -> None:
    schema = load_schema("research_evidence_record.schema.json")
    properties = schema["properties"]
    assert isinstance(properties, dict)
    assert properties["canonical_effect"] == {"const": "NONE"}


def test_provenance_schema_is_valid_json_and_separates_approval() -> None:
    schema = load_schema("provenance_record.schema.json")
    properties = schema["properties"]
    assert isinstance(properties, dict)
    assert "attributions" in properties
    assert "approval" in properties
    assert properties["canonical_effect"] == {"const": "NONE"}


def test_provenance_schema_preserves_unverified_source_class() -> None:
    schema = load_schema("provenance_record.schema.json")
    source_class = schema["properties"]["source_class"]
    assert "SOURCE_UNVERIFIED" in source_class["enum"]
