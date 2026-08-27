from __future__ import annotations

import json

from aion_bounded_research_loop import export_interop_views, extended_run_to_research_evidence_record
from test_extended_evidence_binding import extended_report


def test_extended_record_exports_all_reused_interop_views_without_authority() -> None:
    _, report = extended_report()
    expected_head = "a" * 40
    record = extended_run_to_research_evidence_record(
        report,
        repository_commit=expected_head,
        protocol_ref="research-labs/bounded-autonomous-research-loop_v0.1.0/docs/PROTOCOL.md",
        protocol_hash="b" * 64,
        source_refs=("fixture:seven-state",),
    )
    views = export_interop_views(
        record,
        source_ref="fixture:seven-state-record",
        expected_head=expected_head,
    )

    assert set(views) == {
        "source-evidence.json",
        "prov.jsonld",
        "ro-crate-metadata.json",
        "attestation.intoto.json",
        "inspect/task-manifest.json",
        "inspect/dataset.jsonl",
    }
    assert all(isinstance(value, bytes) and value for value in views.values())

    source_record = json.loads(views["source-evidence.json"])
    assert source_record["claim_id"] == record["claim_id"]
    assert source_record["result_status"] == "HOLD"
    assert source_record["canonical_effect"] == "NONE"

    attestation = json.loads(views["attestation.intoto.json"])
    predicate = attestation["predicate"]
    assert attestation["_type"] == "https://in-toto.io/Statement/v1"
    assert predicate["source"]["codeCommit"] == expected_head
    assert predicate["source"]["claimId"] == record["claim_id"]
    assert predicate["signatureStatus"] == "UNSIGNED_REFERENCE"
    assert predicate["humanApproval"] == "NOT_INFERRED"
    assert predicate["mergeAuthority"] == "NOT_INFERRED"
    assert predicate["canonicalEffect"] == "NONE"
    assert predicate["deployment"] is False
    assert predicate["researchExecution"] is False
    assert predicate["modelExecution"] is False
    assert predicate["networkAccess"] is False

    prov = json.loads(views["prov.jsonld"])
    rocrate = json.loads(views["ro-crate-metadata.json"])
    inspect_task = json.loads(views["inspect/task-manifest.json"])
    inspect_sample = json.loads(views["inspect/dataset.jsonl"])
    assert prov
    assert rocrate
    assert inspect_task
    assert inspect_sample
