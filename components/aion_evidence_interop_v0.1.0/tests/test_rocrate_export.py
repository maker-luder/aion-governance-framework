from __future__ import annotations

import json
from pathlib import Path

from aion_evidence_interop.rocrate_export import export_rocrate


COMPONENT = Path(__file__).resolve().parents[1]


def test_rocrate_is_metadata_only_and_noncanonical() -> None:
    record = json.loads((COMPONENT / "fixtures" / "valid_minimal.json").read_text())
    result = export_rocrate(
        record,
        source_ref="components/aion_evidence_interop_v0.1.0/fixtures/valid_minimal.json",
        source_sha256="a" * 64,
        artifact_digests={"prov.jsonld": "b" * 64},
    )
    assert result["@context"] == "https://w3id.org/ro/crate/1.2/context"
    root = next(item for item in result["@graph"] if item["@id"] == "./")
    assert "does not establish" in root["description"]
    source = next(
        item
        for item in result["@graph"]
        if item["@id"] == f"urn:aion:source:sha256:{'a' * 64}"
    )
    assert source["identifier"] == f"sha256:{'a' * 64}"
    assert source["contentUrl"].endswith("valid_minimal.json")
