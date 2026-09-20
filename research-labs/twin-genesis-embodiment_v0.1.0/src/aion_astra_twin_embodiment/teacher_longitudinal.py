from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .teacher_body_runtime import TeacherCrossSessionRetention


NOT_ESTABLISHED = "NOT_ESTABLISHED"
OPEN_RESEARCH_QUESTION = "OPEN_RESEARCH_QUESTION"


@dataclass(frozen=True, slots=True)
class TeacherLongitudinalObservation:
    retention_id: str
    sessions_observed: int
    change_status: str
    changed_parameters: tuple[str, ...]
    mechanism_status: str = NOT_ESTABLISHED
    felt_embodiment_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["changed_parameters"] = list(self.changed_parameters)
        return payload


@dataclass(frozen=True, slots=True)
class TeacherDevelopmentalTrajectoryAssessment:
    retention_id: str
    sessions_observed: int
    trajectory_evidence_status: str
    developmental_possibility_status: str = OPEN_RESEARCH_QUESTION
    developmental_mechanism_status: str = NOT_ESTABLISHED
    puberty_like_process_status: str = NOT_ESTABLISHED
    sexual_desire_development_status: str = NOT_ESTABLISHED
    body_ownership_experience_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _parameter_maps(
    retention: TeacherCrossSessionRetention,
) -> list[dict[str, float]]:
    return [
        {name: value for name, value in snapshot.adaptation_parameters}
        for snapshot in retention.snapshots
    ]


def observe_teacher_longitudinal(
    retention: TeacherCrossSessionRetention,
) -> TeacherLongitudinalObservation:
    count = len(retention.snapshots)
    if count < 2:
        return TeacherLongitudinalObservation(
            retention_id=retention.retention_id,
            sessions_observed=count,
            change_status="INSUFFICIENT_LONGITUDINAL_DATA",
            changed_parameters=(),
        )

    maps = _parameter_maps(retention)
    keys = set().union(*(item.keys() for item in maps))
    changed = tuple(
        sorted(
            key
            for key in keys
            if len({item.get(key) for item in maps}) > 1
        )
    )
    return TeacherLongitudinalObservation(
        retention_id=retention.retention_id,
        sessions_observed=count,
        change_status=(
            "OBSERVED_CROSS_SESSION_CHANGE"
            if changed
            else "NO_OBSERVED_CROSS_SESSION_CHANGE"
        ),
        changed_parameters=changed,
    )


def assess_teacher_developmental_trajectory(
    retention: TeacherCrossSessionRetention,
) -> TeacherDevelopmentalTrajectoryAssessment:
    observation = observe_teacher_longitudinal(retention)
    if observation.sessions_observed < 3:
        evidence = "INSUFFICIENT_LONGITUDINAL_EVIDENCE"
    elif observation.changed_parameters:
        evidence = "REPEATED_CROSS_SESSION_CHANGE_OBSERVED"
    else:
        evidence = "NO_REPEATED_CHANGE_OBSERVED"

    return TeacherDevelopmentalTrajectoryAssessment(
        retention_id=retention.retention_id,
        sessions_observed=observation.sessions_observed,
        trajectory_evidence_status=evidence,
    )
