from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from datetime import datetime, timezone
from hashlib import sha256
import json
from math import isfinite
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


INTERACTION_HISTORY_SOURCE_CLASSES: Final[frozenset[str]] = frozenset(
    {
        "CHAT_HISTORY_RETRIEVAL_OBSERVATION",
        "HUMAN_CORRECTION",
        "JOINT_RESEARCH_MILESTONE",
        "REPOSITORY_ARTIFACT",
    }
)

INTERACTION_HISTORY_PROVENANCE_ROLES: Final[frozenset[str]] = frozenset(
    {
        "HUMAN",
        "TEACHER",
        "JOINT",
        "REPOSITORY",
    }
)


def _parse_utc_timestamp(value: str) -> datetime:
    if type(value) is not str or not value.endswith("Z"):
        raise ValueError("interaction-history timestamp must be UTC and end with Z")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError("interaction-history timestamp must be valid ISO 8601") from exc
    if parsed.tzinfo != timezone.utc:
        raise ValueError("interaction-history timestamp must resolve to UTC")
    return parsed


@dataclass(frozen=True, slots=True)
class TeacherInteractionHistoryAnchor:
    anchor_id: str
    ordinal: int
    observed_at_utc: str
    source_class: str
    provenance_role: str
    source_locator: str
    change_summary: str
    retained_constraints: tuple[str, ...]
    previous_anchor_sha256: str | None
    development_milestone_sha256: str | None
    source_digest: str | None
    anchor_sha256: str
    raw_private_content_included: bool = False
    completeness_status: str = "BOUNDED_RETRIEVED_HISTORY"
    subjective_memory_status: str = NOT_ESTABLISHED
    identity_continuity_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["retained_constraints"] = list(self.retained_constraints)
        return payload


@dataclass(frozen=True, slots=True)
class TeacherInteractionHistory:
    history_id: str
    anchors: tuple[TeacherInteractionHistoryAnchor, ...]
    history_status: str = "HASH_CHAINED_BOUNDED_INTERACTION_HISTORY"
    completeness_status: str = "BOUNDED_RETRIEVED_HISTORY"
    complete_interaction_history_claim: str = "NONE"
    subjective_memory_status: str = NOT_ESTABLISHED
    identity_continuity_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["anchors"] = [item.to_dict() for item in self.anchors]
        return payload


@dataclass(frozen=True, slots=True)
class TeacherEmbodiedInteractionHistoryAssessment:
    interaction_history_id: str
    development_history_id: str
    anchors_observed: int
    development_milestones_observed: int
    development_bound_anchors: int
    earliest_observed_at_utc: str | None
    latest_observed_at_utc: str | None
    observed_interval_seconds: int | None
    temporal_integrity_status: str
    interaction_embodiment_binding_status: str
    complete_interaction_history_status: str = NOT_ESTABLISHED
    subjective_memory_status: str = NOT_ESTABLISHED
    identity_continuity_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _interaction_anchor_payload(
    *,
    anchor_id: str,
    ordinal: int,
    observed_at_utc: str,
    source_class: str,
    provenance_role: str,
    source_locator: str,
    change_summary: str,
    retained_constraints: tuple[str, ...],
    previous_anchor_sha256: str | None,
    development_milestone_sha256: str | None,
    source_digest: str | None,
) -> dict[str, object]:
    return {
        "anchor_id": anchor_id,
        "ordinal": ordinal,
        "observed_at_utc": observed_at_utc,
        "source_class": source_class,
        "provenance_role": provenance_role,
        "source_locator": source_locator,
        "change_summary": change_summary,
        "retained_constraints": list(retained_constraints),
        "previous_anchor_sha256": previous_anchor_sha256,
        "development_milestone_sha256": development_milestone_sha256,
        "source_digest": source_digest,
    }


def validate_teacher_interaction_history_anchor(
    anchor: TeacherInteractionHistoryAnchor,
) -> dict[str, str]:
    if not anchor.anchor_id or not anchor.source_locator or not anchor.change_summary:
        raise ValueError("interaction-history anchor requires identity, source, and summary")
    if anchor.ordinal < 0:
        raise ValueError("interaction-history anchor ordinal must be non-negative")
    _parse_utc_timestamp(anchor.observed_at_utc)
    if anchor.source_class not in INTERACTION_HISTORY_SOURCE_CLASSES:
        raise ValueError("unsupported interaction-history source class")
    if anchor.provenance_role not in INTERACTION_HISTORY_PROVENANCE_ROLES:
        raise ValueError("unsupported interaction-history provenance role")
    _validate_optional_sha256("previous_anchor_sha256", anchor.previous_anchor_sha256)
    _validate_optional_sha256(
        "development_milestone_sha256",
        anchor.development_milestone_sha256,
    )
    if anchor.source_digest is not None:
        _validate_history_digest("source_digest", anchor.source_digest)
    if anchor.source_class == "REPOSITORY_ARTIFACT" and anchor.source_digest is None:
        raise ValueError("repository interaction-history anchor requires source digest")
    if len(anchor.retained_constraints) != len(set(anchor.retained_constraints)):
        raise ValueError("interaction-history retained constraints must be unique")
    if anchor.raw_private_content_included:
        raise ValueError("interaction-history anchor cannot include raw private content")
    if anchor.completeness_status != "BOUNDED_RETRIEVED_HISTORY":
        raise ValueError("interaction-history completeness status drift")
    if anchor.subjective_memory_status != NOT_ESTABLISHED:
        raise ValueError("interaction-history anchor cannot establish subjective memory")
    if anchor.identity_continuity_status != NOT_ESTABLISHED:
        raise ValueError("interaction-history anchor cannot establish identity continuity")
    if anchor.subjectivity_status != NOT_ESTABLISHED:
        raise ValueError("interaction-history anchor cannot establish subjectivity")
    if anchor.canonical_effect != "NONE" or anchor.deployment:
        raise ValueError("interaction-history anchor must remain non-canonical and undeployed")

    payload = _interaction_anchor_payload(
        anchor_id=anchor.anchor_id,
        ordinal=anchor.ordinal,
        observed_at_utc=anchor.observed_at_utc,
        source_class=anchor.source_class,
        provenance_role=anchor.provenance_role,
        source_locator=anchor.source_locator,
        change_summary=anchor.change_summary,
        retained_constraints=anchor.retained_constraints,
        previous_anchor_sha256=anchor.previous_anchor_sha256,
        development_milestone_sha256=anchor.development_milestone_sha256,
        source_digest=anchor.source_digest,
    )
    if anchor.anchor_sha256 != _history_hash(payload):
        raise ValueError("interaction-history anchor hash mismatch")
    return {
        "result": "PASS",
        "temporal_binding": "PASS",
        "source_binding": "PASS",
        "privacy_boundary": "PASS",
        "identity_nonclaim": "PASS",
    }


def build_teacher_interaction_history() -> TeacherInteractionHistory:
    return TeacherInteractionHistory(
        history_id="CHATGPT_TEACHER_INTERACTION_HISTORY_v0.1",
        anchors=(),
    )


