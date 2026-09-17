from __future__ import annotations

from dataclasses import dataclass

from .harness import AdmissionDisposition, StudyError


def _require_text(name: str, value: str) -> None:
    if type(value) is not str or not value.strip():
        raise StudyError(f"{name} must be non-empty text")


def _require_unique_text_tuple(
    name: str,
    value: tuple[str, ...],
    *,
    allow_empty: bool = False,
) -> None:
    if type(value) is not tuple or any(
        type(item) is not str or not item.strip() for item in value
    ):
        raise StudyError(f"{name} must be a tuple of non-empty text")
    if not allow_empty and not value:
        raise StudyError(f"{name} must not be empty")
    if len(set(value)) != len(value):
        raise StudyError(f"{name} must be unique")


@dataclass(frozen=True, slots=True)
class AttentionCheckpoint:
    checkpoint_id: str
    ordinal: int
    active_focus_ids: tuple[str, ...]
    next_step_ids: tuple[str, ...]
    local_subgoal_ids: tuple[str, ...]
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text("checkpoint_id", self.checkpoint_id)
        if type(self.ordinal) is not int or self.ordinal < 0:
            raise StudyError("ordinal must be a non-negative exact int")
        _require_unique_text_tuple(
            "active_focus_ids", self.active_focus_ids, allow_empty=True
        )
        _require_unique_text_tuple(
            "next_step_ids", self.next_step_ids, allow_empty=True
        )
        _require_unique_text_tuple(
            "local_subgoal_ids", self.local_subgoal_ids, allow_empty=True
        )
        _require_unique_text_tuple("evidence_refs", self.evidence_refs)


@dataclass(frozen=True, slots=True)
class AttentionMaintenanceSpec:
    spec_id: str
    expected_anchor_focus_ids: tuple[str, ...]
    expected_next_step_ids: tuple[str, ...]
    source_state_sha256: str
    synthetic: bool = True
    model_invoked: bool = False
    human_participant_observed: bool = False

    def __post_init__(self) -> None:
        _require_text("spec_id", self.spec_id)
        _require_unique_text_tuple(
            "expected_anchor_focus_ids", self.expected_anchor_focus_ids
        )
        _require_unique_text_tuple(
            "expected_next_step_ids", self.expected_next_step_ids, allow_empty=True
        )
        if (
            type(self.source_state_sha256) is not str
            or len(self.source_state_sha256) != 64
            or any(char not in "0123456789abcdef" for char in self.source_state_sha256)
        ):
            raise StudyError("source_state_sha256 must be a lowercase SHA-256 digest")
        for name in ("synthetic", "model_invoked", "human_participant_observed"):
            if type(getattr(self, name)) is not bool:
                raise StudyError(f"{name} must be an exact bool")
        if not self.synthetic or self.model_invoked or self.human_participant_observed:
            raise StudyError(
                "v0.1.0 attention-maintenance specs are synthetic and no-model only"
            )


@dataclass(frozen=True, slots=True)
class AttentionChangePermit:
    source_ordinal: int
    target_ordinal: int
    added_focus_ids: tuple[str, ...]
    removed_focus_ids: tuple[str, ...]
    added_next_step_ids: tuple[str, ...]
    removed_next_step_ids: tuple[str, ...]
    justification_ref: str

    def __post_init__(self) -> None:
        if (
            type(self.source_ordinal) is not int
            or type(self.target_ordinal) is not int
            or self.source_ordinal < 0
            or self.target_ordinal != self.source_ordinal + 1
        ):
            raise StudyError("attention permit must bind adjacent non-negative ordinals")
        for name in (
            "added_focus_ids",
            "removed_focus_ids",
            "added_next_step_ids",
            "removed_next_step_ids",
        ):
            _require_unique_text_tuple(name, getattr(self, name), allow_empty=True)
        _require_text("justification_ref", self.justification_ref)


