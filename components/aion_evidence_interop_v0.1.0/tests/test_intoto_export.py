from __future__ import annotations

from aion_evidence_interop.intoto_export import export_intoto


def test_intoto_attestation_does_not_infer_authority() -> None:
    result = export_intoto(
        {"claim_id": "c1", "result_status": "NOT_RUN"},
        source_ref="qa/evidence.json",
        source_sha256="a" * 64,
        expected_head="b" * 40,
        artifact_digests={"prov.jsonld": "c" * 64},
    )
    assert result["_type"] == "https://in-toto.io/Statement/v1"
    predicate = result["predicate"]
    assert predicate["signatureStatus"] == "UNSIGNED_REFERENCE"
    assert predicate["humanApproval"] == "NOT_INFERRED"
    assert predicate["mergeAuthority"] == "NOT_INFERRED"
    assert predicate["canonicalEffect"] == "NONE"
    assert predicate["deployment"] is False
    assert predicate["modelExecution"] is False
