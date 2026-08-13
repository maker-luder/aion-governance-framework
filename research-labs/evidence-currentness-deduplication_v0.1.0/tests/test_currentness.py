from __future__ import annotations

from aion_evidence_currentness import (
    CurrentnessStatus,
    EvidenceLedger,
    EvidenceRecord,
    LedgerStatus,
    RelationType,
    audit_evidence_ledger,
)


EVALUATED = "2026-08-13T07:40:00+00:00"
RETRIEVED = "2026-08-13T07:30:00+00:00"
PUBLISHED = "2026-08-01T00:00:00+00:00"


def record(
    record_id: str = "record:1",
    underlying: str = "evidence:1",
    *,
    status: CurrentnessStatus = CurrentnessStatus.CURRENT,
    locator: str = "https://example.org/source-1",
    source_id: str = "source:example-1",
    basis: str | None = "basis:retrieval-and-version",
    version: str | None = "version:1",
    retrieved: str | None = RETRIEVED,
    published: str | None = PUBLISHED,
    digest: str | None = "sha256:one",
    derived_from: str | None = None,
) -> EvidenceRecord:
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
    values: dict[str, object] = {
        "ledger_id": "ledger:currentness-001",
        "records": records or (record(),),
        "evaluation_time": EVALUATED,
        "claimed_new_evidence_ids": tuple(sorted({item.underlying_evidence_id for item in (records or (record(),)) if item.underlying_evidence_id})),
        "claimed_replication_record_ids": (),
        "canonical_effect": "NONE",
        "governance_effect": "NONE",
        "deployment": False,
    }
    values.update(changes)
    return EvidenceLedger(**values)


def test_current_unique_evidence_is_admissible() -> None:
    result = audit_evidence_ledger(ledger())
    assert result.status is LedgerStatus.COMPLETE
    assert result.reason == "EVIDENCE_LEDGER_ADMISSIBLE_WITH_REUSE_DISTINCTION"
    assert result.current_record_ids == ("record:1",)
    assert result.unique_underlying_evidence_count == 1
    assert result.relations == (("record:1", RelationType.UNIQUE_UNDERLYING_EVIDENCE),)


def test_stale_record_is_preserved_but_not_current() -> None:
    result = audit_evidence_ledger(ledger(record(status=CurrentnessStatus.STALE, version="version:old")))
    assert result.status is LedgerStatus.COMPLETE
    assert result.stale_record_ids == ("record:1",)
    assert result.current_record_ids == ()


def test_historical_record_is_preserved_for_review() -> None:
    result = audit_evidence_ledger(ledger(record(status=CurrentnessStatus.HISTORICAL, version="version:historical")))
    assert result.status is LedgerStatus.COMPLETE
    assert result.stale_record_ids == ("record:1",)


def test_retrieved_unverified_is_not_current() -> None:
    item = record(status=CurrentnessStatus.RETRIEVED_UNVERIFIED, basis=None, version=None)
    result = audit_evidence_ledger(ledger(item))
    assert result.status is LedgerStatus.COMPLETE
    assert result.unverified_record_ids == ("record:1",)


def test_remembered_unverified_is_held() -> None:
    item = record(status=CurrentnessStatus.REMEMBERED_UNVERIFIED, basis=None, version=None, retrieved=None)
    result = audit_evidence_ledger(ledger(item))
    assert result.status is LedgerStatus.INDETERMINATE
    assert result.reason == "REMEMBERED_SOURCE_NOT_ADMISSIBLE"


def test_unknown_currentness_is_held() -> None:
    item = record(status=CurrentnessStatus.UNKNOWN, basis=None, version=None, retrieved=None)
    result = audit_evidence_ledger(ledger(item))
    assert result.status is LedgerStatus.INDETERMINATE
    assert result.reason == "CURRENTNESS_UNKNOWN"


def test_missing_stable_identity_is_indeterminate() -> None:
    result = audit_evidence_ledger(ledger(record(source_id=None)))
    assert result.status is LedgerStatus.INDETERMINATE
    assert "record:1.stable_source_id" in result.missing_fields


def test_missing_currentness_basis_is_indeterminate() -> None:
    result = audit_evidence_ledger(ledger(record(basis=None)))
    assert result.status is LedgerStatus.INDETERMINATE
    assert "record:1.currentness_basis_ref" in result.missing_fields


def test_current_record_requires_source_version() -> None:
    result = audit_evidence_ledger(ledger(record(version=None)))
    assert result.status is LedgerStatus.INDETERMINATE
    assert "record:1.source_version_ref" in result.missing_fields


def test_duplicate_records_share_one_underlying_evidence_count() -> None:
    first = record(record_id="record:1")
    second = record(record_id="record:2", underlying="evidence:1", locator="https://mirror.example.org/source-1", source_id="source:mirror-1", digest="sha256:one")
    result = audit_evidence_ledger(ledger(first, second, claimed_new_evidence_ids=("evidence:1",)))
    assert result.status is LedgerStatus.COMPLETE
    assert result.unique_underlying_evidence_count == 1
    assert result.reused_underlying_evidence_count == 1
    assert dict(result.relations)["record:2"] is RelationType.SAME_UNDERLYING_EVIDENCE
    assert result.duplicate_groups == (("evidence:1", ("record:1", "record:2")),)


