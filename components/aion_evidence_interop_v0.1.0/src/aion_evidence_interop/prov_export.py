from __future__ import annotations

import hashlib
from typing import Any


PROV_CONTEXT = {
    "prov": "http://www.w3.org/ns/prov#",
    "aion": "https://example.invalid/aion/interop#",
    "label": "http://www.w3.org/2000/01/rdf-schema#label",
    "prov:wasDerivedFrom": {"@type": "@id"},
    "prov:wasAttributedTo": {"@type": "@id"},
}


def _node_id(kind: str, value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return f"urn:aion:{kind}:{digest}"


def _refs(kind: str, values: list[str]) -> list[dict[str, str]]:
    return [{"@id": _node_id(kind, item)} for item in sorted(set(values))]


def export_prov(record: dict[str, Any], source_ref: str) -> dict[str, Any]:
    provenance = record.get("provenance", {})
    entities = (
        [source_ref]
        + list(provenance.get("entities", []))
        + list(provenance.get("derived_from", []))
    )
    activities = list(provenance.get("activities", []))
    agents = list(provenance.get("agents", [])) + list(
        provenance.get("attributed_to", [])
    )

    graph: list[dict[str, Any]] = []
    for value in sorted(set(str(item) for item in entities)):
        graph.append(
            {
                "@id": _node_id("entity", value),
                "@type": "prov:Entity",
                "label": value,
            }
        )
    for value in sorted(set(str(item) for item in activities)):
        graph.append(
            {
                "@id": _node_id("activity", value),
                "@type": "prov:Activity",
                "label": value,
            }
        )
    for value in sorted(set(str(item) for item in agents)):
        graph.append(
            {
                "@id": _node_id("agent", value),
                "@type": "prov:Agent",
                "label": value,
            }
        )

    source_node = {
        "@id": _node_id("entity", source_ref),
        "@type": "prov:Entity",
        "label": source_ref,
        "prov:wasDerivedFrom": _refs(
            "entity", [str(v) for v in provenance.get("derived_from", [])]
        ),
        "prov:wasAttributedTo": _refs(
            "agent", [str(v) for v in provenance.get("attributed_to", [])]
        ),
        "aion:subjectivityConclusion": "NOT_ESTABLISHED",
        "aion:identityContinuityConclusion": "NOT_ESTABLISHED",
    }
    graph = [item for item in graph if item["@id"] != source_node["@id"]]
    graph.append(source_node)

    if provenance.get("associated_with"):
        source_node["aion:declaredAssociatedWith"] = sorted(
            str(v) for v in provenance.get("associated_with", [])
        )

    return {
        "@context": PROV_CONTEXT,
        "@graph": sorted(graph, key=lambda item: item["@id"]),
        "aion:profileVersion": "0.1.0",
        "aion:canonicalEffect": "NONE",
        "aion:deployment": False,
        "aion:nonclaims": [
            "PROV_AGENT != IDENTITY_PROOF",
            "PROVENANCE != SUBJECTIVITY",
            "PROVENANCE != MECHANISM_PROOF",
        ],
    }