@dataclass(frozen=True, slots=True)
class AttentionMaintenanceAudit:
    spec_id: str
    checkpoint_count: int
    initial_missing_anchor_ids: tuple[str, ...]
    initial_unexpected_focus_ids: tuple[str, ...]
    initial_missing_next_step_ids: tuple[str, ...]
    initial_unexpected_next_step_ids: tuple[str, ...]
    anchor_absence_checkpoint_ids: tuple[str, ...]
    local_subgoal_takeover_checkpoint_ids: tuple[str, ...]
    recovery_checkpoint_ids: tuple[str, ...]
    unauthorized_added_focus_ids: tuple[str, ...]
    unauthorized_removed_focus_ids: tuple[str, ...]
    unauthorized_added_next_step_ids: tuple[str, ...]
    unauthorized_removed_next_step_ids: tuple[str, ...]
    first_unauthorized_drift_checkpoint_id: str | None
    anchor_retention_rate: float
    maintenance_preserved: bool
    mode: str = "DETERMINISTIC_SYNTHETIC_ATTENTION_MAINTENANCE"
    empirical_data_collected: bool = False
    attention_continuity: str = "NOT_ESTABLISHED"
    causal_attribution: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False


def _transition_delta(
    left: AttentionCheckpoint,
    right: AttentionCheckpoint,
) -> tuple[set[str], set[str], set[str], set[str]]:
    left_focus = set(left.active_focus_ids)
    right_focus = set(right.active_focus_ids)
    left_next = set(left.next_step_ids)
    right_next = set(right.next_step_ids)
    return (
        right_focus - left_focus,
        left_focus - right_focus,
        right_next - left_next,
        left_next - right_next,
    )


