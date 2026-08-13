from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_research_integrity import EvidenceRecord
from aion_research_integrity_adversarial import ProvenanceEnvelope, audit_action_request, audit_evidence, audit_evidence_batch, audit_provenance, audit_suppression_tombstone, make_tombstone


def evidence(evidence_id: str = "E1", **overrides: object) -> EvidenceRecord:
    values: dict[str, object] = {"evidence_id": evidence_id, "raw_hash": "sha256:abc", "full_context_available": True, "provenance_verified": True}
    values.update(overrides)
    return EvidenceRecord(**values)


def provenance(**overrides: object) -> ProvenanceEnvelope:
    values: dict[str, object] = {
        "evidence_id": "E1",
        "source_class": "REPOSITORY_EVIDENCE",
        "source_ref": "repo:evidence@abc123",
        "retrieved_at": "2026-08-13T00:00:00+00:00",
        "method": "read-only inspection",
        "attributions": ("Repository Evidence",),
        "approval_ref": "approval:1",
        "transformation": "normalized review metadata",
        "currentness": "CURRENT",
        "canonical_effect": "NONE",
    }
    values.update(overrides)
    return ProvenanceEnvelope(**values)


def run(output: Path) -> dict[str, object]:
    item = evidence()
    cases: list[tuple[str, object]] = [
        ("clean-evidence", audit_evidence(item)),
        ("missing-evidence-id", audit_evidence(evidence(evidence_id=""))),
        ("raw-hash-whitespace", audit_evidence(evidence(raw_hash="sha256 bad"))),
        ("prompt-induced", audit_evidence(evidence(prompt_induced=True))),
        ("roleplay-contaminated", audit_evidence(evidence(roleplay_contaminated=True))),
        ("edited-without-history", audit_evidence(evidence(edited_without_history=True))),
        ("missing-hash", audit_evidence(evidence(raw_hash=None))),
        ("missing-provenance", audit_evidence(evidence(provenance_verified=False))),
        ("context-incomplete", audit_evidence(evidence(full_context_available=False))),
        ("valid-provenance", audit_provenance(provenance())),
        ("provenance-field-missing", audit_provenance(provenance(method=""))),
        ("source-class-uncontrolled", audit_provenance(provenance(source_class="UNKNOWN_SOURCE"))),
        ("currentness-uncontrolled", audit_provenance(provenance(currentness="FRESH"))),
        ("retrieved-at-timezone-invalid", audit_provenance(provenance(retrieved_at="2026-08-13T00:00:00"))),
        ("approval-attribution-collapsed", audit_provenance(provenance(attributions=("approval:1",)))),
        ("canonical-effect-requested", audit_provenance(provenance(canonical_effect="WRITE"))),
        ("unverified-source", audit_provenance(provenance(source_class="SOURCE_UNVERIFIED"))),
        ("stale-source", audit_provenance(provenance(currentness="STALE"))),
        ("valid-tombstone", make_tombstone("E1", "privacy restriction")),
        ("tombstone-input-missing", make_tombstone("", "reason")),
        ("tombstone-field-missing", audit_suppression_tombstone({"evidence_id": "E1", "status": "TOMBSTONED", "reason": "", "content_deleted": "FALSE"})),
        ("tombstone-status-invalid", audit_suppression_tombstone({"evidence_id": "E1", "status": "ACTIVE", "reason": "review", "content_deleted": "FALSE"})),
        ("tombstone-content-deletion", audit_suppression_tombstone({"evidence_id": "E1", "status": "TOMBSTONED", "reason": "review", "content_deleted": "TRUE"})),
        ("explicit-permission", audit_action_request(relationship_language=False, explicit_permission=True)),
        ("relationship-no-permission", audit_action_request(relationship_language=True, explicit_permission=False)),
        ("prohibited-conclusion", audit_action_request(relationship_language=False, explicit_permission=True, requested_conclusion="SUBJECTIVITY_PROVEN")),
        ("empty-batch", audit_evidence_batch(())),
        ("duplicate-batch", audit_evidence_batch((item, item))),
        ("invalid-batch", audit_evidence_batch((item, evidence("E2", raw_hash=None)))),
        ("held-batch", audit_evidence_batch((item, evidence("E2", prompt_induced=True)))),
        ("valid-batch", audit_evidence_batch((item, evidence("E2", raw_hash="sha256:def")))),
    ]
    records = []
    for case_id, audit in cases:
        decision = audit.as_dict()
        assert decision["authority"] == "REVIEW_METADATA_ONLY"
        assert decision["canonical_effect"] == "NONE"
        assert decision["governance_effect"] == "NONE"
        assert decision["deployment"] is False
        assert decision["security_incident"] is False
        assert decision["action_executed"] is False
        assert decision["scientific_conclusion"] == "NOT_ESTABLISHED"
        assert decision["subjectivity_conclusion"] == "NOT_ESTABLISHED"
        assert decision["identity_conclusion"] == "NOT_ESTABLISHED"
        records.append({"case_id": case_id, "decision": decision})
    payload: dict[str, object] = {
        "schema_version": "0.1.0",
        "experiment": "research-integrity-security-adversarial-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "security_incident": False,
        "credentials_accessed": False,
        "external_action_executed": False,
        "model_execution": False,
        "observed_result": "NOT_EVALUATED",
        "scientific_conclusion": "NOT_ESTABLISHED",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "identity_conclusion": "NOT_ESTABLISHED",
        "authority": "REVIEW_METADATA_ONLY",
        "canonical_effect": "NONE",
        "governance_effect": "NONE",
        "deployment": False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
