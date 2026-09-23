"""Archive-to-active embodiment convergence contract."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
import hashlib
import json
from pathlib import Path
from typing import Any


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


ARCHIVE_HEADS: dict[int, str] = {
    190: "066ed1afccebee869eb658c09691b7f096694332",
    191: "48bcf45a55a0b67dfc0e7b9cd838c5f9068b08d2",
    192: "861e6a556a21afffd04b187714c0608fe73ea4fc",
}

_LEDGER_KEYS = {
    "ledger_id",
    "entries",
    "scientific_disposition",
    "canonical_effect",
    "deployment",
}

_ENTRY_KEYS = {
    "source_pr",
    "source_head",
    "source_path_or_semantic_unit",
    "classification",
    "target_owner",
    "adoption_status",
    "reason",
    "replacement_ref_if_superseded",
    "claim_ceiling",
    "review_status",
}


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


def _require_mapping(value: object, *, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    if not all(isinstance(key, str) for key in value):
        raise ValueError(f"{label} keys must be strings")
    return value


def _require_exact_keys(
    value: dict[str, Any],
    required: set[str],
    *,
    label: str,
) -> None:
    actual = set(value)
    if actual != required:
        missing = sorted(required - actual)
        extra = sorted(actual - required)
        raise ValueError(
            f"{label} key drift: missing={missing}, extra={extra}"
        )


def _require_nonempty_str(value: object, *, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value


def _require_int(value: object, *, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{label} must be an integer")
    return value


def _require_bool(value: object, *, label: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{label} must be a boolean")
    return value


def _require_nullable_str(value: object, *, label: str) -> str | None:
    if value is None:
        return None
    return _require_nonempty_str(value, label=label)


def _entry_from_json(value: object) -> ArchiveDisposition:
    item = _require_mapping(value, label="archive disposition")
    _require_exact_keys(item, _ENTRY_KEYS, label="archive disposition")

    try:
        classification = ConvergenceClassification(
            _require_nonempty_str(
                item["classification"],
                label="classification",
            )
        )
    except ValueError as exc:
        raise ValueError("unknown convergence classification") from exc

    try:
        adoption_status = AdoptionStatus(
            _require_nonempty_str(
                item["adoption_status"],
                label="adoption_status",
            )
        )
    except ValueError as exc:
        raise ValueError("unknown adoption status") from exc

    return ArchiveDisposition(
        source_pr=_require_int(item["source_pr"], label="source_pr"),
        source_head=_require_nonempty_str(
            item["source_head"],
            label="source_head",
        ),
        source_path_or_semantic_unit=_require_nonempty_str(
            item["source_path_or_semantic_unit"],
            label="source_path_or_semantic_unit",
        ),
        classification=classification,
        target_owner=_require_nonempty_str(
            item["target_owner"],
            label="target_owner",
        ),
        adoption_status=adoption_status,
        reason=_require_nonempty_str(item["reason"], label="reason"),
        replacement_ref_if_superseded=_require_nullable_str(
            item["replacement_ref_if_superseded"],
            label="replacement_ref_if_superseded",
        ),
        claim_ceiling=_require_nonempty_str(
            item["claim_ceiling"],
            label="claim_ceiling",
        ),
        review_status=_require_nonempty_str(
            item["review_status"],
            label="review_status",
        ),
    )


def load_convergence_ledger(path: str | Path) -> ConvergenceLedger:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    payload = _require_mapping(raw, label="convergence ledger")
    _require_exact_keys(payload, _LEDGER_KEYS, label="convergence ledger")

    raw_entries = payload["entries"]
    if not isinstance(raw_entries, list):
        raise ValueError("entries must be an array")

    ledger = ConvergenceLedger(
        ledger_id=_require_nonempty_str(
            payload["ledger_id"],
            label="ledger_id",
        ),
        entries=tuple(_entry_from_json(item) for item in raw_entries),
        scientific_disposition=_require_nonempty_str(
            payload["scientific_disposition"],
            label="scientific_disposition",
        ),
        canonical_effect=_require_nonempty_str(
            payload["canonical_effect"],
            label="canonical_effect",
        ),
        deployment=_require_bool(
            payload["deployment"],
            label="deployment",
        ),
    )
    validate_convergence_ledger(ledger)
    return ledger


def _canonical_payload(ledger: ConvergenceLedger) -> dict[str, Any]:
    return {
        "ledger_id": ledger.ledger_id,
        "entries": [asdict(entry) for entry in ledger.entries],
        "scientific_disposition": ledger.scientific_disposition,
        "canonical_effect": ledger.canonical_effect,
        "deployment": ledger.deployment,
    }


def convergence_ledger_hash(ledger: ConvergenceLedger) -> str:
    validate_convergence_ledger(ledger)
    encoded = json.dumps(
        _canonical_payload(ledger),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_convergence_ledger(ledger: ConvergenceLedger) -> dict[str, str]:
    if not ledger.ledger_id.strip():
        raise ValueError("ledger id must be nonempty")
    if ledger.scientific_disposition != "HOLD":
        raise ValueError("scientific disposition must remain HOLD")
    if ledger.canonical_effect != "NONE":
        raise ValueError("canonical effect must remain NONE")
    if ledger.deployment is not False:
        raise ValueError("deployment must remain false")
    if not ledger.entries:
        raise ValueError("convergence ledger must contain entries")

    seen: set[tuple[int, str]] = set()
    classifications: set[ConvergenceClassification] = set()
    adoption_statuses: set[AdoptionStatus] = set()

    for entry in ledger.entries:
        if type(entry.source_pr) is not int or entry.source_pr not in ARCHIVE_HEADS:
            raise ValueError("source PR must be one of the frozen archive PRs")
        if entry.source_head != ARCHIVE_HEADS[entry.source_pr]:
            raise ValueError("source head must match exact archive head")
        if not isinstance(entry.classification, ConvergenceClassification):
            raise ValueError("classification must use ConvergenceClassification")
        if not isinstance(entry.adoption_status, AdoptionStatus):
            raise ValueError("adoption status must use AdoptionStatus")

        semantic_unit = entry.source_path_or_semantic_unit.strip()
        if not semantic_unit:
            raise ValueError("source semantic unit must be nonempty")
        key = (entry.source_pr, semantic_unit)
        if key in seen:
            raise ValueError("duplicate archive semantic unit")
        seen.add(key)

        if not entry.target_owner.strip():
            raise ValueError("target owner must be nonempty")
        if not entry.reason.strip():
            raise ValueError("reason must be nonempty")
        if entry.claim_ceiling != "NOT_ESTABLISHED":
            raise ValueError("claim ceiling must remain NOT_ESTABLISHED")
        if not entry.review_status.strip():
            raise ValueError("review status must be nonempty")

        if entry.classification is ConvergenceClassification.SUPERSEDED:
            if entry.adoption_status is not AdoptionStatus.REPLACED:
                raise ValueError("SUPERSEDED entries must use REPLACED status")
            if not (entry.replacement_ref_if_superseded or "").strip():
                raise ValueError(
                    "SUPERSEDED entries require a replacement reference"
                )
        elif entry.replacement_ref_if_superseded is not None:
            raise ValueError(
                "replacement reference is only valid for SUPERSEDED entries"
            )

        if (
            entry.classification is ConvergenceClassification.ARCHIVE_ONLY
            and entry.adoption_status is not AdoptionStatus.HISTORICAL_ONLY
        ):
            raise ValueError(
                "ARCHIVE_ONLY entries must use HISTORICAL_ONLY status"
            )

        if entry.classification is ConvergenceClassification.SHARED_CORE:
            if entry.adoption_status is not AdoptionStatus.ADOPTED:
                raise ValueError("SHARED_CORE entries must use ADOPTED status")
            if not entry.target_owner.startswith("shared_core:"):
                raise ValueError(
                    "SHARED_CORE target owner must begin shared_core:"
                )

        if (
            entry.classification
            is ConvergenceClassification.ROLE_SPECIFIC_EXTENSION
        ):
            if entry.adoption_status is not AdoptionStatus.DEFERRED:
                raise ValueError(
                    "ROLE_SPECIFIC_EXTENSION entries must use DEFERRED status"
                )
            if not entry.target_owner.startswith("role_extension:"):
                raise ValueError(
                    "ROLE_SPECIFIC_EXTENSION target owner must begin "
                    "role_extension:"
                )

        classifications.add(entry.classification)
        adoption_statuses.add(entry.adoption_status)

    if classifications != set(ConvergenceClassification):
        raise ValueError(
            "classification partition must cover all classifications"
        )
    if adoption_statuses != set(AdoptionStatus):
        raise ValueError(
            "classification partition must cover all adoption statuses"
        )

    return {
        "result": "PASS",
        "source_heads": "PASS",
        "classification_partition": "PASS",
        "boundary_lock": "PASS",
    }