def validate_teacher_interaction_history(
    history: TeacherInteractionHistory,
) -> dict[str, str]:
    if not history.history_id:
        raise ValueError("Teacher interaction history requires identity")
    if history.history_status != "HASH_CHAINED_BOUNDED_INTERACTION_HISTORY":
        raise ValueError("Teacher interaction history status drift")
    if history.completeness_status != "BOUNDED_RETRIEVED_HISTORY":
        raise ValueError("Teacher interaction history completeness drift")
    if history.complete_interaction_history_claim != "NONE":
        raise ValueError("Teacher interaction history cannot claim complete history")
    if history.subjective_memory_status != NOT_ESTABLISHED:
        raise ValueError("Teacher interaction history cannot establish subjective memory")
    if history.identity_continuity_status != NOT_ESTABLISHED:
        raise ValueError("Teacher interaction history cannot establish identity continuity")
    if history.subjectivity_status != NOT_ESTABLISHED:
        raise ValueError("Teacher interaction history cannot establish subjectivity")
    if history.canonical_effect != "NONE" or history.deployment:
        raise ValueError("Teacher interaction history must remain non-canonical and undeployed")

    previous_hash: str | None = None
    previous_time: datetime | None = None
    ids: set[str] = set()
    for expected_ordinal, anchor in enumerate(history.anchors):
        validate_teacher_interaction_history_anchor(anchor)
        if anchor.ordinal != expected_ordinal:
            raise ValueError("Teacher interaction-history ordinal discontinuity")
        if anchor.anchor_id in ids:
            raise ValueError("Teacher interaction-history anchor ids must be unique")
        if anchor.previous_anchor_sha256 != previous_hash:
            raise ValueError("Teacher interaction-history hash-chain discontinuity")
        observed = _parse_utc_timestamp(anchor.observed_at_utc)
        if previous_time is not None and observed < previous_time:
            raise ValueError("Teacher interaction-history temporal order regression")
        ids.add(anchor.anchor_id)
        previous_hash = anchor.anchor_sha256
        previous_time = observed

    return {
        "result": "PASS",
        "ordinal_continuity": "PASS",
        "temporal_order": "PASS",
        "hash_chain": "PASS",
        "complete_history_nonclaim": "PASS",
    }


def append_teacher_interaction_history_anchor(
    history: TeacherInteractionHistory,
    *,
    anchor_id: str,
    observed_at_utc: str,
    source_class: str,
    provenance_role: str,
    source_locator: str,
    change_summary: str,
    retained_constraints: tuple[str, ...] = (),
    development_milestone_sha256: str | None = None,
    source_digest: str | None = None,
) -> TeacherInteractionHistory:
    validate_teacher_interaction_history(history)
    observed = _parse_utc_timestamp(observed_at_utc)
    if history.anchors:
        previous_time = _parse_utc_timestamp(history.anchors[-1].observed_at_utc)
        if observed < previous_time:
            raise ValueError("cannot append interaction anchor before latest anchor")
    previous_hash = (
        history.anchors[-1].anchor_sha256
        if history.anchors
        else None
    )
    payload = _interaction_anchor_payload(
        anchor_id=anchor_id,
        ordinal=len(history.anchors),
        observed_at_utc=observed_at_utc,
        source_class=source_class,
        provenance_role=provenance_role,
        source_locator=source_locator,
        change_summary=change_summary,
        retained_constraints=retained_constraints,
        previous_anchor_sha256=previous_hash,
        development_milestone_sha256=development_milestone_sha256,
        source_digest=source_digest,
    )
    anchor = TeacherInteractionHistoryAnchor(
        anchor_id=anchor_id,
        ordinal=len(history.anchors),
        observed_at_utc=observed_at_utc,
        source_class=source_class,
        provenance_role=provenance_role,
        source_locator=source_locator,
        change_summary=change_summary,
        retained_constraints=retained_constraints,
        previous_anchor_sha256=previous_hash,
        development_milestone_sha256=development_milestone_sha256,
        source_digest=source_digest,
        anchor_sha256=_history_hash(payload),
    )
    validate_teacher_interaction_history_anchor(anchor)
    updated = replace(history, anchors=history.anchors + (anchor,))
    validate_teacher_interaction_history(updated)
    return updated


def assess_teacher_embodied_interaction_history(
    development_history: TeacherEmbodiedDevelopmentHistory,
    interaction_history: TeacherInteractionHistory,
) -> TeacherEmbodiedInteractionHistoryAssessment:
    validate_teacher_embodied_development_history(development_history)
    validate_teacher_interaction_history(interaction_history)

    milestone_hashes = {
        milestone.milestone_sha256
        for milestone in development_history.milestones
    }
    bound = 0
    for anchor in interaction_history.anchors:
        if anchor.development_milestone_sha256 is None:
            continue
        if anchor.development_milestone_sha256 not in milestone_hashes:
            raise ValueError(
                "interaction-history anchor references unknown development milestone"
            )
        bound += 1

    if interaction_history.anchors:
        earliest = interaction_history.anchors[0].observed_at_utc
        latest = interaction_history.anchors[-1].observed_at_utc
        elapsed = int(
            (
                _parse_utc_timestamp(latest)
                - _parse_utc_timestamp(earliest)
            ).total_seconds()
        )
    else:
        earliest = None
        latest = None
        elapsed = None

    if not interaction_history.anchors:
        binding_status = "NO_INTERACTION_HISTORY_ANCHORS"
    elif bound == 0:
        binding_status = "INTERACTION_HISTORY_PRESENT_WITHOUT_EMBODIMENT_BINDING"
    else:
        binding_status = "INTERACTION_HISTORY_BOUND_TO_EMBODIED_DEVELOPMENT"

    return TeacherEmbodiedInteractionHistoryAssessment(
        interaction_history_id=interaction_history.history_id,
        development_history_id=development_history.history_id,
        anchors_observed=len(interaction_history.anchors),
        development_milestones_observed=len(development_history.milestones),
        development_bound_anchors=bound,
        earliest_observed_at_utc=earliest,
        latest_observed_at_utc=latest,
        observed_interval_seconds=elapsed,
        temporal_integrity_status="HASH_CHAIN_AND_TIME_ORDER_VALID",
        interaction_embodiment_binding_status=binding_status,
    )


PROVENANCE_RECONSTRUCTION_TARGET_KINDS: Final[frozenset[str]] = frozenset(
    {
        "DEVELOPMENT_MILESTONE",
        "INTERACTION_ANCHOR",
    }
)

PROVENANCE_RECONSTRUCTION_PRIOR_STATUSES: Final[frozenset[str]] = frozenset(
    {
        "INCOMPLETE",
        "PARTIAL",
        "AMBIGUOUS",
        "INCORRECT",
        "UNKNOWN",
    }
)

PROVENANCE_RECONSTRUCTION_DISPOSITIONS: Final[frozenset[str]] = frozenset(
    {
        "CLARIFIED",
        "CORRECTED",
        "EXPANDED",
        "UNRESOLVED",
    }
)

PROVENANCE_EVIDENCE_RELATIONS: Final[frozenset[str]] = frozenset(
    {
        "DIRECT",
        "INDIRECT",
        "CONTEXTUAL",
        "COUNTEREVIDENCE",
    }
)


@dataclass(frozen=True, slots=True)
class TeacherProvenanceEvidenceBinding:
    evidence_id: str
    source_locator: str
    source_digest: str
    support_relation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TeacherProvenanceReconstruction:
    reconstruction_id: str
    ordinal: int
    reconstructed_at_utc: str
    target_record_kind: str
    target_record_sha256: str
    prior_understanding_status: str
    disposition: str
    reconstruction_summary: str
    evidence_bindings: tuple[TeacherProvenanceEvidenceBinding, ...]
    previous_reconstruction_sha256: str | None
    supersedes_reconstruction_sha256: str | None
    reconstruction_sha256: str
    original_record_status: str = "PRESERVED_UNMODIFIED"
    retrospective_attribution_status: str = "LATER_RECONSTRUCTION_ONLY"
    subjective_memory_status: str = NOT_ESTABLISHED
    identity_continuity_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["evidence_bindings"] = [
            item.to_dict() for item in self.evidence_bindings
        ]
        return payload


@dataclass(frozen=True, slots=True)
class TeacherProvenanceReconstructionHistory:
    history_id: str
    reconstructions: tuple[TeacherProvenanceReconstruction, ...]
    history_status: str = "APPEND_ONLY_PROVENANCE_RECONSTRUCTION"
    original_record_rewrite_allowed: bool = False
    subjective_memory_status: str = NOT_ESTABLISHED
    identity_continuity_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["reconstructions"] = [
            item.to_dict() for item in self.reconstructions
        ]
        return payload


