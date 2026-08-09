from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


def _require_aware(value: datetime, field_name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")


def _utc_max() -> datetime:
    return datetime.max.replace(tzinfo=timezone.utc)


@dataclass(frozen=True, slots=True)
class TemporalVersion:
    stream_id: str
    version_id: str
    subject_id: str
    namespace: str
    payload_ref: str
    recorded_at: datetime
    valid_from: datetime
    observed_at: datetime | None = None
    event_time: datetime | None = None
    valid_to: datetime | None = None
    revision_of: str | None = None
    source_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for field_name in ("stream_id", "version_id", "subject_id", "namespace", "payload_ref"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} must be non-empty")
        _require_aware(self.recorded_at, "recorded_at")
        _require_aware(self.valid_from, "valid_from")
        for name in ("observed_at", "event_time", "valid_to"):
            value = getattr(self, name)
            if value is not None:
                _require_aware(value, name)
        if self.valid_to is not None and self.valid_to <= self.valid_from:
            raise ValueError("valid_to must be after valid_from")

    def is_valid_at(self, at: datetime) -> bool:
        _require_aware(at, "at")
        return self.valid_from <= at and (self.valid_to is None or at < self.valid_to)


@dataclass(frozen=True, slots=True)
class RetrospectiveAnnotation:
    annotation_id: str
    stream_id: str
    target_version_id: str
    interpretation_ref: str
    recorded_at: datetime
    source_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        for field_name in ("annotation_id", "stream_id", "target_version_id", "interpretation_ref"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} must be non-empty")
        _require_aware(self.recorded_at, "recorded_at")
        if not self.source_refs:
            raise ValueError("retrospective annotation requires source_refs")


@dataclass(frozen=True, slots=True)
class TemporalProjection:
    stream_id: str
    historical_at: datetime
    as_was: TemporalVersion | None
    current_as_of: TemporalVersion | None
    retrospective_annotations: tuple[RetrospectiveAnnotation, ...]
    transition_lineage: tuple[tuple[str, str], ...]


class TemporalVersionResolver:
    """Append-only research resolver that separates historical knowledge from later interpretation."""

    def __init__(self) -> None:
        self._versions: dict[str, TemporalVersion] = {}
        self._streams: dict[str, list[str]] = {}
        self._annotations: dict[str, RetrospectiveAnnotation] = {}

    def add_version(self, version: TemporalVersion) -> None:
        if version.version_id in self._versions:
            raise ValueError(f"duplicate version_id: {version.version_id}")
        existing_ids = self._streams.get(version.stream_id, [])
        if existing_ids:
            first = self._versions[existing_ids[0]]
            if (first.subject_id, first.namespace) != (version.subject_id, version.namespace):
                raise ValueError("stream subject_id/namespace binding is immutable")
        if version.revision_of is not None:
            parent = self._versions.get(version.revision_of)
            if parent is None:
                raise ValueError("revision_of must reference an existing version")
            if parent.stream_id != version.stream_id:
                raise ValueError("revision_of cannot cross streams")
            if parent.recorded_at > version.recorded_at:
                raise ValueError("a revision cannot be recorded before its parent")
        self._versions[version.version_id] = version
        self._streams.setdefault(version.stream_id, []).append(version.version_id)

    def add_retrospective_annotation(self, annotation: RetrospectiveAnnotation) -> None:
        if annotation.annotation_id in self._annotations:
            raise ValueError(f"duplicate annotation_id: {annotation.annotation_id}")
        target = self._versions.get(annotation.target_version_id)
        if target is None or target.stream_id != annotation.stream_id:
            raise ValueError("annotation target must exist in the same stream")
        if annotation.recorded_at < target.recorded_at:
            raise ValueError("retrospective annotation cannot predate the target record")
        self._annotations[annotation.annotation_id] = annotation

    def as_was(self, stream_id: str, at: datetime) -> TemporalVersion | None:
        _require_aware(at, "at")
        candidates = [version for version in self._stream_versions(stream_id) if version.recorded_at <= at and version.is_valid_at(at)]
        if not candidates:
            return None
        return max(candidates, key=lambda item: (item.valid_from, item.recorded_at, item.version_id))

    def current(self, stream_id: str, *, as_of: datetime | None = None) -> TemporalVersion | None:
        cutoff = as_of or _utc_max()
        _require_aware(cutoff, "as_of")
        candidates = [version for version in self._stream_versions(stream_id) if version.recorded_at <= cutoff]
        if not candidates:
            return None
        effective_at = cutoff if as_of is not None else max(item.valid_from for item in candidates)
        valid = [item for item in candidates if item.is_valid_at(effective_at)]
        pool = valid or candidates
        return max(pool, key=lambda item: (item.valid_from, item.recorded_at, item.version_id))

    def project(self, stream_id: str, *, historical_at: datetime, as_of: datetime) -> TemporalProjection:
        _require_aware(historical_at, "historical_at")
        _require_aware(as_of, "as_of")
        if as_of < historical_at:
            raise ValueError("as_of cannot predate historical_at")
        annotations = tuple(sorted((item for item in self._annotations.values() if item.stream_id == stream_id and item.recorded_at <= as_of), key=lambda item: (item.recorded_at, item.annotation_id)))
        return TemporalProjection(
            stream_id=stream_id,
            historical_at=historical_at,
            as_was=self.as_was(stream_id, historical_at),
            current_as_of=self.current(stream_id, as_of=as_of),
            retrospective_annotations=annotations,
            transition_lineage=self.transition_lineage(stream_id),
        )

    def transition_lineage(self, stream_id: str) -> tuple[tuple[str, str], ...]:
        edges = [(version.revision_of, version.version_id) for version in self._stream_versions(stream_id) if version.revision_of is not None]
        return tuple(sorted(edges))

    def versions(self, stream_id: str) -> tuple[TemporalVersion, ...]:
        return tuple(sorted(self._stream_versions(stream_id), key=lambda item: (item.recorded_at, item.valid_from, item.version_id)))

    def _stream_versions(self, stream_id: str) -> list[TemporalVersion]:
        return [self._versions[item_id] for item_id in self._streams.get(stream_id, [])]
