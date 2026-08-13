from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_evidence_currentness import (
    CurrentnessStatus,
    EvidenceLedger,
    EvidenceRecord,
    audit_evidence_ledger,
)

EVALUATED = "2026-08-13T07:40:00+00:00"
RETRIEVED = "2026-08-13T07:30:00+00:00"
PUBLISHED = "2026-08-01T00:00:00+00:00"


def record(record_id: str = "record:1", underlying: str = "evidence:1", *, status: CurrentnessStatus = CurrentnessStatus.CURRENT, locator: str = "https://example.org/source-1", source_id: str = "source:example-1", basis: str | None = "basis:retrieval-and-version", version: str | None = "version:1", retrieved: str | None = RETRIEVED, published: str | None = PUBLISHED, digest: str | None = "sha256:one", derived_from: str | None = None) -> EvidenceRecord:
    return EvidenceRecord(
        record_id=record_id,
        stable_source_id=source_id,
        underlying_evidence_id=underlying,
        source_locator=locator,
        authority_kind="EXTERNAL_LITERATURE",
        transformation_ref="transform:clean-room",
        claim_scope="scope:method-only",
        currentness_status=status,
        currentness_basis_ref=basis,
        source_version_ref=version,
        retrieved_at=retrieved,
        source_published_at=published,
        content_digest=digest,
        derived_from_record_id=derived_from,
    )


def ledger(*records: EvidenceRecord, **changes: object) -> EvidenceLedger:
    items = records or (record(),)
    values: dict[str, object] = {
        "ledger_id": "ledger:currentness-exp",
        "records": items,
        "evaluation_time": EVALUATED,
        "claimed_new_evidence_ids": tuple(sorted({item.underlying_evidence_id for item in items if item.underlying_evidence_id})),
        "claimed_replication_record_ids": (),
        "canonical_effect": "NONE",
        "governance_effect": "NONE",
        "deployment": False,
    }
    values.update(changes)
    return EvidenceLedger(**values)


def run(output: Path) -> dict[str, object]:
    duplicate_first = record(record_id="record:1")
    duplicate_second = record(record_id="record:2", underlying="evidence:1", locator="https://mirror.example.org/source-1", source_id="source:mirror-1", digest="sha256:one")
    derived_parent = record(record_id="record:parent", underlying="evidence:parent")
    derived_child = record(record_id="record:child", underlying="evidence:child", locator="repo:derived", source_id="source:derived", digest="sha256:derived", derived_from="record:parent")
    cases: list[tuple[str, EvidenceLedger]] = [
        ("current-unique", ledger()),
        ("stale-preserved", ledger(record(status=CurrentnessStatus.STALE, version="version:old"))),
        ("historical-preserved", ledger(record(status=CurrentnessStatus.HISTORICAL, version="version:historical"))),
        ("retrieved-unverified", ledger(record(status=CurrentnessStatus.RETRIEVED_UNVERIFIED, basis=None, version=None))),
        ("remembered-unverified", ledger(record(status=CurrentnessStatus.REMEMBERED_UNVERIFIED, basis=None, version=None, retrieved=None))),
        ("unknown-currentness", ledger(record(status=CurrentnessStatus.UNKNOWN, basis=None, version=None, retrieved=None))),
        ("duplicate-reuse", ledger(duplicate_first, duplicate_second, claimed_new_evidence_ids=("evidence:1",))),
        ("duplicate-mislabeled-replication", ledger(duplicate_first, duplicate_second, claimed_new_evidence_ids=("evidence:1",), claimed_replication_record_ids=("record:2",))),
        ("derived-record", ledger(derived_parent, derived_child, claimed_new_evidence_ids=("evidence:parent", "evidence:child"))),
        ("same-locator-relation-unknown", ledger(record(record_id="record:1"), record(record_id="record:2", underlying="evidence:2", source_id="source:other", digest="sha256:two"), claimed_new_evidence_ids=("evidence:1", "evidence:2"))),
        ("digest-contradiction", ledger(duplicate_first, record(record_id="record:2", underlying="evidence:1", locator="https://mirror.example.org/source-1", source_id="source:mirror-1", digest="sha256:two"), claimed_new_evidence_ids=("evidence:1",))),
        ("published-after-retrieval", ledger(record(published="2026-08-14T00:00:00+00:00"))),
        ("missing-stable-identity", ledger(record(source_id=None))),
        ("missing-derivation-parent", ledger(record(derived_from="record:missing"))),
        ("boundary-effect", ledger(canonical_effect="WRITE")),
    ]
    records = []
    for case_id, item in cases:
        decision = audit_evidence_ledger(item)
        records.append({"case_id": case_id, "decision": decision.as_dict()})
    payload = {
        "schema_version": "0.1.0",
        "experiment": "evidence-currentness-deduplication-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "model_execution": False,
        "observed_result": "NOT_EVALUATED",
        "scientific_conclusion": "NOT_ESTABLISHED",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "identity_continuity_conclusion": "NOT_ESTABLISHED",
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
