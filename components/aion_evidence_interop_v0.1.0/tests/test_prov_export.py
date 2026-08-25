from __future__ import annotations

import json
from pathlib import Path

from aion_evidence_interop.prov_export import export_prov


COMPONENT = Path(__file__).resolve().parents[1]


def test_prov_export_preserves_nonclaims_without_identity_inference() -> None:
    record = json.loads((COMPONENT / "fixtures" / "valid_minimal.json").read_text())
    result = export_prov(record, "components/aion_evidence_interop_v0.1.0/fixtures/valid_minimal.json")
    assert result["@context"]["prov"] == "http://www.w3.org/ns/prov#"
    assert result["aion:canonicalEffect"] == "NONE"
    assert result["aion:deployment"] is False

    source_nodes = [
        item
        for item in result["@graph"]
        if item.get("label", "").endswith("valid_minimal.json")
    ]
    assert len(source_nodes) == 1
    source = source_nodes[0]
    assert source["aion:subjectivityConclusion"] == "NOT_ESTABLISHED"
    assert source["aion:identityContinuityConclusion"] == "NOT_ESTABLISHED"
    assert "aion:declaredAssociatedWith" in source
    graph_ids = {item["@id"] for item in result["@graph"]}
    for relation in ("prov:wasDerivedFrom", "prov:wasAttributedTo"):
        assert all(item["@id"] in graph_ids for item in source[relation])
    assert "prov:wasAssociatedWith" not in source
    assert result["aion:nonclaims"] == [
        "PROV_AGENT != IDENTITY_PROOF",
        "PROVENANCE != SUBJECTIVITY",
        "PROVENANCE != MECHANISM_PROOF",
    ]
