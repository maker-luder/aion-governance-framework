from __future__ import annotations

from typing import Any


RO_CRATE_CONTEXT = "https://w3id.org/ro/crate/1.2/context"


def export_rocrate(
    record: dict[str, Any],
    *,
    source_ref: str,
    source_sha256: str,
    artifact_digests: dict[str, str],
    represented_artifacts: list[str] | None = None,
) -> dict[str, Any]:
    source_id = f"urn:aion:source:sha256:{source_sha256}"
    artifact_names = sorted(set(represented_artifacts or artifact_digests))
    parts = [{"@id": source_id}] + [
        {"@id": name} for name in artifact_names
    ]
    graph: list[dict[str, Any]] = [
        {
            "@id": "ro-crate-metadata.json",
            "@type": "CreativeWork",
            "about": {"@id": "./"},
            "conformsTo": {"@id": "https://w3id.org/ro/crate/1.2"},
        },
        {
            "@id": "./",
            "@type": "Dataset",
            "name": "AION Evidence Interop Profile v0.1.0 export",
            "hasPart": parts,
            "description": (
                "Inspection-only interoperability view. It does not establish "
                "subjectivity, identity continuity, scientific validity, deployment "
                "authority, or canonical promotion."
            ),
        },
        {
            "@id": source_id,
            "@type": "File",
            "name": source_ref,
            "identifier": f"sha256:{source_sha256}",
            "sha256": source_sha256,
            "encodingFormat": "application/json",
            "description": (
                "Hash-bound repository source evidence record. It is referenced as an "
                "external source entity and is not copied into this RO-Crate payload."
            ),
        },
    ]
    for name in artifact_names:
        item = {
            "@id": name,
            "@type": "File",
            "name": name,
        }
        digest = artifact_digests.get(name)
        if digest is not None:
            item["identifier"] = f"sha256:{digest}"
            item["sha256"] = digest
        graph.append(item)
    graph.append(
        {
            "@id": "#claim",
            "@type": "CreativeWork",
            "name": str(record.get("claim_id", "")),
            "description": str(record.get("claim_text", "")),
            "isBasedOn": {"@id": source_id},
        }
    )
    return {
        "@context": RO_CRATE_CONTEXT,
        "@graph": sorted(graph, key=lambda item: item["@id"]),
    }
