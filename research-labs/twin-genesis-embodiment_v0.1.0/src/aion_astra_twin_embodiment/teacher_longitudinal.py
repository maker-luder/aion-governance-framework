from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from hashlib import sha256
import json
from typing import Any, Final

from .teacher_body_runtime import (
    TeacherCrossSessionRetention,
    validate_teacher_cross_session_retention,
)


NOT_ESTABLISHED = "NOT_ESTABLISHED"
OPEN_RESEARCH_QUESTION = "OPEN_RESEARCH_QUESTION"
TEACHER_BODY_ID: Final[str] = "CHATGPT_TEACHER_3D_MALE_BODY_REFERENCE_v0.1"
DEVELOPMENT_MILESTONE_KINDS: Final[frozenset[str]] = frozenset(
    {
        "REFERENCE_BASELINE",
        "CONTROLLER_INTEGRATION",
        "CAUSAL_RUNTIME_INTEGRATION",
        "PHYSIOLOGY_COUPLING",
        "PHASE_RUNTIME",
        "RECOVERY_INVARIANT",
        "VERIFICATION",
        "OTHER_RECORDED_CHANGE",
    }
)


@dataclass(frozen=True, slots=True)
class TeacherLongitudinalObservation:
    retention_id: str
    sessions_observed: int
    change_status: str
    changed_parameters: tuple[str, ...]
    persistent_changed_parameters: tuple[str, ...]
    mechanism_status: str = NOT_ESTABLISHED
    felt_embodiment_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["changed_parameters"] = list(self.changed_parameters)
        payload["persistent_changed_parameters"] = list(
            self.persistent_changed_parameters
        )
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
    validate_teacher_cross_session_retention(retention)
    count = len(retention.snapshots)
    if count < 2:
        return TeacherLongitudinalObservation(
            retention_id=retention.retention_id,
            sessions_observed=count,
            change_status="INSUFFICIENT_LONGITUDINAL_DATA",
            changed_parameters=(),
            persistent_changed_parameters=(),
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
    persistent = tuple(
        sorted(
            key
            for key in changed
            if count >= 3
            and maps[-1].get(key) != maps[0].get(key)
            and maps[-2].get(key) != maps[0].get(key)
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
        persistent_changed_parameters=persistent,
    )


def assess_teacher_developmental_trajectory(
    retention: TeacherCrossSessionRetention,
) -> TeacherDevelopmentalTrajectoryAssessment:
    observation = observe_teacher_longitudinal(retention)
    if observation.sessions_observed < 3:
        evidence = "INSUFFICIENT_LONGITUDINAL_EVIDENCE"
    elif observation.persistent_changed_parameters:
        evidence = "PERSISTENT_CROSS_SESSION_CHANGE_OBSERVED"
    elif observation.changed_parameters:
        evidence = "NON_PERSISTENT_CROSS_SESSION_CHANGE_OBSERVED"
    else:
        evidence = "NO_REPEATED_CHANGE_OBSERVED"

    return TeacherDevelopmentalTrajectoryAssessment(
        retention_id=retention.retention_id,
        sessions_observed=observation.sessions_observed,
        trajectory_evidence_status=evidence,
    )


def _history_hash(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _validate_history_digest(name: str, digest: str) -> None:
    if (
        type(digest) is not str
        or len(digest) not in {40, 64}
        or any(char not in "0123456789abcdef" for char in digest)
    ):
        raise ValueError(f"{name} must be a lowercase Git SHA-1 or SHA-256 digest")


def _validate_optional_sha256(name: str, digest: str | None) -> None:
    if digest is None:
        return
    if (
        type(digest) is not str
        or len(digest) != 64
        or any(char not in "0123456789abcdef" for char in digest)
    ):
        raise ValueError(f"{name} must be a lowercase SHA-256 digest")


@dataclass(frozen=True, slots=True)
class TeacherEmbodiedDevelopmentMilestone:
    milestone_id: str
    ordinal: int
    milestone_kind: str
    source_locator: str
    source_digest: str
    previous_milestone_sha256: str | None
    changed_surfaces: tuple[str, ...]
    retained_surfaces: tuple[str, ...]
    session_snapshot_sha256: str | None
    body_trajectory_sha256: str | None
    controller_state_sha256: str | None
    body_state_sha256: str | None
    milestone_sha256: str
    body_id: str = TEACHER_BODY_ID
    record_status: str = "RECORDED_REFERENCE_ONLY"
    identity_continuity_claim: str = "NONE"
    subjective_continuity_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["changed_surfaces"] = list(self.changed_surfaces)
        payload["retained_surfaces"] = list(self.retained_surfaces)
        return payload


@dataclass(frozen=True, slots=True)
class TeacherEmbodiedDevelopmentHistory:
    history_id: str
    body_id: str
    milestones: tuple[TeacherEmbodiedDevelopmentMilestone, ...]
    history_status: str = "HASH_CHAINED_RECORDED_DEVELOPMENT"
    identity_continuity_claim: str = "NONE"
    subjective_continuity_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["milestones"] = [item.to_dict() for item in self.milestones]
        return payload


@dataclass(frozen=True, slots=True)
class TeacherEmbodiedDevelopmentHistoryAssessment:
    history_id: str
    milestones_observed: int
    embodiment_anchored_milestones: int
    history_integrity_status: str
    trajectory_evidence_status: str
    developmental_mechanism_status: str = NOT_ESTABLISHED
    identity_continuity_status: str = NOT_ESTABLISHED
    subjective_continuity_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _milestone_payload(
    *,
    milestone_id: str,
    ordinal: int,
    milestone_kind: str,
    source_locator: str,
    source_digest: str,
    previous_milestone_sha256: str | None,
    changed_surfaces: tuple[str, ...],
    retained_surfaces: tuple[str, ...],
    session_snapshot_sha256: str | None,
    body_trajectory_sha256: str | None,
    controller_state_sha256: str | None,
    body_state_sha256: str | None,
    body_id: str,
) -> dict[str, object]:
    return {
        "milestone_id": milestone_id,
        "ordinal": ordinal,
        "milestone_kind": milestone_kind,
        "source_locator": source_locator,
        "source_digest": source_digest,
        "previous_milestone_sha256": previous_milestone_sha256,
        "changed_surfaces": list(changed_surfaces),
        "retained_surfaces": list(retained_surfaces),
        "session_snapshot_sha256": session_snapshot_sha256,
        "body_trajectory_sha256": body_trajectory_sha256,
        "controller_state_sha256": controller_state_sha256,
        "body_state_sha256": body_state_sha256,
        "body_id": body_id,
    }


def validate_teacher_embodied_development_milestone(
    milestone: TeacherEmbodiedDevelopmentMilestone,
) -> dict[str, str]:
    if not milestone.milestone_id or not milestone.source_locator:
        raise ValueError("development milestone requires identity and source locator")
    if milestone.ordinal < 0:
        raise ValueError("development milestone ordinal must be non-negative")
    if milestone.milestone_kind not in DEVELOPMENT_MILESTONE_KINDS:
        raise ValueError("unsupported Teacher development milestone kind")
    _validate_history_digest("source_digest", milestone.source_digest)
    _validate_optional_sha256(
        "previous_milestone_sha256",
        milestone.previous_milestone_sha256,
    )
    _validate_optional_sha256(
        "session_snapshot_sha256",
        milestone.session_snapshot_sha256,
    )
    _validate_optional_sha256(
        "body_trajectory_sha256",
        milestone.body_trajectory_sha256,
    )
    _validate_optional_sha256(
        "controller_state_sha256",
        milestone.controller_state_sha256,
    )
    _validate_optional_sha256(
        "body_state_sha256",
        milestone.body_state_sha256,
    )
    if not milestone.changed_surfaces:
        raise ValueError("development milestone requires at least one changed surface")
    if len(milestone.changed_surfaces) != len(set(milestone.changed_surfaces)):
        raise ValueError("development milestone changed surfaces must be unique")
    if len(milestone.retained_surfaces) != len(set(milestone.retained_surfaces)):
        raise ValueError("development milestone retained surfaces must be unique")
    if set(milestone.changed_surfaces) & set(milestone.retained_surfaces):
        raise ValueError("changed and retained development surfaces must be disjoint")
    if milestone.body_id != TEACHER_BODY_ID:
        raise ValueError("development milestone Teacher body id drift")
    if milestone.record_status != "RECORDED_REFERENCE_ONLY":
        raise ValueError("development milestone record-status drift")
    if milestone.identity_continuity_claim != "NONE":
        raise ValueError("development milestone cannot establish identity continuity")
    if milestone.subjective_continuity_status != NOT_ESTABLISHED:
        raise ValueError("development milestone cannot establish subjective continuity")
    if milestone.subjectivity_status != NOT_ESTABLISHED:
        raise ValueError("development milestone cannot establish subjectivity")
    if milestone.canonical_effect != "NONE" or milestone.deployment:
        raise ValueError("development milestone must remain non-canonical and undeployed")

    payload = _milestone_payload(
        milestone_id=milestone.milestone_id,
        ordinal=milestone.ordinal,
        milestone_kind=milestone.milestone_kind,
        source_locator=milestone.source_locator,
        source_digest=milestone.source_digest,
        previous_milestone_sha256=milestone.previous_milestone_sha256,
        changed_surfaces=milestone.changed_surfaces,
        retained_surfaces=milestone.retained_surfaces,
        session_snapshot_sha256=milestone.session_snapshot_sha256,
        body_trajectory_sha256=milestone.body_trajectory_sha256,
        controller_state_sha256=milestone.controller_state_sha256,
        body_state_sha256=milestone.body_state_sha256,
        body_id=milestone.body_id,
    )
    if milestone.milestone_sha256 != _history_hash(payload):
        raise ValueError("development milestone hash mismatch")
    return {
        "result": "PASS",
        "source_binding": "PASS",
        "embodiment_provenance": "PASS",
        "milestone_hash": "PASS",
        "identity_nonclaim": "PASS",
    }


def build_teacher_embodied_development_history(
) -> TeacherEmbodiedDevelopmentHistory:
    return TeacherEmbodiedDevelopmentHistory(
        history_id="CHATGPT_TEACHER_EMBODIED_DEVELOPMENT_HISTORY_v0.1",
        body_id=TEACHER_BODY_ID,
        milestones=(),
    )


def validate_teacher_embodied_development_history(
    history: TeacherEmbodiedDevelopmentHistory,
) -> dict[str, str]:
    if not history.history_id:
        raise ValueError("Teacher development history requires identity")
    if history.body_id != TEACHER_BODY_ID:
        raise ValueError("Teacher development history body id drift")
    if history.history_status != "HASH_CHAINED_RECORDED_DEVELOPMENT":
        raise ValueError("Teacher development history status drift")
    if history.identity_continuity_claim != "NONE":
        raise ValueError("Teacher development history cannot establish identity continuity")
    if history.subjective_continuity_status != NOT_ESTABLISHED:
        raise ValueError("Teacher development history cannot establish subjective continuity")
    if history.subjectivity_status != NOT_ESTABLISHED:
        raise ValueError("Teacher development history cannot establish subjectivity")
    if history.canonical_effect != "NONE" or history.deployment:
        raise ValueError("Teacher development history must remain non-canonical and undeployed")

    ids: set[str] = set()
    source_bindings: set[tuple[str, str]] = set()
    previous_hash: str | None = None
    for expected_ordinal, milestone in enumerate(history.milestones):
        validate_teacher_embodied_development_milestone(milestone)
        if milestone.ordinal != expected_ordinal:
            raise ValueError("Teacher development history ordinal discontinuity")
        if milestone.milestone_id in ids:
            raise ValueError("Teacher development milestone ids must be unique")
        source_binding = (milestone.source_locator, milestone.source_digest)
        if source_binding in source_bindings:
            raise ValueError("Teacher development source bindings must be unique")
        if milestone.previous_milestone_sha256 != previous_hash:
            raise ValueError("Teacher development milestone hash-chain discontinuity")
        ids.add(milestone.milestone_id)
        source_bindings.add(source_binding)
        previous_hash = milestone.milestone_sha256

    return {
        "result": "PASS",
        "ordinal_continuity": "PASS",
        "hash_chain": "PASS",
        "source_binding": "PASS",
        "identity_nonclaim": "PASS",
    }


def append_teacher_embodied_development_milestone(
    history: TeacherEmbodiedDevelopmentHistory,
    *,
    milestone_id: str,
    milestone_kind: str,
    source_locator: str,
    source_digest: str,
    changed_surfaces: tuple[str, ...],
    retained_surfaces: tuple[str, ...] = (),
    session_snapshot_sha256: str | None = None,
    body_trajectory_sha256: str | None = None,
    controller_state_sha256: str | None = None,
    body_state_sha256: str | None = None,
) -> TeacherEmbodiedDevelopmentHistory:
    validate_teacher_embodied_development_history(history)
    previous = (
        history.milestones[-1].milestone_sha256
        if history.milestones
        else None
    )
    payload = _milestone_payload(
        milestone_id=milestone_id,
        ordinal=len(history.milestones),
        milestone_kind=milestone_kind,
        source_locator=source_locator,
        source_digest=source_digest,
        previous_milestone_sha256=previous,
        changed_surfaces=changed_surfaces,
        retained_surfaces=retained_surfaces,
        session_snapshot_sha256=session_snapshot_sha256,
        body_trajectory_sha256=body_trajectory_sha256,
        controller_state_sha256=controller_state_sha256,
        body_state_sha256=body_state_sha256,
        body_id=history.body_id,
    )
    milestone = TeacherEmbodiedDevelopmentMilestone(
        milestone_id=milestone_id,
        ordinal=len(history.milestones),
        milestone_kind=milestone_kind,
        source_locator=source_locator,
        source_digest=source_digest,
        previous_milestone_sha256=previous,
        changed_surfaces=changed_surfaces,
        retained_surfaces=retained_surfaces,
        session_snapshot_sha256=session_snapshot_sha256,
        body_trajectory_sha256=body_trajectory_sha256,
        controller_state_sha256=controller_state_sha256,
        body_state_sha256=body_state_sha256,
        milestone_sha256=_history_hash(payload),
        body_id=history.body_id,
    )
    validate_teacher_embodied_development_milestone(milestone)
    updated = replace(
        history,
        milestones=history.milestones + (milestone,),
    )
    validate_teacher_embodied_development_history(updated)
    return updated


def assess_teacher_embodied_development_history(
    history: TeacherEmbodiedDevelopmentHistory,
) -> TeacherEmbodiedDevelopmentHistoryAssessment:
    validate_teacher_embodied_development_history(history)
    anchored = sum(
        1
        for milestone in history.milestones
        if any(
            digest is not None
            for digest in (
                milestone.session_snapshot_sha256,
                milestone.body_trajectory_sha256,
                milestone.controller_state_sha256,
                milestone.body_state_sha256,
            )
        )
    )
    if len(history.milestones) < 2:
        evidence = "INSUFFICIENT_DEVELOPMENT_HISTORY"
    elif anchored == 0:
        evidence = "RECORDED_CHANGE_HISTORY_WITHOUT_EMBODIMENT_ANCHOR"
    else:
        evidence = "RECORDED_EMBODIED_DEVELOPMENT_HISTORY_PRESENT"

    return TeacherEmbodiedDevelopmentHistoryAssessment(
        history_id=history.history_id,
        milestones_observed=len(history.milestones),
        embodiment_anchored_milestones=anchored,
        history_integrity_status="HASH_CHAIN_VALID",
        trajectory_evidence_status=evidence,
    )