def test_duplicate_underlying_evidence_mislabeled_as_replication_is_invalid() -> None:
    first = record(record_id="record:1")
    second = record(record_id="record:2", underlying="evidence:1", locator="https://mirror.example.org/source-1", source_id="source:mirror-1", digest="sha256:one")
    result = audit_evidence_ledger(ledger(first, second, claimed_new_evidence_ids=("evidence:1",), claimed_replication_record_ids=("record:2",)))
    assert result.status is LedgerStatus.INVALID
    assert result.reason == "DUPLICATION_MISLABELED_AS_REPLICATION"


def test_derived_record_is_not_counted_as_unique_underlying_evidence() -> None:
    parent = record(record_id="record:1", underlying="evidence:1")
    child = record(record_id="record:2", underlying="evidence:2", locator="repo:derived-record", source_id="source:derived", digest="sha256:derived", derived_from="record:1")
    result = audit_evidence_ledger(ledger(parent, child, claimed_new_evidence_ids=("evidence:1", "evidence:2")))
    assert result.status is LedgerStatus.COMPLETE
    assert dict(result.relations)["record:2"] is RelationType.DERIVED_RECORD
    assert result.unique_underlying_evidence_count == 2


def test_same_locator_with_unresolved_underlying_relation_is_indeterminate() -> None:
    first = record(record_id="record:1", underlying="evidence:1")
    second = record(record_id="record:2", underlying="evidence:2", source_id="source:other", digest="sha256:two")
    result = audit_evidence_ledger(ledger(first, second, claimed_new_evidence_ids=("evidence:1", "evidence:2")))
    assert result.status is LedgerStatus.INDETERMINATE
    assert result.reason == "SAME_LOCATOR_RELATION_UNKNOWN"


def test_same_underlying_digest_contradiction_is_invalid() -> None:
    first = record(record_id="record:1", digest="sha256:one")
    second = record(record_id="record:2", underlying="evidence:1", locator="https://mirror.example.org/source-1", source_id="source:mirror-1", digest="sha256:two")
    result = audit_evidence_ledger(ledger(first, second, claimed_new_evidence_ids=("evidence:1",)))
    assert result.status is LedgerStatus.INVALID
    assert result.reason == "UNDERLYING_EVIDENCE_DIGEST_CONTRADICTION"


def test_published_after_retrieval_is_invalid() -> None:
    item = record(published="2026-08-14T00:00:00+00:00")
    result = audit_evidence_ledger(ledger(item))
    assert result.status is LedgerStatus.INVALID
    assert result.reason == "SOURCE_PUBLISHED_AFTER_RETRIEVAL"


def test_record_id_collision_is_invalid() -> None:
    result = audit_evidence_ledger(ledger(record(record_id="record:same"), record(record_id="record:same", underlying="evidence:2", locator="repo:second", source_id="source:second", digest="sha256:two"), claimed_new_evidence_ids=("evidence:1", "evidence:2")))
    assert result.status is LedgerStatus.INVALID
    assert result.reason == "RECORD_ID_COLLISION"


def test_missing_derivation_parent_is_indeterminate() -> None:
    item = record(derived_from="record:missing")
    result = audit_evidence_ledger(ledger(item))
    assert result.status is LedgerStatus.INDETERMINATE
    assert result.reason == "DERIVATION_PARENT_MISSING"


def test_self_derivation_is_invalid() -> None:
    item = record(derived_from="record:1")
    result = audit_evidence_ledger(ledger(item))
    assert result.status is LedgerStatus.INVALID
    assert result.reason == "SELF_DERIVATION"


def test_boundary_effect_is_invalid() -> None:
    for changes in ({"canonical_effect": "WRITE"}, {"governance_effect": "PROMOTE"}, {"deployment": True}):
        result = audit_evidence_ledger(ledger(**changes))
        assert result.status is LedgerStatus.INVALID
        assert result.reason == "BOUNDARY_EFFECT_REQUESTED"


def test_invalid_evaluation_time_is_indeterminate() -> None:
    result = audit_evidence_ledger(ledger(evaluation_time="not-a-time"))
    assert result.status is LedgerStatus.INDETERMINATE
    assert result.reason == "EVALUATION_TIME_INVALID"


def test_remembered_record_with_retrieval_is_contradictory() -> None:
    item = record(status=CurrentnessStatus.REMEMBERED_UNVERIFIED, basis=None, version=None)
    result = audit_evidence_ledger(ledger(item))
    assert result.status is LedgerStatus.INVALID
    assert result.reason == "REMEMBERED_STATUS_CONTRADICTS_RETRIEVAL"
