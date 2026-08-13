from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any


class CurrentnessStatus(StrEnum):
    CURRENT = "CURRENT"
    STALE = "STALE"
    HISTORICAL = "HISTORICAL"
    RETRIEVED_UNVERIFIED = "RETRIEVED_UNVERIFIED"
    REMEMBERED_UNVERIFIED = "REMEMBERED_UNVERIFIED"
    UNKNOWN = "UNKNOWN"


class RelationType(StrEnum):
    UNIQUE_UNDERLYING_EVIDENCE = "UNIQUE_UNDERLYING_EVIDENCE"
    SAME_UNDERLYING_EVIDENCE = "SAME_UNDERLYING_EVIDENCE"
    DERIVED_RECORD = "DERIVED_RECORD"
    RELATION_UNKNOWN = "RELATION_UNKNOWN"


class LedgerStatus(StrEnum):
    COMPLETE = "COMPLETE"
    INDETERMINATE = "INDETERMINATE"
    INVALID = "INVALID"


class Disposition(StrEnum):
    ADMISSIBLE_FOR_REVIEW = "ADMISSIBLE_FOR_REVIEW"
    HOLD = "HOLD"


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    record_id: str
    stable_source_id: str | None
    underlying_evidence_id: str | None
    source_locator: str | None
    authority_kind: str | None
    transformation_ref: str | None
    claim_scope: str | None
    currentness_status: CurrentnessStatus
    currentness_basis_ref: str | None
    source_version_ref: str | None
    retrieved_at: str | None
    source_published_at: str | None = None
    content_digest: str | None = None
    derived_from_record_id: str | None = None


@dataclass(frozen=True, slots=True)
class EvidenceLedger:
    ledger_id: str
    records: tuple[EvidenceRecord, ...]
    evaluation_time: str | None
    claimed_new_evidence_ids: tuple[str, ...] = ()
    claimed_replication_record_ids: tuple[str, ...] = ()
    canonical_effect: str = "NONE"
    governance_effect: str = "NONE"
    deployment: bool = False


@dataclass(frozen=True, slots=True)
class LedgerDecision:
    status: LedgerStatus
    disposition: Disposition
    reason: str
    ledger_id: str
    missing_fields: tuple[str, ...] = ()
    contradiction_fields: tuple[str, ...] = ()
    duplicate_groups: tuple[tuple[str, tuple[str, ...]], ...] = ()
    relations: tuple[tuple[str, RelationType], ...] = ()
    current_record_ids: tuple[str, ...] = ()
    stale_record_ids: tuple[str, ...] = ()
    unverified_record_ids: tuple[str, ...] = ()
    unique_underlying_evidence_count: int = 0
    reused_underlying_evidence_count: int = 0
    scientific_conclusion: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    governance_effect: str = "NONE"
    deployment: bool = False

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["status"] = self.status.value
        payload["disposition"] = self.disposition.value
        payload["relations"] = [(record_id, relation.value) for record_id, relation in self.relations]
        return payload


def _decision(
    ledger: EvidenceLedger,
    status: LedgerStatus,
    disposition: Disposition,
    reason: str,
    *,
    missing: tuple[str, ...] = (),
    contradictions: tuple[str, ...] = (),
    duplicate_groups: tuple[tuple[str, tuple[str, ...]], ...] = (),
    relations: tuple[tuple[str, RelationType], ...] = (),
    current_ids: tuple[str, ...] = (),
    stale_ids: tuple[str, ...] = (),
    unverified_ids: tuple[str, ...] = (),
    unique_count: int = 0,
    reused_count: int = 0,
) -> LedgerDecision:
    return LedgerDecision(
        status=status,
        disposition=disposition,
        reason=reason,
        ledger_id=ledger.ledger_id,
        missing_fields=missing,
        contradiction_fields=contradictions,
        duplicate_groups=duplicate_groups,
        relations=relations,
        current_record_ids=current_ids,
        stale_record_ids=stale_ids,
        unverified_record_ids=unverified_ids,
        unique_underlying_evidence_count=unique_count,
        reused_underlying_evidence_count=reused_count,
        canonical_effect="NONE",
        governance_effect="NONE",
        deployment=False,
    )