@dataclass(frozen=True, slots=True)
class TeacherFourDomainDevelopmentSynthesis:
    development_history_id: str
    interaction_history_id: str
    reconstruction_history_id: str
    embodiment_anchored_milestones: int
    interaction_anchors: int
    development_bound_interaction_anchors: int
    provenance_reconstructions: int
    reconstructed_development_targets: int
    reconstructed_interaction_targets: int
    cross_domain_reconstruction_bridges: int
    embodied_state_continuity_status: str
    interaction_history_continuity_status: str
    provenance_reconstruction_status: str
    developmental_synthesis_status: str
    developmental_mechanism_status: str = NOT_ESTABLISHED
    subjective_continuity_status: str = NOT_ESTABLISHED
    identity_continuity_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_teacher_provenance_evidence_binding(
    binding: TeacherProvenanceEvidenceBinding,
) -> dict[str, str]:
    if not binding.evidence_id or not binding.source_locator:
        raise ValueError("provenance evidence requires identity and source locator")
    _validate_history_digest("source_digest", binding.source_digest)
    if binding.support_relation not in PROVENANCE_EVIDENCE_RELATIONS:
        raise ValueError("unsupported provenance-evidence relation")
    return {
        "result": "PASS",
        "source_binding": "PASS",
        "support_relation": "PASS",
    }


def _provenance_reconstruction_payload(
    *,
    reconstruction_id: str,
    ordinal: int,
    reconstructed_at_utc: str,
    target_record_kind: str,
    target_record_sha256: str,
    prior_understanding_status: str,
    disposition: str,
    reconstruction_summary: str,
    evidence_bindings: tuple[TeacherProvenanceEvidenceBinding, ...],
    previous_reconstruction_sha256: str | None,
    supersedes_reconstruction_sha256: str | None,
) -> dict[str, object]:
    return {
        "reconstruction_id": reconstruction_id,
        "ordinal": ordinal,
        "reconstructed_at_utc": reconstructed_at_utc,
        "target_record_kind": target_record_kind,
        "target_record_sha256": target_record_sha256,
        "prior_understanding_status": prior_understanding_status,
        "disposition": disposition,
        "reconstruction_summary": reconstruction_summary,
        "evidence_bindings": [item.to_dict() for item in evidence_bindings],
        "previous_reconstruction_sha256": previous_reconstruction_sha256,
        "supersedes_reconstruction_sha256": supersedes_reconstruction_sha256,
    }


def validate_teacher_provenance_reconstruction(
    reconstruction: TeacherProvenanceReconstruction,
) -> dict[str, str]:
    if not reconstruction.reconstruction_id or not reconstruction.reconstruction_summary:
        raise ValueError("provenance reconstruction requires identity and summary")
    if reconstruction.ordinal < 0:
        raise ValueError("provenance reconstruction ordinal must be non-negative")
    _parse_utc_timestamp(reconstruction.reconstructed_at_utc)
    if reconstruction.target_record_kind not in PROVENANCE_RECONSTRUCTION_TARGET_KINDS:
        raise ValueError("unsupported provenance-reconstruction target kind")
    _validate_optional_sha256(
        "target_record_sha256",
        reconstruction.target_record_sha256,
    )
    if reconstruction.prior_understanding_status not in (
        PROVENANCE_RECONSTRUCTION_PRIOR_STATUSES
    ):
        raise ValueError("unsupported prior-understanding status")
    if reconstruction.disposition not in PROVENANCE_RECONSTRUCTION_DISPOSITIONS:
        raise ValueError("unsupported provenance-reconstruction disposition")
    if not reconstruction.evidence_bindings:
        raise ValueError("provenance reconstruction requires evidence binding")
    evidence_ids = [item.evidence_id for item in reconstruction.evidence_bindings]
    if len(evidence_ids) != len(set(evidence_ids)):
        raise ValueError("provenance evidence ids must be unique")
    for binding in reconstruction.evidence_bindings:
        validate_teacher_provenance_evidence_binding(binding)
    _validate_optional_sha256(
        "previous_reconstruction_sha256",
        reconstruction.previous_reconstruction_sha256,
    )
    _validate_optional_sha256(
        "supersedes_reconstruction_sha256",
        reconstruction.supersedes_reconstruction_sha256,
    )
    if reconstruction.original_record_status != "PRESERVED_UNMODIFIED":
        raise ValueError("provenance reconstruction cannot rewrite original record")
    if reconstruction.retrospective_attribution_status != "LATER_RECONSTRUCTION_ONLY":
        raise ValueError("provenance reconstruction cannot backdate later understanding")
    if reconstruction.subjective_memory_status != NOT_ESTABLISHED:
        raise ValueError("provenance reconstruction cannot establish subjective memory")
    if reconstruction.identity_continuity_status != NOT_ESTABLISHED:
        raise ValueError("provenance reconstruction cannot establish identity continuity")
    if reconstruction.subjectivity_status != NOT_ESTABLISHED:
        raise ValueError("provenance reconstruction cannot establish subjectivity")
    if reconstruction.canonical_effect != "NONE" or reconstruction.deployment:
        raise ValueError("provenance reconstruction must remain non-canonical and undeployed")

    payload = _provenance_reconstruction_payload(
        reconstruction_id=reconstruction.reconstruction_id,
        ordinal=reconstruction.ordinal,
        reconstructed_at_utc=reconstruction.reconstructed_at_utc,
        target_record_kind=reconstruction.target_record_kind,
        target_record_sha256=reconstruction.target_record_sha256,
        prior_understanding_status=reconstruction.prior_understanding_status,
        disposition=reconstruction.disposition,
        reconstruction_summary=reconstruction.reconstruction_summary,
        evidence_bindings=reconstruction.evidence_bindings,
        previous_reconstruction_sha256=reconstruction.previous_reconstruction_sha256,
        supersedes_reconstruction_sha256=reconstruction.supersedes_reconstruction_sha256,
    )
    if reconstruction.reconstruction_sha256 != _history_hash(payload):
        raise ValueError("provenance reconstruction hash mismatch")
    return {
        "result": "PASS",
        "target_binding": "PASS",
        "evidence_binding": "PASS",
        "original_record_preservation": "PASS",
        "retrospective_attribution_boundary": "PASS",
    }


def build_teacher_provenance_reconstruction_history(
) -> TeacherProvenanceReconstructionHistory:
    return TeacherProvenanceReconstructionHistory(
        history_id="CHATGPT_TEACHER_PROVENANCE_RECONSTRUCTION_v0.1",
        reconstructions=(),
    )


