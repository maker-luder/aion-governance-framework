from datetime import datetime, timezone

import pytest

from aion_four_domain_p1 import RetrospectiveAnnotation, TemporalVersion, TemporalVersionResolver

UTC = timezone.utc


def dt(day: int, hour: int = 0) -> datetime:
    return datetime(2026, 8, day, hour, tzinfo=UTC)


def test_as_was_prevents_later_back_projection() -> None:
    resolver = TemporalVersionResolver()
    resolver.add_version(
        TemporalVersion(
            stream_id="memory-1",
            version_id="v1",
            subject_id="subject-a",
            namespace="AION",
            payload_ref="sha256:v1",
            recorded_at=dt(1),
            valid_from=dt(1),
            source_refs=("source:1",),
        )
    )
    resolver.add_version(
        TemporalVersion(
            stream_id="memory-1",
            version_id="v2",
            subject_id="subject-a",
            namespace="AION",
            payload_ref="sha256:v2",
            recorded_at=dt(3),
            valid_from=dt(1),
            revision_of="v1",
            source_refs=("source:2",),
        )
    )

    assert resolver.as_was("memory-1", dt(2)).version_id == "v1"
    assert resolver.current("memory-1", as_of=dt(4)).version_id == "v2"


def test_projection_keeps_as_was_separate_from_retrospective_interpretation() -> None:
    resolver = TemporalVersionResolver()
    resolver.add_version(
        TemporalVersion(
            stream_id="s",
            version_id="v1",
            subject_id="subject-a",
            namespace="AION",
            payload_ref="payload:v1",
            recorded_at=dt(1),
            valid_from=dt(1),
            source_refs=("source:1",),
        )
    )
    resolver.add_retrospective_annotation(
        RetrospectiveAnnotation(
            annotation_id="a1",
            stream_id="s",
            target_version_id="v1",
            interpretation_ref="analysis:later",
            recorded_at=dt(3),
            source_refs=("review:1",),
        )
    )

    projection = resolver.project("s", historical_at=dt(2), as_of=dt(4))
    assert projection.as_was.version_id == "v1"
    assert projection.retrospective_annotations[0].interpretation_ref == "analysis:later"


def test_stream_binding_is_immutable() -> None:
    resolver = TemporalVersionResolver()
    resolver.add_version(
        TemporalVersion("s", "v1", "subject-a", "AION", "p1", dt(1), dt(1), source_refs=("src",))
    )
    with pytest.raises(ValueError, match="binding is immutable"):
        resolver.add_version(
            TemporalVersion("s", "v2", "subject-b", "AION", "p2", dt(2), dt(2), source_refs=("src",))
        )


def test_naive_datetime_fails_closed() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        TemporalVersion(
            stream_id="s",
            version_id="v1",
            subject_id="subject-a",
            namespace="AION",
            payload_ref="p",
            recorded_at=datetime(2026, 8, 1),
            valid_from=dt(1),
        )