def _parse_time(value: str | None) -> datetime | None:
    if value is None:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def audit_evidence_ledger(ledger: EvidenceLedger) -> LedgerDecision:
    """Audit evidence identity/currentness metadata only; never determines truth."""
    if not ledger.ledger_id:
        return _decision(ledger, LedgerStatus.INVALID, Disposition.HOLD, "MISSING_LEDGER_ID")
    if ledger.canonical_effect != "NONE" or ledger.governance_effect != "NONE" or ledger.deployment:
        return _decision(ledger, LedgerStatus.INVALID, Disposition.HOLD, "BOUNDARY_EFFECT_REQUESTED")
    if ledger.evaluation_time is None or _parse_time(ledger.evaluation_time) is None:
        return _decision(ledger, LedgerStatus.INDETERMINATE, Disposition.HOLD, "EVALUATION_TIME_INVALID", missing=("evaluation_time",))

    record_ids = [record.record_id for record in ledger.records]
    if any(not record_id for record_id in record_ids):
        return _decision(ledger, LedgerStatus.INDETERMINATE, Disposition.HOLD, "RECORD_ID_MISSING", missing=("record_id",))
    if len(record_ids) != len(set(record_ids)):
        return _decision(ledger, LedgerStatus.INVALID, Disposition.HOLD, "RECORD_ID_COLLISION", contradictions=("record_id",))

    missing: list[str] = []
    current_ids: list[str] = []
    stale_ids: list[str] = []
    unverified_ids: list[str] = []
    for record in ledger.records:
        required = {
            f"{record.record_id}.stable_source_id": record.stable_source_id,
            f"{record.record_id}.underlying_evidence_id": record.underlying_evidence_id,
            f"{record.record_id}.source_locator": record.source_locator,
            f"{record.record_id}.authority_kind": record.authority_kind,
            f"{record.record_id}.transformation_ref": record.transformation_ref,
            f"{record.record_id}.claim_scope": record.claim_scope,
        }
        missing.extend(key for key, value in required.items() if value is None or value == "")
        if record.currentness_status in {CurrentnessStatus.CURRENT, CurrentnessStatus.STALE, CurrentnessStatus.HISTORICAL, CurrentnessStatus.RETRIEVED_UNVERIFIED}:
            if record.retrieved_at is None or _parse_time(record.retrieved_at) is None:
                missing.append(f"{record.record_id}.retrieved_at")
        if record.currentness_status in {CurrentnessStatus.CURRENT, CurrentnessStatus.STALE, CurrentnessStatus.HISTORICAL} and not record.currentness_basis_ref:
            missing.append(f"{record.record_id}.currentness_basis_ref")
        if record.currentness_status is CurrentnessStatus.CURRENT and not record.source_version_ref:
            missing.append(f"{record.record_id}.source_version_ref")
        if record.currentness_status is CurrentnessStatus.REMEMBERED_UNVERIFIED and record.retrieved_at is not None:
            return _decision(ledger, LedgerStatus.INVALID, Disposition.HOLD, "REMEMBERED_STATUS_CONTRADICTS_RETRIEVAL", contradictions=(record.record_id, "retrieved_at"))
        if record.currentness_status is CurrentnessStatus.CURRENT:
            current_ids.append(record.record_id)
        elif record.currentness_status in {CurrentnessStatus.STALE, CurrentnessStatus.HISTORICAL}:
            stale_ids.append(record.record_id)
        else:
            unverified_ids.append(record.record_id)
        published = _parse_time(record.source_published_at)
        retrieved = _parse_time(record.retrieved_at)
        if published is not None and retrieved is not None and published > retrieved:
            return _decision(ledger, LedgerStatus.INVALID, Disposition.HOLD, "SOURCE_PUBLISHED_AFTER_RETRIEVAL", contradictions=(record.record_id, "source_published_at", "retrieved_at"))
        if record.currentness_status is CurrentnessStatus.REMEMBERED_UNVERIFIED:
            return _decision(ledger, LedgerStatus.INDETERMINATE, Disposition.HOLD, "REMEMBERED_SOURCE_NOT_ADMISSIBLE", contradictions=(record.record_id, "currentness_status"))
        if record.currentness_status is CurrentnessStatus.UNKNOWN:
            return _decision(ledger, LedgerStatus.INDETERMINATE, Disposition.HOLD, "CURRENTNESS_UNKNOWN", contradictions=(record.record_id, "currentness_status"))
        if record.derived_from_record_id == record.record_id:
            return _decision(ledger, LedgerStatus.INVALID, Disposition.HOLD, "SELF_DERIVATION", contradictions=(record.record_id, "derived_from_record_id"))
        if record.derived_from_record_id is not None and record.derived_from_record_id not in record_ids:
            return _decision(ledger, LedgerStatus.INDETERMINATE, Disposition.HOLD, "DERIVATION_PARENT_MISSING", missing=(f"{record.record_id}.derived_from_record_id",))
    if missing:
        return _decision(ledger, LedgerStatus.INDETERMINATE, Disposition.HOLD, "EVIDENCE_RECORD_INCOMPLETE", missing=tuple(missing))

    by_underlying: dict[str, list[EvidenceRecord]] = {}
    by_locator: dict[str, list[EvidenceRecord]] = {}
    for record in ledger.records:
        assert record.underlying_evidence_id is not None
        assert record.source_locator is not None
        by_underlying.setdefault(record.underlying_evidence_id, []).append(record)
        by_locator.setdefault(record.source_locator, []).append(record)

    contradictions: list[str] = []
    duplicate_groups: list[tuple[str, tuple[str, ...]]] = []
    for underlying_id, records in by_underlying.items():
        if len(records) > 1:
            duplicate_groups.append((underlying_id, tuple(record.record_id for record in records)))
        digests = {record.content_digest for record in records if record.content_digest is not None}
        if len(digests) > 1:
            contradictions.extend((underlying_id, "content_digest"))
    if contradictions:
        return _decision(ledger, LedgerStatus.INVALID, Disposition.HOLD, "UNDERLYING_EVIDENCE_DIGEST_CONTRADICTION", contradictions=tuple(contradictions), duplicate_groups=tuple(duplicate_groups))

    for locator, records in by_locator.items():
        underlying_ids = {record.underlying_evidence_id for record in records}
        if len(underlying_ids) > 1 and not all(record.derived_from_record_id is not None for record in records):
            return _decision(ledger, LedgerStatus.INDETERMINATE, Disposition.HOLD, "SAME_LOCATOR_RELATION_UNKNOWN", contradictions=(locator, "underlying_evidence_id"), duplicate_groups=tuple(duplicate_groups))

    if ledger.claimed_replication_record_ids:
        for record_id in ledger.claimed_replication_record_ids:
            matching = [record for record in ledger.records if record.record_id == record_id]
            if not matching:
                return _decision(ledger, LedgerStatus.INDETERMINATE, Disposition.HOLD, "CLAIMED_REPLICATION_RECORD_MISSING", missing=(record_id,))
            underlying_id = matching[0].underlying_evidence_id
            if underlying_id is not None and len(by_underlying.get(underlying_id, [])) > 1:
                return _decision(ledger, LedgerStatus.INVALID, Disposition.HOLD, "DUPLICATION_MISLABELED_AS_REPLICATION", contradictions=(record_id, underlying_id), duplicate_groups=tuple(duplicate_groups))

    unique_ids = tuple(sorted(by_underlying))
    claimed_new = set(ledger.claimed_new_evidence_ids)
    if claimed_new and claimed_new != set(unique_ids):
        return _decision(ledger, LedgerStatus.INVALID, Disposition.HOLD, "NEW_EVIDENCE_COUNT_CLAIM_MISMATCH", contradictions=("claimed_new_evidence_ids",))

    relations: list[tuple[str, RelationType]] = []
    for record in ledger.records:
        if record.derived_from_record_id is not None:
            relations.append((record.record_id, RelationType.DERIVED_RECORD))
        elif record.underlying_evidence_id is not None and len(by_underlying[record.underlying_evidence_id]) > 1:
            relations.append((record.record_id, RelationType.SAME_UNDERLYING_EVIDENCE))
        else:
            relations.append((record.record_id, RelationType.UNIQUE_UNDERLYING_EVIDENCE))

    return _decision(
        ledger,
        LedgerStatus.COMPLETE,
        Disposition.ADMISSIBLE_FOR_REVIEW,
        "EVIDENCE_LEDGER_ADMISSIBLE_WITH_REUSE_DISTINCTION",
        duplicate_groups=tuple(duplicate_groups),
        relations=tuple(relations),
        current_ids=tuple(current_ids),
        stale_ids=tuple(stale_ids),
        unverified_ids=tuple(unverified_ids),
        unique_count=len(unique_ids),
        reused_count=sum(1 for records in by_underlying.values() if len(records) > 1),
    )