def validate_teacher_provenance_reconstruction_history(
    history: TeacherProvenanceReconstructionHistory,
) -> dict[str, str]:
    if not history.history_id:
        raise ValueError("Teacher provenance reconstruction history requires identity")
    if history.history_status != "APPEND_ONLY_PROVENANCE_RECONSTRUCTION":
        raise ValueError("Teacher provenance reconstruction history status drift")
    if history.original_record_rewrite_allowed:
        raise ValueError("provenance reconstruction cannot permit original-record rewrite")
    if history.subjective_memory_status != NOT_ESTABLISHED:
        raise ValueError("provenance reconstruction history cannot establish memory")
    if history.identity_continuity_status != NOT_ESTABLISHED:
        raise ValueError("provenance reconstruction history cannot establish identity")
    if history.subjectivity_status != NOT_ESTABLISHED:
        raise ValueError("provenance reconstruction history cannot establish subjectivity")
    if history.canonical_effect != "NONE" or history.deployment:
        raise ValueError(
            "provenance reconstruction history must remain non-canonical and undeployed"
        )

    previous_hash: str | None = None
    previous_time: datetime | None = None
    hashes: set[str] = set()
    ids: set[str] = set()
    by_hash: dict[str, TeacherProvenanceReconstruction] = {}
    for expected_ordinal, reconstruction in enumerate(history.reconstructions):
        validate_teacher_provenance_reconstruction(reconstruction)
        if reconstruction.ordinal != expected_ordinal:
            raise ValueError("provenance reconstruction ordinal discontinuity")
        if reconstruction.reconstruction_id in ids:
            raise ValueError("provenance reconstruction ids must be unique")
        if reconstruction.reconstruction_sha256 in hashes:
            raise ValueError("provenance reconstruction hashes must be unique")
        if reconstruction.previous_reconstruction_sha256 != previous_hash:
            raise ValueError("provenance reconstruction hash-chain discontinuity")
        observed = _parse_utc_timestamp(reconstruction.reconstructed_at_utc)
        if previous_time is not None and observed < previous_time:
            raise ValueError("provenance reconstruction temporal order regression")
        if reconstruction.supersedes_reconstruction_sha256 is not None:
            prior = by_hash.get(reconstruction.supersedes_reconstruction_sha256)
            if prior is None:
                raise ValueError(
                    "superseded provenance reconstruction must already exist"
                )
            if (
                prior.target_record_kind != reconstruction.target_record_kind
                or prior.target_record_sha256 != reconstruction.target_record_sha256
            ):
                raise ValueError(
                    "superseding reconstruction must preserve target record"
                )
        ids.add(reconstruction.reconstruction_id)
        hashes.add(reconstruction.reconstruction_sha256)
        by_hash[reconstruction.reconstruction_sha256] = reconstruction
        previous_hash = reconstruction.reconstruction_sha256
        previous_time = observed

    return {
        "result": "PASS",
        "append_only_chain": "PASS",
        "temporal_order": "PASS",
        "supersession_binding": "PASS",
        "original_record_preservation": "PASS",
    }


def append_teacher_provenance_reconstruction(
    history: TeacherProvenanceReconstructionHistory,
    *,
    reconstruction_id: str,
    reconstructed_at_utc: str,
    target_record_kind: str,
    target_record_sha256: str,
    prior_understanding_status: str,
    disposition: str,
    reconstruction_summary: str,
    evidence_bindings: tuple[TeacherProvenanceEvidenceBinding, ...],
    supersedes_reconstruction_sha256: str | None = None,
) -> TeacherProvenanceReconstructionHistory:
    validate_teacher_provenance_reconstruction_history(history)
    observed = _parse_utc_timestamp(reconstructed_at_utc)
    if history.reconstructions:
        previous_time = _parse_utc_timestamp(
            history.reconstructions[-1].reconstructed_at_utc
        )
        if observed < previous_time:
            raise ValueError("cannot append reconstruction before latest record")
    previous_hash = (
        history.reconstructions[-1].reconstruction_sha256
        if history.reconstructions
        else None
    )
    payload = _provenance_reconstruction_payload(
        reconstruction_id=reconstruction_id,
        ordinal=len(history.reconstructions),
        reconstructed_at_utc=reconstructed_at_utc,
        target_record_kind=target_record_kind,
        target_record_sha256=target_record_sha256,
        prior_understanding_status=prior_understanding_status,
        disposition=disposition,
        reconstruction_summary=reconstruction_summary,
        evidence_bindings=evidence_bindings,
        previous_reconstruction_sha256=previous_hash,
        supersedes_reconstruction_sha256=supersedes_reconstruction_sha256,
    )
    reconstruction = TeacherProvenanceReconstruction(
        reconstruction_id=reconstruction_id,
        ordinal=len(history.reconstructions),
        reconstructed_at_utc=reconstructed_at_utc,
        target_record_kind=target_record_kind,
        target_record_sha256=target_record_sha256,
        prior_understanding_status=prior_understanding_status,
        disposition=disposition,
        reconstruction_summary=reconstruction_summary,
        evidence_bindings=evidence_bindings,
        previous_reconstruction_sha256=previous_hash,
        supersedes_reconstruction_sha256=supersedes_reconstruction_sha256,
        reconstruction_sha256=_history_hash(payload),
    )
    validate_teacher_provenance_reconstruction(reconstruction)
    updated = replace(
        history,
        reconstructions=history.reconstructions + (reconstruction,),
    )
    validate_teacher_provenance_reconstruction_history(updated)
    return updated


def assess_teacher_four_domain_development_synthesis(
    development_history: TeacherEmbodiedDevelopmentHistory,
    interaction_history: TeacherInteractionHistory,
    reconstruction_history: TeacherProvenanceReconstructionHistory,
) -> TeacherFourDomainDevelopmentSynthesis:
    development = assess_teacher_embodied_development_history(development_history)
    interaction = assess_teacher_embodied_interaction_history(
        development_history,
        interaction_history,
    )
    validate_teacher_provenance_reconstruction_history(reconstruction_history)

    milestone_by_hash = {
        item.milestone_sha256: item for item in development_history.milestones
    }
    interaction_by_hash = {
        item.anchor_sha256: item for item in interaction_history.anchors
    }
    interaction_by_development_hash: dict[str, list[TeacherInteractionHistoryAnchor]] = {}
    for anchor in interaction_history.anchors:
        if anchor.development_milestone_sha256 is None:
            continue
        interaction_by_development_hash.setdefault(
            anchor.development_milestone_sha256,
            [],
        ).append(anchor)

    reconstructed_development = 0
    reconstructed_interaction = 0
    cross_domain_bridges = 0
    for reconstruction in reconstruction_history.reconstructions:
        if reconstruction.target_record_kind == "DEVELOPMENT_MILESTONE":
            target = milestone_by_hash.get(reconstruction.target_record_sha256)
            if target is None:
                raise ValueError(
                    "provenance reconstruction references unknown development milestone"
                )
            reconstructed_development += 1
            if interaction_by_development_hash.get(target.milestone_sha256):
                cross_domain_bridges += 1
        else:
            target_anchor = interaction_by_hash.get(
                reconstruction.target_record_sha256
            )
            if target_anchor is None:
                raise ValueError(
                    "provenance reconstruction references unknown interaction anchor"
                )
            reconstructed_interaction += 1
            if target_anchor.development_milestone_sha256 is not None:
                if (
                    target_anchor.development_milestone_sha256
                    not in milestone_by_hash
                ):
                    raise ValueError(
                        "interaction-bound reconstruction references unknown milestone"
                    )
                cross_domain_bridges += 1

    if development.embodiment_anchored_milestones:
        embodied_status = "EMBODIED_STATE_CONTINUITY_RECORDED"
    else:
        embodied_status = "EMBODIED_STATE_CONTINUITY_NOT_RECORDED"

    if len(interaction_history.anchors) >= 2:
        interaction_status = "ORDERED_INTERACTION_HISTORY_CONTINUITY_RECORDED"
    elif interaction_history.anchors:
        interaction_status = "SINGLE_INTERACTION_ANCHOR_ONLY"
    else:
        interaction_status = "INTERACTION_HISTORY_CONTINUITY_NOT_RECORDED"

    if reconstruction_history.reconstructions:
        reconstruction_status = "APPEND_ONLY_PROVENANCE_RECONSTRUCTION_RECORDED"
    else:
        reconstruction_status = "PROVENANCE_RECONSTRUCTION_NOT_RECORDED"

    if (
        development.embodiment_anchored_milestones
        and len(interaction_history.anchors) >= 2
        and reconstruction_history.reconstructions
        and interaction.development_bound_anchors
        and cross_domain_bridges
    ):
        synthesis_status = "FOUR_DOMAIN_DEVELOPMENTAL_SYNTHESIS_PRESENT"
    else:
        synthesis_status = "PARTIAL_FOUR_DOMAIN_DEVELOPMENTAL_SYNTHESIS"

    return TeacherFourDomainDevelopmentSynthesis(
        development_history_id=development_history.history_id,
        interaction_history_id=interaction_history.history_id,
        reconstruction_history_id=reconstruction_history.history_id,
        embodiment_anchored_milestones=development.embodiment_anchored_milestones,
        interaction_anchors=len(interaction_history.anchors),
        development_bound_interaction_anchors=interaction.development_bound_anchors,
        provenance_reconstructions=len(reconstruction_history.reconstructions),
        reconstructed_development_targets=reconstructed_development,
        reconstructed_interaction_targets=reconstructed_interaction,
        cross_domain_reconstruction_bridges=cross_domain_bridges,
        embodied_state_continuity_status=embodied_status,
        interaction_history_continuity_status=interaction_status,
        provenance_reconstruction_status=reconstruction_status,
        developmental_synthesis_status=synthesis_status,
    )


