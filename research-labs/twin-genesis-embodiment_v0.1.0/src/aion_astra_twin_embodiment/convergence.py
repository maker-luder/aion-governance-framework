"""Archive-to-active embodiment convergence contract."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class ConvergenceClassification(StrEnum):
    SHARED_CORE = "SHARED_CORE"
    ROLE_SPECIFIC_EXTENSION = "ROLE_SPECIFIC_EXTENSION"
    ARCHIVE_ONLY = "ARCHIVE_ONLY"
    SUPERSEDED = "SUPERSEDED"


class AdoptionStatus(StrEnum):
    ADOPTED = "ADOPTED"
    DEFERRED = "DEFERRED"
    HISTORICAL_ONLY = "HISTORICAL_ONLY"
    REPLACED = "REPLACED"


@dataclass(frozen=True, slots=True)
class ArchiveDisposition:
    source_pr: int
    source_head: str
    source_path_or_semantic_unit: str
    classification: ConvergenceClassification
    target_owner: str
    adoption_status: AdoptionStatus
    reason: str
    replacement_ref_if_superseded: str | None
    claim_ceiling: str
    review_status: str


@dataclass(frozen=True, slots=True)
class ConvergenceLedger:
    ledger_id: str
    entries: tuple[ArchiveDisposition, ...]
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    deployment: bool = False


def load_convergence_ledger(path: str | Path) -> ConvergenceLedger:
    raise NotImplementedError("ledger loading is defined by the next TDD cycle")


def convergence_ledger_hash(ledger: ConvergenceLedger) -> str:
    raise NotImplementedError("ledger hashing is defined by the next TDD cycle")


def validate_convergence_ledger(ledger: ConvergenceLedger) -> dict[str, str]:
    raise NotImplementedError("ledger validation is defined by the next TDD cycle")
