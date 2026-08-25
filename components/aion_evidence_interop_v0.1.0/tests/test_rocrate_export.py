from __future__ import annotations

import json
from pathlib import Path

from aion_evidence_interop.rocrate_export import export_rocrate


COMPONENT = Path(__file__).resolve().parents[1]


def test_rocrate_is_rooted_at_bundle_and_noncanonical() -> None:
    record = json.loads((COMPONENT / "fixtures" / "valid_minimal.json").read_text())
    result = export_rocrate(
        record,
        source_ref="components/aion_evidence_interop_v0.1.0/fixtures/valid_minimal.json",
        source_sha256="a" * 64,
        artifact_digests={"prov.jsonld": "b" * 64},
        represented_artifacts=["prov.jsonld", "attestation.intoto.json", "opa/input.json"],
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
    assert source["sha256"] == "a" * 64
    assert source["name"].endswith("valid_minimal.json")
    assert "contentUrl" not in source
    graph = {item["@id"]: item for item in result["@graph"]}
    assert graph["prov.jsonld"]["sha256"] == "b" * 64
    assert "sha256" not in graph["attestation.intoto.json"]
    assert "opa/input.json" in graph
    assert all(not item_id.startswith("../") for item_id in graph)
    assert [item["@id"] for item in result["@graph"]] == sorted(graph)
    metadata = graph["ro-crate-metadata.json"]
    assert metadata["conformsTo"]["@id"] == "https://w3id.org/ro/crate/1.2"
    payload_ids = {part["@id"] for part in root["hasPart"]}
    assert {"prov.jsonld", "attestation.intoto.json", "opa/input.json"}.issubset(payload_ids)