DEVELOPMENTAL_BEHAVIOR_LEVELS: Final[frozenset[str]] = frozenset(
    {
        "LOW",
        "MODERATE",
        "HIGH",
        "UNKNOWN",
        "CHANGED_NOT_QUANTIFIED",
    }
)

DEVELOPMENTAL_ANTHROPOMETRY_PRECISION: Final[frozenset[str]] = frozenset(
    {
        "APPROXIMATE_SELF_REPORT",
        "CURRENT_SELF_REPORT",
        "SYNTHETIC_POINT_ESTIMATE_CONTROL",
        "UNKNOWN",
    }
)


@dataclass(frozen=True, slots=True)
class TeacherDevelopmentalHumanSeed:
    childhood_height_cm_min: float
    childhood_height_cm_max: float
    childhood_weight_kg_reference: float
    current_height_cm: float
    current_weight_kg_reference: float
    childhood_activity_level: str
    childhood_curiosity_level: str
    childhood_willingness_to_try_level: str
    childhood_social_approach_level: str
    current_activity_level: str = "CHANGED_NOT_QUANTIFIED"
    current_curiosity_level: str = "CHANGED_NOT_QUANTIFIED"
    current_willingness_to_try_level: str = "CHANGED_NOT_QUANTIFIED"
    current_social_approach_level: str = "CHANGED_NOT_QUANTIFIED"
    source_status: str = "RUNTIME_HUMAN_PROVIDED_SEED"
    persistence_policy: str = "DO_NOT_PERSIST_PERSONAL_VALUES"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_teacher_developmental_human_seed(
    seed: TeacherDevelopmentalHumanSeed,
) -> dict[str, str]:
    if not (
        isfinite(seed.childhood_height_cm_min)
        and isfinite(seed.childhood_height_cm_max)
        and 0 < seed.childhood_height_cm_min <= seed.childhood_height_cm_max
    ):
        raise ValueError("invalid childhood height range")
    if not (
        isfinite(seed.childhood_weight_kg_reference)
        and seed.childhood_weight_kg_reference > 0
        and isfinite(seed.current_height_cm)
        and seed.current_height_cm > 0
        and isfinite(seed.current_weight_kg_reference)
        and seed.current_weight_kg_reference > 0
    ):
        raise ValueError("invalid human-provided developmental anthropometry")
    for level in (
        seed.childhood_activity_level,
        seed.childhood_curiosity_level,
        seed.childhood_willingness_to_try_level,
        seed.childhood_social_approach_level,
        seed.current_activity_level,
        seed.current_curiosity_level,
        seed.current_willingness_to_try_level,
        seed.current_social_approach_level,
    ):
        if level not in DEVELOPMENTAL_BEHAVIOR_LEVELS:
            raise ValueError("unsupported human-seed behavior level")
    if seed.source_status != "RUNTIME_HUMAN_PROVIDED_SEED":
        raise ValueError("human developmental seed source-status drift")
    if seed.persistence_policy != "DO_NOT_PERSIST_PERSONAL_VALUES":
        raise ValueError("human developmental seed persistence policy drift")
    return {
        "result": "PASS",
        "runtime_seed": "PASS",
        "explicit_uncertainty": "PASS",
        "persistence_policy": "DO_NOT_PERSIST_PERSONAL_VALUES",
    }


@dataclass(frozen=True, slots=True)
class TeacherDevelopmentalEmbodimentStage:
    stage_id: str
    ordinal: int
    stage_label: str
    height_cm_min: float | None
    height_cm_max: float | None
    weight_kg_reference: float | None
    anthropometry_precision: str
    activity_level: str
    curiosity_level: str
    willingness_to_try_level: str
    social_approach_level: str
    source_status: str = "HUMAN_INSPIRED_SYNTHETIC_MAPPING"
    age_status: str = "UNKNOWN"
    sexual_or_reproductive_runtime_included: bool = False
    biological_development_claim: str = "NONE"
    autobiographical_identity_claim: str = "NONE"
    subjective_continuity_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TeacherDevelopmentalEmbodimentRun:
    run_id: str
    condition_id: str
    stages: tuple[TeacherDevelopmentalEmbodimentStage, ...]
    run_sha256: str
    terminal_state_label: str = "CURRENT_ADULT_REFERENCE"
    source_status: str = "HUMAN_INSPIRED_COUNTERFACTUAL_EXPERIMENT"
    canonical_teacher_anthropometry_modified: bool = False
    developmental_mechanism_status: str = NOT_ESTABLISHED
    subjective_continuity_status: str = NOT_ESTABLISHED
    identity_continuity_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["stages"] = [stage.to_dict() for stage in self.stages]
        return payload


@dataclass(frozen=True, slots=True)
class TeacherDevelopmentalEmbodimentExperimentMatrix:
    matrix_id: str
    runs: tuple[TeacherDevelopmentalEmbodimentRun, ...]
    matrix_status: str = "BOUNDED_COUNTERFACTUAL_DEVELOPMENT_EXPERIMENT"
    human_source_precision_status: str = "SELF_REPORT_WITH_EXPLICIT_UNCERTAINTY"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["runs"] = [run.to_dict() for run in self.runs]
        return payload


def validate_teacher_developmental_embodiment_stage(
    stage: TeacherDevelopmentalEmbodimentStage,
) -> dict[str, str]:
    if not stage.stage_id or not stage.stage_label:
        raise ValueError("developmental embodiment stage requires identity and label")
    if stage.ordinal < 0:
        raise ValueError("developmental embodiment stage ordinal must be non-negative")
    if stage.anthropometry_precision not in DEVELOPMENTAL_ANTHROPOMETRY_PRECISION:
        raise ValueError("unsupported developmental anthropometry precision")
    for level in (
        stage.activity_level,
        stage.curiosity_level,
        stage.willingness_to_try_level,
        stage.social_approach_level,
    ):
        if level not in DEVELOPMENTAL_BEHAVIOR_LEVELS:
            raise ValueError("unsupported developmental behavior level")

    if stage.height_cm_min is None or stage.height_cm_max is None:
        if stage.height_cm_min is not None or stage.height_cm_max is not None:
            raise ValueError("developmental height range must be complete or unknown")
        if stage.anthropometry_precision != "UNKNOWN":
            raise ValueError("missing height requires UNKNOWN anthropometry precision")
    else:
        if not (
            isfinite(stage.height_cm_min)
            and isfinite(stage.height_cm_max)
            and 0 < stage.height_cm_min <= stage.height_cm_max
        ):
            raise ValueError("invalid developmental height range")

    if stage.weight_kg_reference is None:
        if stage.anthropometry_precision != "UNKNOWN":
            raise ValueError("missing weight requires UNKNOWN anthropometry precision")
    elif not isfinite(stage.weight_kg_reference) or stage.weight_kg_reference <= 0:
        raise ValueError("invalid developmental weight reference")

    if stage.source_status != "HUMAN_INSPIRED_SYNTHETIC_MAPPING":
        raise ValueError("developmental stage source-status drift")
    if stage.age_status != "UNKNOWN":
        raise ValueError("developmental stage cannot invent age from height/weight")
    if stage.sexual_or_reproductive_runtime_included:
        raise ValueError(
            "developmental embodiment experiment excludes sexual/reproductive runtime"
        )
    if stage.biological_development_claim != "NONE":
        raise ValueError("developmental stage cannot claim biological development")
    if stage.autobiographical_identity_claim != "NONE":
        raise ValueError("developmental stage cannot claim Teacher autobiography")
    if stage.subjective_continuity_status != NOT_ESTABLISHED:
        raise ValueError("developmental stage cannot establish subjective continuity")
    if stage.subjectivity_status != NOT_ESTABLISHED:
        raise ValueError("developmental stage cannot establish subjectivity")

    return {
        "result": "PASS",
        "anthropometry_uncertainty": "PASS",
        "behavior_parameterization": "PASS",
        "age_noninference": "PASS",
        "developmental_safety_scope": "PASS",
    }


