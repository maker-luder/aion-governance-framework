from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import re

_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _require_aware(value: datetime, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")


class ObservationSourceClass(str, Enum):
    ACADEMIC_RESEARCH = "ACADEMIC_RESEARCH"
    PUBLIC_EVENT = "PUBLIC_EVENT"
    PUBLIC_DOCUMENTATION = "PUBLIC_DOCUMENTATION"
    DAILY_LIFE_GENERALIZATION = "DAILY_LIFE_GENERALIZATION"
    ENGINEERING_EXPERIMENT = "ENGINEERING_EXPERIMENT"


@dataclass(frozen=True, slots=True)
class PublicObservationRecord:
    observation_id: str
    source_class: ObservationSourceClass
    source_ref: str
    observed_at: datetime
    summary_ref: str
    evidence_hash: str
    public_safe: bool
    contains_personal_data: bool = False
    contains_private_conversation: bool = False
    transformation_refs: tuple[str, ...] = ()
    notes: str = ""

    def __post_init__(self) -> None:
        for name in ("observation_id", "source_ref", "summary_ref"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        _require_aware(self.observed_at, "observed_at")
        if not _SHA256.fullmatch(self.evidence_hash):
            raise ValueError("evidence_hash must be SHA-256")
        if not self.public_safe:
            raise ValueError("research branch only accepts public-safe observation records")
        if self.contains_personal_data or self.contains_private_conversation:
            raise ValueError("personal/private material cannot enter public observation intake")


class PublicObservationLedger:
    """Append-only public-safe observation intake.

    The ledger stores references and hashes, not copied private material.
    """

    def __init__(self) -> None:
        self._records: dict[str, PublicObservationRecord] = {}

    def append(self, record: PublicObservationRecord) -> None:
        if record.observation_id in self._records:
            raise ValueError(f"duplicate observation_id: {record.observation_id}")
        self._records[record.observation_id] = record

    def records(self) -> tuple[PublicObservationRecord, ...]:
        return tuple(sorted(self._records.values(), key=lambda item: (item.observed_at, item.observation_id)))
