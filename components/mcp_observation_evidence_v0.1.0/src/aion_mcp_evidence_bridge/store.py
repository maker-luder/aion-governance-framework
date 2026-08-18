from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from types import MappingProxyType
from typing import Any


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({str(key): _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value


class EvidenceStore:
    """Immutable, fixture-backed Phase 1 evidence store.

    The store deliberately accepts only a fixture file supplied at construction.
    It has no write, append, update, promotion, runtime, memory, or identity API.
    Query methods return fresh defensive copies.
    """

    __slots__ = ("_observations", "_provenance_records", "_attributions", "_boundary", "_nonclaims")

    def __init__(self, payload: Mapping[str, Any]) -> None:
        self._observations = tuple(_freeze(item) for item in payload.get("observations", []))
        self._provenance_records = tuple(_freeze(item) for item in payload.get("provenance_records", []))
        self._attributions = tuple(_freeze(item) for item in payload.get("attributions", []))
        self._boundary = _freeze(payload.get("research_boundary", {}))
        self._nonclaims = _freeze(payload.get("current_nonclaims", {}))

    @classmethod
    def from_json(cls, path: Path) -> "EvidenceStore":
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if not isinstance(payload, dict):
            raise ValueError("evidence fixture root must be an object")
        return cls(payload)

    def list_continuity_observations(self) -> list[dict[str, Any]]:
        return [_thaw(item) for item in self._observations]

    def get_continuity_observation(self, observation_id: str) -> dict[str, Any] | None:
        for item in self._observations:
            if item.get("observation_id") == observation_id:
                return _thaw(item)
        return None

    def search_provenance_records(self, query: str) -> list[dict[str, Any]]:
        needle = query.strip().casefold()
        if not needle:
            return []
        results: list[dict[str, Any]] = []
        for item in self._provenance_records:
            haystack = " ".join(str(item.get(key, "")) for key in ("record_id", "source_id", "label", "attribution"))
            if needle in haystack.casefold():
                results.append(_thaw(item))
        return results

    def get_source_attribution(self, record_id: str) -> dict[str, Any] | None:
        for item in self._attributions:
            if item.get("record_id") == record_id:
                return _thaw(item)
        return None

    def get_research_boundary(self) -> dict[str, Any]:
        return _thaw(self._boundary)

    def get_current_nonclaims(self) -> dict[str, Any]:
        return _thaw(self._nonclaims)


_REQUIRED_ADMISSION_FIELDS = (
    "existing_question",
    "provenance",
    "source_scope",
    "evidence_role",
)


def validate_external_source_admission(candidate: Mapping[str, Any]) -> dict[str, Any]:
    """Validate admission metadata without ingesting, storing, or fetching a source."""

    missing = [field for field in _REQUIRED_ADMISSION_FIELDS if not str(candidate.get(field, "")).strip()]
    bulk_ingest = bool(candidate.get("bulk_ingest", False))
    automatic_memory_generation = bool(candidate.get("automatic_memory_generation", False))
    automatic_canonical_promotion = bool(candidate.get("automatic_canonical_promotion", False))
    admitted = not missing and not bulk_ingest and not automatic_memory_generation and not automatic_canonical_promotion
    return {
        "admission": "ADMIT_CANDIDATE" if admitted else "HOLD_OR_DROP",
        "missing_fields": missing,
        "bulk_ingest": bulk_ingest,
        "automatic_memory_generation": automatic_memory_generation,
        "automatic_canonical_promotion": automatic_canonical_promotion,
        "canonical_effect": "NONE",
        "subjectivity_evidence_weight": 0,
        "ingested": False,
    }
