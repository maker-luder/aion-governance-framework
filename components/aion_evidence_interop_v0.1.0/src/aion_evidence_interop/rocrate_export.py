from __future__ import annotations

from typing import Any


RO_CRATE_CONTEXT = "https://w3id.org/ro/crate/1.2/context"


def export_rocrate(
    record: dict[str, Any],
    *,
    source_ref: str,
    source_sha256: str,
    artifact_digests: dict[str, str],
) -> dict[str, Any]:
    source_id = f"urn:aion:source:sha256:{source_sha256}"
    parts = [
        {"@id": source_id},
        {"@id": "../prov.jsonld"},
        {"@id": "../attestation.intoto.json"},
        {"@id": "../inspect/task-manifest.json"},
        {"@id": "../inspect/dataset.jsonl"},
    ]
    graph: list[dict[str, Any]] = [
        {
            "@id": "ro-crate-metadata.json",
            "@type": "CreativeWork",
            "about": {"@id": "./"},
            "conformsTo": {"@id": RO_CRATE_CONTEXT},
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
            "name": "AION source research evidence record",
            "identifier": f"sha256:{source_sha256}",
            "contentUrl": source_ref,
        },
    ]
    for name, digest in sorted(artifact_digests.items()):
        graph.append(
            {
                "@id": f"../{name}" if not name.startswith("ro-crate/") else name.removeprefix("ro-crate/"),
                "@type": "File",
                "identifier": f"sha256:{digest}",
            }
        )
    graph.append(
        {
            "@id": "#claim",
            "@type": "CreativeWork",
            "name": str(record.get("claim_id", "")),
            "description": str(record.get("claim_text", "")),
            "isBasedOn": {"@id": source_id},
        }
    )
    return {"@context": RO_CRATE_CONTEXT, "@graph": graph}