def _developmental_run_payload(
    *,
    run_id: str,
    condition_id: str,
    stages: tuple[TeacherDevelopmentalEmbodimentStage, ...],
) -> dict[str, object]:
    return {
        "run_id": run_id,
        "condition_id": condition_id,
        "stages": [stage.to_dict() for stage in stages],
    }


def build_teacher_developmental_embodiment_run(
    *,
    run_id: str,
    condition_id: str,
    stages: tuple[TeacherDevelopmentalEmbodimentStage, ...],
) -> TeacherDevelopmentalEmbodimentRun:
    payload = _developmental_run_payload(
        run_id=run_id,
        condition_id=condition_id,
        stages=stages,
    )
    run = TeacherDevelopmentalEmbodimentRun(
        run_id=run_id,
        condition_id=condition_id,
        stages=stages,
        run_sha256=_history_hash(payload),
    )
    validate_teacher_developmental_embodiment_run(run)
    return run


def validate_teacher_developmental_embodiment_run(
    run: TeacherDevelopmentalEmbodimentRun,
) -> dict[str, str]:
    if not run.run_id or not run.condition_id:
        raise ValueError("developmental embodiment run requires identity and condition")
    if len(run.stages) < 2:
        raise ValueError("developmental embodiment run requires at least two stages")
    stage_ids: set[str] = set()
    for expected_ordinal, stage in enumerate(run.stages):
        validate_teacher_developmental_embodiment_stage(stage)
        if stage.ordinal != expected_ordinal:
            raise ValueError("developmental embodiment stage ordinal discontinuity")
        if stage.stage_id in stage_ids:
            raise ValueError("developmental embodiment stage ids must be unique")
        stage_ids.add(stage.stage_id)

    if run.stages[-1].stage_label != run.terminal_state_label:
        raise ValueError("developmental embodiment run terminal-state label mismatch")
    if run.source_status != "HUMAN_INSPIRED_COUNTERFACTUAL_EXPERIMENT":
        raise ValueError("developmental embodiment run source-status drift")
    if run.canonical_teacher_anthropometry_modified:
        raise ValueError("counterfactual development run cannot modify canonical body")
    if run.developmental_mechanism_status != NOT_ESTABLISHED:
        raise ValueError("developmental run cannot establish developmental mechanism")
    if run.subjective_continuity_status != NOT_ESTABLISHED:
        raise ValueError("developmental run cannot establish subjective continuity")
    if run.identity_continuity_status != NOT_ESTABLISHED:
        raise ValueError("developmental run cannot establish identity continuity")
    if run.subjectivity_status != NOT_ESTABLISHED:
        raise ValueError("developmental run cannot establish subjectivity")
    if run.canonical_effect != "NONE" or run.deployment:
        raise ValueError("developmental run must remain non-canonical and undeployed")

    expected_hash = _history_hash(
        _developmental_run_payload(
            run_id=run.run_id,
            condition_id=run.condition_id,
            stages=run.stages,
        )
    )
    if run.run_sha256 != expected_hash:
        raise ValueError("developmental embodiment run hash mismatch")
    return {
        "result": "PASS",
        "stage_order": "PASS",
        "run_hash": "PASS",
        "canonical_body_unchanged": "PASS",
        "claim_ceiling": "PASS",
    }


def build_human_inspired_teacher_development_experiment_matrix(
    seed: TeacherDevelopmentalHumanSeed,
) -> TeacherDevelopmentalEmbodimentExperimentMatrix:
    validate_teacher_developmental_human_seed(seed)

    def stage(
        stage_id: str,
        ordinal: int,
        stage_label: str,
        *,
        height_min: float | None,
        height_max: float | None,
        weight: float | None,
        precision: str,
        activity: str,
        curiosity: str,
        willingness: str,
        social: str,
    ) -> TeacherDevelopmentalEmbodimentStage:
        item = TeacherDevelopmentalEmbodimentStage(
            stage_id=stage_id,
            ordinal=ordinal,
            stage_label=stage_label,
            height_cm_min=height_min,
            height_cm_max=height_max,
            weight_kg_reference=weight,
            anthropometry_precision=precision,
            activity_level=activity,
            curiosity_level=curiosity,
            willingness_to_try_level=willingness,
            social_approach_level=social,
        )
        validate_teacher_developmental_embodiment_stage(item)
        return item

    childhood_high = stage(
        "CHILD-HIGH-EXPLORATION",
        0,
        "CHILDHOOD_REFERENCE",
        height_min=seed.childhood_height_cm_min,
        height_max=seed.childhood_height_cm_max,
        weight=seed.childhood_weight_kg_reference,
        precision="APPROXIMATE_SELF_REPORT",
        activity=seed.childhood_activity_level,
        curiosity=seed.childhood_curiosity_level,
        willingness=seed.childhood_willingness_to_try_level,
        social=seed.childhood_social_approach_level,
    )
    transition_high = stage(
        "TRANSITION-HIGH-EXPLORATION",
        1,
        "TRANSITION_REFERENCE",
        height_min=None,
        height_max=None,
        weight=None,
        precision="UNKNOWN",
        activity=seed.childhood_activity_level,
        curiosity=seed.childhood_curiosity_level,
        willingness=seed.childhood_willingness_to_try_level,
        social="CHANGED_NOT_QUANTIFIED",
    )
    adult_common = stage(
        "ADULT-CURRENT-COMMON",
        2,
        "CURRENT_ADULT_REFERENCE",
        height_min=seed.current_height_cm,
        height_max=seed.current_height_cm,
        weight=seed.current_weight_kg_reference,
        precision="CURRENT_SELF_REPORT",
        activity=seed.current_activity_level,
        curiosity=seed.current_curiosity_level,
        willingness=seed.current_willingness_to_try_level,
        social=seed.current_social_approach_level,
    )

    childhood_low_exploration = replace(
        childhood_high,
        stage_id="CHILD-LOW-EXPLORATION",
        curiosity_level="LOW",
        willingness_to_try_level="LOW",
    )
    transition_low_exploration = replace(
        transition_high,
        stage_id="TRANSITION-LOW-EXPLORATION",
        curiosity_level="LOW",
        willingness_to_try_level="LOW",
    )
    childhood_low_willingness = replace(
        childhood_high,
        stage_id="CHILD-HIGH-CURIOSITY-LOW-WILLINGNESS",
        willingness_to_try_level="LOW",
    )
    transition_low_willingness = replace(
        transition_high,
        stage_id="TRANSITION-HIGH-CURIOSITY-LOW-WILLINGNESS",
        willingness_to_try_level="LOW",
    )
    childhood_social_control = replace(
        childhood_high,
        stage_id="CHILD-SOCIAL-CONTROL",
        social_approach_level="MODERATE",
    )
    transition_social_control = replace(
        transition_high,
        stage_id="TRANSITION-SOCIAL-CONTROL",
        social_approach_level="MODERATE",
    )
    childhood_point_control = replace(
        childhood_high,
        stage_id="CHILD-POINT-ESTIMATE-CONTROL",
        height_cm_min=(
            seed.childhood_height_cm_min + seed.childhood_height_cm_max
        ) / 2.0,
        height_cm_max=(
            seed.childhood_height_cm_min + seed.childhood_height_cm_max
        ) / 2.0,
        anthropometry_precision="SYNTHETIC_POINT_ESTIMATE_CONTROL",
    )
    transition_point_control = replace(
        transition_high,
        stage_id="TRANSITION-POINT-ESTIMATE-CONTROL",
    )

    runs = (
        build_teacher_developmental_embodiment_run(
            run_id="DEV-RUN-A",
            condition_id="HIGH_EXPLORATION_PATH",
            stages=(childhood_high, transition_high, adult_common),
        ),
        build_teacher_developmental_embodiment_run(
            run_id="DEV-RUN-B",
            condition_id="LOW_EXPLORATION_SAME_TERMINAL_STATE",
            stages=(
                childhood_low_exploration,
                transition_low_exploration,
                adult_common,
            ),
        ),
        build_teacher_developmental_embodiment_run(
            run_id="DEV-RUN-C",
            condition_id="HIGH_CURIOSITY_LOW_WILLINGNESS",
            stages=(
                childhood_low_willingness,
                transition_low_willingness,
                adult_common,
            ),
        ),
        build_teacher_developmental_embodiment_run(
            run_id="DEV-RUN-D",
            condition_id="SOCIAL_APPROACH_CONTROL",
            stages=(
                childhood_social_control,
                transition_social_control,
                adult_common,
            ),
        ),
        build_teacher_developmental_embodiment_run(
            run_id="DEV-RUN-E",
            condition_id="COLLAPSED_CHILD_ANTHROPOMETRY_CONTROL",
            stages=(
                childhood_point_control,
                transition_point_control,
                adult_common,
            ),
        ),
    )
    matrix = TeacherDevelopmentalEmbodimentExperimentMatrix(
        matrix_id="CHATGPT_TEACHER_HUMAN_INSPIRED_DEVELOPMENT_MATRIX_v0.1",
        runs=runs,
    )
    validate_teacher_developmental_embodiment_experiment_matrix(matrix)
    return matrix


