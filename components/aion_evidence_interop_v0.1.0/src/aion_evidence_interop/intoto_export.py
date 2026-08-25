from __future__ import annotations

from typing import Any


PREDICATE_TYPE = "https://example.invalid/aion/interop/derivation/v0.1.0"


def export_intoto(
    record: dict[str, Any],
    *,
    source_ref: str,
    source_sha256: str,
    expected_head: str,
    artifact_digests: dict[str, str],
) -> dict[str, Any]:
    return {
        "_type": "https://in-toto.io/Statement/v1",
        "subject": [
            {
                "name": name,
                "digest": {"sha256": digest},
            }
            for name, digest in sorted(artifact_digests.items())
        ],
        "predicateType": PREDICATE_TYPE,
        "predicate": {
            "transformer": {
                "name": "aion-evidence-interop",
                "version": "0.1.0",
            },
            "source": {
                "codeCommit": expected_head,
                "claimId": str(record.get("claim_id", "")),
                "resultStatus": str(record.get("result_status", "")),
            },
            "materials": [
                {
                    "uri": source_ref,
                    "digest": {"sha256": source_sha256},
                },
                {
                    "uri": "git+repository:aion-governance-framework",
                    "digest": {"sha1": expected_head},
                },
            ],
            "derivedArtifacts": [
                {"name": name, "digest": {"sha256": digest}}
                for name, digest in sorted(artifact_digests.items())
            ],
            "signatureStatus": "UNSIGNED_REFERENCE",
            "humanApproval": "NOT_INFERRED",
            "mergeAuthority": "NOT_INFERRED",
            "canonicalEffect": "NONE",
            "deployment": False,
            "researchExecution": False,
            "modelExecution": False,
            "networkAccess": False,
        },
    }