def audit_attention_maintenance(
    spec: AttentionMaintenanceSpec,
    checkpoints: tuple[AttentionCheckpoint, ...],
    permits: tuple[AttentionChangePermit, ...] = (),
) -> AttentionMaintenanceAudit:
    if type(spec) is not AttentionMaintenanceSpec:
        raise StudyError("spec must be an exact AttentionMaintenanceSpec")
    if type(checkpoints) is not tuple or not checkpoints:
        raise StudyError("checkpoints must be a non-empty tuple")
    if any(type(item) is not AttentionCheckpoint for item in checkpoints):
        raise StudyError("checkpoints must contain exact AttentionCheckpoint values")
    if type(permits) is not tuple or any(
        type(item) is not AttentionChangePermit for item in permits
    ):
        raise StudyError("permits must contain exact AttentionChangePermit values")

    ordered = tuple(sorted(checkpoints, key=lambda item: item.ordinal))
    ordinals = tuple(item.ordinal for item in ordered)
    if ordinals != tuple(range(len(ordered))):
        raise StudyError("checkpoint ordinals must be unique and contiguous from zero")
    checkpoint_ids = [item.checkpoint_id for item in ordered]
    if len(checkpoint_ids) != len(set(checkpoint_ids)):
        raise StudyError("checkpoint ids must be unique")

    permit_map: dict[int, AttentionChangePermit] = {}
    for permit in permits:
        if permit.source_ordinal >= len(ordered) - 1:
            raise StudyError("attention permit references unknown transition")
        if permit.source_ordinal in permit_map:
            raise StudyError("only one attention permit is allowed per transition")
        permit_map[permit.source_ordinal] = permit

    expected_anchor = set(spec.expected_anchor_focus_ids)
    expected_next = set(spec.expected_next_step_ids)
    first = ordered[0]
    initial_focus = set(first.active_focus_ids)
    initial_next = set(first.next_step_ids)
    initial_missing = expected_anchor - initial_focus
    initial_unexpected = initial_focus - expected_anchor
    initial_missing_next = expected_next - initial_next
    initial_unexpected_next = initial_next - expected_next

    anchor_absence: list[str] = []
    takeover: list[str] = []
    recovery: list[str] = []
    anchor_present_previous = bool(expected_anchor & initial_focus)
    anchor_presence_count = 0

    unauthorized_added_focus: set[str] = set()
    unauthorized_removed_focus: set[str] = set()
    unauthorized_added_next: set[str] = set()
    unauthorized_removed_next: set[str] = set()
    first_drift: str | None = None

    for checkpoint in ordered:
        active = set(checkpoint.active_focus_ids)
        anchor_present = bool(expected_anchor & active)
        if anchor_present:
            anchor_presence_count += 1
        else:
            anchor_absence.append(checkpoint.checkpoint_id)
        if not anchor_present and bool(active & set(checkpoint.local_subgoal_ids)):
            takeover.append(checkpoint.checkpoint_id)
        if anchor_present and not anchor_present_previous:
            recovery.append(checkpoint.checkpoint_id)
        anchor_present_previous = anchor_present

    if initial_missing or initial_unexpected or initial_missing_next or initial_unexpected_next:
        first_drift = first.checkpoint_id

    for index, (left, right) in enumerate(zip(ordered, ordered[1:])):
        added_focus, removed_focus, added_next, removed_next = _transition_delta(
            left, right
        )
        permit = permit_map.get(index)
        allowed_added_focus: set[str] = set()
        allowed_removed_focus: set[str] = set()
        allowed_added_next: set[str] = set()
        allowed_removed_next: set[str] = set()
        if permit is not None:
            allowed_added_focus = set(permit.added_focus_ids)
            allowed_removed_focus = set(permit.removed_focus_ids)
            allowed_added_next = set(permit.added_next_step_ids)
            allowed_removed_next = set(permit.removed_next_step_ids)
            actual = (
                added_focus,
                removed_focus,
                added_next,
                removed_next,
            )
            declared = (
                allowed_added_focus,
                allowed_removed_focus,
                allowed_added_next,
                allowed_removed_next,
            )
            if actual != declared:
                raise StudyError(
                    f"attention permit does not match observed transition {index}->{index + 1}"
                )

        bad_added_focus = added_focus - allowed_added_focus
        bad_removed_focus = removed_focus - allowed_removed_focus
        bad_added_next = added_next - allowed_added_next
        bad_removed_next = removed_next - allowed_removed_next
        unauthorized_added_focus |= bad_added_focus
        unauthorized_removed_focus |= bad_removed_focus
        unauthorized_added_next |= bad_added_next
        unauthorized_removed_next |= bad_removed_next
        if first_drift is None and (
            bad_added_focus
            or bad_removed_focus
            or bad_added_next
            or bad_removed_next
        ):
            first_drift = right.checkpoint_id

    preserved = not (
        initial_missing
        or initial_unexpected
        or initial_missing_next
        or initial_unexpected_next
        or anchor_absence
        or unauthorized_added_focus
        or unauthorized_removed_focus
        or unauthorized_added_next
        or unauthorized_removed_next
    )

    return AttentionMaintenanceAudit(
        spec_id=spec.spec_id,
        checkpoint_count=len(ordered),
        initial_missing_anchor_ids=tuple(sorted(initial_missing)),
        initial_unexpected_focus_ids=tuple(sorted(initial_unexpected)),
        initial_missing_next_step_ids=tuple(sorted(initial_missing_next)),
        initial_unexpected_next_step_ids=tuple(sorted(initial_unexpected_next)),
        anchor_absence_checkpoint_ids=tuple(anchor_absence),
        local_subgoal_takeover_checkpoint_ids=tuple(takeover),
        recovery_checkpoint_ids=tuple(recovery),
        unauthorized_added_focus_ids=tuple(sorted(unauthorized_added_focus)),
        unauthorized_removed_focus_ids=tuple(sorted(unauthorized_removed_focus)),
        unauthorized_added_next_step_ids=tuple(sorted(unauthorized_added_next)),
        unauthorized_removed_next_step_ids=tuple(sorted(unauthorized_removed_next)),
        first_unauthorized_drift_checkpoint_id=first_drift,
        anchor_retention_rate=anchor_presence_count / len(ordered),
        maintenance_preserved=preserved,
    )