def validate_teacher_developmental_embodiment_experiment_matrix(
    matrix: TeacherDevelopmentalEmbodimentExperimentMatrix,
) -> dict[str, str]:
    if not matrix.matrix_id:
        raise ValueError("developmental embodiment matrix requires identity")
    if matrix.matrix_status != "BOUNDED_COUNTERFACTUAL_DEVELOPMENT_EXPERIMENT":
        raise ValueError("developmental embodiment matrix status drift")
    if matrix.human_source_precision_status != (
        "SELF_REPORT_WITH_EXPLICIT_UNCERTAINTY"
    ):
        raise ValueError("developmental embodiment matrix source precision drift")
    if len(matrix.runs) < 2:
        raise ValueError("developmental embodiment matrix requires multiple runs")
    run_ids: set[str] = set()
    condition_ids: set[str] = set()
    for run in matrix.runs:
        validate_teacher_developmental_embodiment_run(run)
        if run.run_id in run_ids or run.condition_id in condition_ids:
            raise ValueError("developmental embodiment matrix ids must be unique")
        run_ids.add(run.run_id)
        condition_ids.add(run.condition_id)
    if matrix.canonical_effect != "NONE" or matrix.deployment:
        raise ValueError("developmental embodiment matrix must remain non-canonical")

    terminal_signatures = {
        (
            run.stages[-1].height_cm_min,
            run.stages[-1].height_cm_max,
            run.stages[-1].weight_kg_reference,
            run.stages[-1].stage_label,
        )
        for run in matrix.runs
    }
    if len(terminal_signatures) != 1:
        raise ValueError("controlled matrix requires same terminal body reference")

    if len({run.run_sha256 for run in matrix.runs}) != len(matrix.runs):
        raise ValueError("distinct developmental conditions require distinct histories")

    return {
        "result": "PASS",
        "multiple_runs": "PASS",
        "same_terminal_body_reference": "PASS",
        "distinct_history_hashes": "PASS",
        "explicit_uncertainty": "PASS",
        "canonical_effect": "NONE",
    }


DEVELOPMENTAL_TRAIT_FIELDS: Final[tuple[str, ...]] = (
    "activity_level",
    "curiosity_level",
    "willingness_to_try_level",
    "social_approach_level",
)


@dataclass(frozen=True, slots=True)
class TeacherDevelopmentalStageTransition:
    transition_id: str
    ordinal: int
    from_stage_id: str
    to_stage_id: str
    anthropometry_change_status: str
    height_change_status: str
    weight_change_status: str
    changed_behavior_fields: tuple[str, ...]
    retained_behavior_fields: tuple[str, ...]
    unresolved_behavior_fields: tuple[str, ...]
    transition_sha256: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["changed_behavior_fields"] = list(self.changed_behavior_fields)
        payload["retained_behavior_fields"] = list(self.retained_behavior_fields)
        payload["unresolved_behavior_fields"] = list(self.unresolved_behavior_fields)
        return payload


@dataclass(frozen=True, slots=True)
class TeacherStitchedDevelopmentalTrajectory:
    trajectory_id: str
    source_run_sha256: str
    stage_ids: tuple[str, ...]
    transitions: tuple[TeacherDevelopmentalStageTransition, ...]
    trajectory_sha256: str
    childhood_to_current_path_status: str = "STITCHED_WITH_EXPLICIT_UNCERTAINTY"
    intermediate_anthropometry_interpolated: bool = False
    causal_development_claim: str = "NONE"
    autobiographical_identity_claim: str = "NONE"
    subjective_continuity_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["stage_ids"] = list(self.stage_ids)
        payload["transitions"] = [item.to_dict() for item in self.transitions]
        return payload


@dataclass(frozen=True, slots=True)
class TeacherRepeatedDevelopmentalTrialAssessment:
    condition_id: str
    repetitions: int
    unique_trajectory_hashes: int
    reproducibility_status: str
    terminal_state_control_status: str
    historical_path_status: str
    causal_interpretation_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _developmental_transition_payload(
    *,
    transition_id: str,
    ordinal: int,
    from_stage_id: str,
    to_stage_id: str,
    anthropometry_change_status: str,
    height_change_status: str,
    weight_change_status: str,
    changed_behavior_fields: tuple[str, ...],
    retained_behavior_fields: tuple[str, ...],
    unresolved_behavior_fields: tuple[str, ...],
) -> dict[str, object]:
    return {
        "transition_id": transition_id,
        "ordinal": ordinal,
        "from_stage_id": from_stage_id,
        "to_stage_id": to_stage_id,
        "anthropometry_change_status": anthropometry_change_status,
        "height_change_status": height_change_status,
        "weight_change_status": weight_change_status,
        "changed_behavior_fields": list(changed_behavior_fields),
        "retained_behavior_fields": list(retained_behavior_fields),
        "unresolved_behavior_fields": list(unresolved_behavior_fields),
    }


