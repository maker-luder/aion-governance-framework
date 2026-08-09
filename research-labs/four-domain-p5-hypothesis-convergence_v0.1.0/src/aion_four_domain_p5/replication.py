from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


def _require_aware(value: datetime, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")


class RegistryDecision(str, Enum):
    EMPTY = "EMPTY"
    SINGLE_RUN = "SINGLE_RUN"
    CONSISTENT = "CONSISTENT"
    DIVERGENT = "DIVERGENT"
    CONTAMINATED_ONLY = "CONTAMINATED_ONLY"


@dataclass(frozen=True, slots=True)
class ReplicationEntry:
    registry_id: str
    hypothesis_id: str
    experiment_id: str
    manifest_fingerprint: str
    output_hash: str
    runner_id: str
    actor_kind: str
    result_status: str
    contamination_class: str
    recorded_at: datetime
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in (
            "registry_id", "hypothesis_id", "experiment_id", "manifest_fingerprint",
            "output_hash", "runner_id", "actor_kind", "result_status", "contamination_class",
        ):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        _require_aware(self.recorded_at, "recorded_at")
        if not self.evidence_refs:
            raise ValueError("replication entries require evidence_refs")


@dataclass(frozen=True, slots=True)
class ReplicationSummary:
    hypothesis_id: str
    decision: RegistryDecision
    run_count: int
    runner_count: int
    clean_run_count: int
    output_variant_count: int
    status_counts: tuple[tuple[str, int], ...]
    contamination_counts: tuple[tuple[str, int], ...]


class ReplicationRegistry:
    """Append-only registry for public-safe replication/reproduction evidence."""

    def __init__(self) -> None:
        self._entries: dict[str, ReplicationEntry] = {}
        self._by_hypothesis: dict[str, list[str]] = {}

    def append(self, entry: ReplicationEntry) -> None:
        if entry.registry_id in self._entries:
            raise ValueError(f"duplicate registry_id: {entry.registry_id}")
        self._entries[entry.registry_id] = entry
        self._by_hypothesis.setdefault(entry.hypothesis_id, []).append(entry.registry_id)

    def append_p4(self, *, registry_id: str, hypothesis_id: str, manifest: object,
                  result: object, recorded_at: datetime, evidence_refs: tuple[str, ...]) -> ReplicationEntry:
        """Bind a P4-like manifest/result pair without duplicating P4 implementation."""
        fingerprint = manifest.fingerprint()
        if manifest.experiment_id != result.experiment_id:
            raise ValueError("experiment_id mismatch")
        if fingerprint != result.manifest_fingerprint:
            raise ValueError("result is not bound to manifest")
        entry = ReplicationEntry(
            registry_id=registry_id,
            hypothesis_id=hypothesis_id,
            experiment_id=manifest.experiment_id,
            manifest_fingerprint=fingerprint,
            output_hash=result.output_hash,
            runner_id=manifest.runner_id,
            actor_kind=manifest.actor_kind.value,
            result_status=result.status.value,
            contamination_class=result.contamination_class.value,
            recorded_at=recorded_at,
            evidence_refs=evidence_refs,
        )
        self.append(entry)
        return entry

    def entries(self, hypothesis_id: str) -> tuple[ReplicationEntry, ...]:
        return tuple(
            sorted(
                (self._entries[item_id] for item_id in self._by_hypothesis.get(hypothesis_id, [])),
                key=lambda item: (item.recorded_at, item.registry_id),
            )
        )

    def summarize(self, hypothesis_id: str) -> ReplicationSummary:
        entries = self.entries(hypothesis_id)
        if not entries:
            return ReplicationSummary(hypothesis_id, RegistryDecision.EMPTY, 0, 0, 0, 0, (), ())

        clean = [item for item in entries if item.contamination_class == "NONE"]
        variants = {item.output_hash for item in clean}
        if not clean:
            decision = RegistryDecision.CONTAMINATED_ONLY
        elif len(clean) == 1:
            decision = RegistryDecision.SINGLE_RUN
        elif len(variants) == 1:
            decision = RegistryDecision.CONSISTENT
        else:
            decision = RegistryDecision.DIVERGENT

        status_counts: dict[str, int] = {}
        contamination_counts: dict[str, int] = {}
        for item in entries:
            status_counts[item.result_status] = status_counts.get(item.result_status, 0) + 1
            contamination_counts[item.contamination_class] = contamination_counts.get(item.contamination_class, 0) + 1

        return ReplicationSummary(
            hypothesis_id=hypothesis_id,
            decision=decision,
            run_count=len(entries),
            runner_count=len({item.runner_id for item in entries}),
            clean_run_count=len(clean),
            output_variant_count=len(variants),
            status_counts=tuple(sorted(status_counts.items())),
            contamination_counts=tuple(sorted(contamination_counts.items())),
        )