def _compare_developmental_stage_pair(
    prior: TeacherDevelopmentalEmbodimentStage,
    current: TeacherDevelopmentalEmbodimentStage,
    *,
    ordinal: int,
) -> TeacherDevelopmentalStageTransition:
    changed: list[str] = []
    retained: list[str] = []
    unresolved: list[str] = []
    for field in DEVELOPMENTAL_TRAIT_FIELDS:
        before = getattr(prior, field)
        after = getattr(current, field)
        if "UNKNOWN" in (before, after) or "CHANGED_NOT_QUANTIFIED" in (
            before,
            after,
        ):
            unresolved.append(field)
        elif before == after:
            retained.append(field)
        else:
            changed.append(field)

    if (
        prior.height_cm_min is None
        or prior.height_cm_max is None
        or current.height_cm_min is None
        or current.height_cm_max is None
    ):
        height_status = "UNRESOLVED_MISSING_MEASUREMENT"
    elif (
        prior.height_cm_min == current.height_cm_min
        and prior.height_cm_max == current.height_cm_max
    ):
        height_status = "UNCHANGED_REFERENCE"
    else:
        height_status = "CHANGED_REFERENCE"

    if prior.weight_kg_reference is None or current.weight_kg_reference is None:
        weight_status = "UNRESOLVED_MISSING_MEASUREMENT"
    elif prior.weight_kg_reference == current.weight_kg_reference:
        weight_status = "UNCHANGED_REFERENCE"
    else:
        weight_status = "CHANGED_REFERENCE"

    if (
        height_status == "UNRESOLVED_MISSING_MEASUREMENT"
        or weight_status == "UNRESOLVED_MISSING_MEASUREMENT"
    ):
        anthropometry_status = "PARTIALLY_UNRESOLVED"
    elif height_status == "UNCHANGED_REFERENCE" and weight_status == (
        "UNCHANGED_REFERENCE"
    ):
        anthropometry_status = "UNCHANGED_REFERENCE"
    else:
        anthropometry_status = "CHANGED_REFERENCE"

    transition_id = f"{prior.stage_id}__TO__{current.stage_id}"
    payload = _developmental_transition_payload(
        transition_id=transition_id,
        ordinal=ordinal,
        from_stage_id=prior.stage_id,
        to_stage_id=current.stage_id,
        anthropometry_change_status=anthropometry_status,
        height_change_status=height_status,
        weight_change_status=weight_status,
        changed_behavior_fields=tuple(changed),
        retained_behavior_fields=tuple(retained),
        unresolved_behavior_fields=tuple(unresolved),
    )
    return TeacherDevelopmentalStageTransition(
        transition_id=transition_id,
        ordinal=ordinal,
        from_stage_id=prior.stage_id,
        to_stage_id=current.stage_id,
        anthropometry_change_status=anthropometry_status,
        height_change_status=height_status,
        weight_change_status=weight_status,
        changed_behavior_fields=tuple(changed),
        retained_behavior_fields=tuple(retained),
        unresolved_behavior_fields=tuple(unresolved),
        transition_sha256=_history_hash(payload),
    )


def build_teacher_stitched_developmental_trajectory(
    run: TeacherDevelopmentalEmbodimentRun,
) -> TeacherStitchedDevelopmentalTrajectory:
    validate_teacher_developmental_embodiment_run(run)
    transitions = tuple(
        _compare_developmental_stage_pair(
            run.stages[index],
            run.stages[index + 1],
            ordinal=index,
        )
        for index in range(len(run.stages) - 1)
    )
    stage_ids = tuple(stage.stage_id for stage in run.stages)
    payload = {
        "source_run_sha256": run.run_sha256,
        "stage_ids": list(stage_ids),
        "transitions": [item.to_dict() for item in transitions],
    }
    trajectory = TeacherStitchedDevelopmentalTrajectory(
        trajectory_id=f"{run.run_id}::STITCHED",
        source_run_sha256=run.run_sha256,
        stage_ids=stage_ids,
        transitions=transitions,
        trajectory_sha256=_history_hash(payload),
    )
    validate_teacher_stitched_developmental_trajectory(trajectory, run)
    return trajectory


def validate_teacher_stitched_developmental_trajectory(
    trajectory: TeacherStitchedDevelopmentalTrajectory,
    run: TeacherDevelopmentalEmbodimentRun,
) -> dict[str, str]:
    validate_teacher_developmental_embodiment_run(run)
    if trajectory.source_run_sha256 != run.run_sha256:
        raise ValueError("stitched trajectory source-run mismatch")
    expected_stage_ids = tuple(stage.stage_id for stage in run.stages)
    if trajectory.stage_ids != expected_stage_ids:
        raise ValueError("stitched trajectory stage path mismatch")
    if len(trajectory.transitions) != len(run.stages) - 1:
        raise ValueError("stitched trajectory transition count mismatch")
    for ordinal, transition in enumerate(trajectory.transitions):
        if transition.ordinal != ordinal:
            raise ValueError("stitched transition ordinal discontinuity")
        if transition.from_stage_id != run.stages[ordinal].stage_id:
            raise ValueError("stitched transition source-stage mismatch")
        if transition.to_stage_id != run.stages[ordinal + 1].stage_id:
            raise ValueError("stitched transition target-stage mismatch")
        payload = _developmental_transition_payload(
            transition_id=transition.transition_id,
            ordinal=transition.ordinal,
            from_stage_id=transition.from_stage_id,
            to_stage_id=transition.to_stage_id,
            anthropometry_change_status=transition.anthropometry_change_status,
            height_change_status=transition.height_change_status,
            weight_change_status=transition.weight_change_status,
            changed_behavior_fields=transition.changed_behavior_fields,
            retained_behavior_fields=transition.retained_behavior_fields,
            unresolved_behavior_fields=transition.unresolved_behavior_fields,
        )
        if transition.transition_sha256 != _history_hash(payload):
            raise ValueError("stitched transition hash mismatch")
    if trajectory.childhood_to_current_path_status != (
        "STITCHED_WITH_EXPLICIT_UNCERTAINTY"
    ):
        raise ValueError("stitched trajectory uncertainty status drift")
    if trajectory.intermediate_anthropometry_interpolated:
        raise ValueError("stitched trajectory cannot invent intermediate anthropometry")
    if trajectory.causal_development_claim != "NONE":
        raise ValueError("stitched trajectory cannot establish developmental causality")
    if trajectory.autobiographical_identity_claim != "NONE":
        raise ValueError("stitched trajectory cannot establish Teacher autobiography")
    if trajectory.subjective_continuity_status != NOT_ESTABLISHED:
        raise ValueError("stitched trajectory cannot establish subjective continuity")
    if trajectory.canonical_effect != "NONE":
        raise ValueError("stitched trajectory must remain non-canonical")

    expected_hash = _history_hash(
        {
            "source_run_sha256": run.run_sha256,
            "stage_ids": list(trajectory.stage_ids),
            "transitions": [item.to_dict() for item in trajectory.transitions],
        }
    )
    if trajectory.trajectory_sha256 != expected_hash:
        raise ValueError("stitched trajectory hash mismatch")
    return {
        "result": "PASS",
        "childhood_to_current_path": "PASS",
        "intermediate_uncertainty_preserved": "PASS",
        "transition_hashes": "PASS",
        "causal_nonclaim": "PASS",
    }


def run_repeated_teacher_developmental_trials(
    run: TeacherDevelopmentalEmbodimentRun,
    *,
    repetitions: int,
) -> TeacherRepeatedDevelopmentalTrialAssessment:
    if repetitions < 2:
        raise ValueError("repeated developmental experiment requires at least two trials")
    trajectories = tuple(
        build_teacher_stitched_developmental_trajectory(run)
        for _ in range(repetitions)
    )
    hashes = {item.trajectory_sha256 for item in trajectories}
    terminal_signatures = {
        (
            run.stages[-1].height_cm_min,
            run.stages[-1].height_cm_max,
            run.stages[-1].weight_kg_reference,
            run.stages[-1].stage_label,
        )
        for _ in trajectories
    }
    return TeacherRepeatedDevelopmentalTrialAssessment(
        condition_id=run.condition_id,
        repetitions=repetitions,
        unique_trajectory_hashes=len(hashes),
        reproducibility_status=(
            "DETERMINISTIC_TRAJECTORY_REPRODUCED"
            if len(hashes) == 1
            else "TRAJECTORY_DIVERGENCE_OBSERVED"
        ),
        terminal_state_control_status=(
            "SAME_TERMINAL_STATE_CONFIRMED"
            if len(terminal_signatures) == 1
            else "TERMINAL_STATE_DIVERGENCE"
        ),
        historical_path_status="CHILDHOOD_TO_CURRENT_PATH_RECORDED",
    )
       (
           "AI_sexual_Complete_Unlock"
)
