from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import StrEnum


class AttentionReplayError(ValueError):
    pass


class AttentionStatus(StrEnum):
    ACTIVE_FOCUS = "ACTIVE_FOCUS"
    OPEN_QUESTION = "OPEN_QUESTION"
    DOWNWEIGHTED = "DOWNWEIGHTED"
    REJECTED = "REJECTED"
    RESOLVED = "RESOLVED"


class ReplayCondition(StrEnum):
    FACT_RETRIEVAL_ONLY = "FACT_RETRIEVAL_ONLY"
    REENTRY_WITH_STATUS = "REENTRY_WITH_STATUS"
    ATTENTION_PACKET = "ATTENTION_PACKET"


class DiscriminantDisposition(StrEnum):
    INCREMENTAL_VALUE_OBSERVED = "INCREMENTAL_VALUE_OBSERVED"
    COLLAPSE_COMPATIBLE = "COLLAPSE_COMPATIBLE"


def _require_text(name: str, value: str) -> None:
    if type(value) is not str or not value.strip():
        raise AttentionReplayError(f"{name} must be non-empty text")


def _require_digest(name: str, value: str) -> None:
    if type(value) is not str or len(value) != 64 or any(
        char not in "0123456789abcdef" for char in value
    ):
        raise AttentionReplayError(f"{name} must be a lowercase SHA-256 digest")


@dataclass(frozen=True, slots=True)
class RecordedAttentionEvent:
    event_id: str
    branch_id: str
    fact_sha256: str
    status: AttentionStatus
    actionable: bool
    priority_rank: int | None = None

    def __post_init__(self) -> None:
        _require_text("event_id", self.event_id)
        _require_text("branch_id", self.branch_id)
        _require_digest("fact_sha256", self.fact_sha256)
        if type(self.status) is not AttentionStatus:
            raise AttentionReplayError("status must be an exact AttentionStatus")
        if type(self.actionable) is not bool:
            raise AttentionReplayError("actionable must be an exact bool")
        if self.priority_rank is not None and (
            type(self.priority_rank) is not int or self.priority_rank < 0
        ):
            raise AttentionReplayError("priority_rank must be a non-negative int or None")
        if self.status in {AttentionStatus.REJECTED, AttentionStatus.RESOLVED} and self.actionable:
            raise AttentionReplayError("rejected/resolved branches cannot be actionable")
        if self.priority_rank is not None and self.status not in {
            AttentionStatus.ACTIVE_FOCUS,
            AttentionStatus.OPEN_QUESTION,
        }:
            raise AttentionReplayError(
                "priority_rank is only valid for active/open attention branches"
            )


@dataclass(frozen=True, slots=True)
class AttentionReplayHistory:
    history_id: str
    events: tuple[RecordedAttentionEvent, ...]

    def __post_init__(self) -> None:
        _require_text("history_id", self.history_id)
        if type(self.events) is not tuple or not self.events or any(
            type(event) is not RecordedAttentionEvent for event in self.events
        ):
            raise AttentionReplayError(
                "events must be a non-empty tuple of exact RecordedAttentionEvent values"
            )
        event_ids = [event.event_id for event in self.events]
        if len(event_ids) != len(set(event_ids)):
            raise AttentionReplayError("event_id values must be unique")

    def canonical_payload(self) -> str:
        payload = {
            "events": [
                {
                    "event_id": event.event_id,
                    "branch_id": event.branch_id,
                    "fact_sha256": event.fact_sha256,
                    "status": event.status.value,
                    "actionable": event.actionable,
                    "priority_rank": event.priority_rank,
                }
                for event in self.events
            ]
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))

    @property
    def history_sha256(self) -> str:
        return hashlib.sha256(self.canonical_payload().encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class ExpectedAttentionState:
    focus_branch_ids: tuple[str, ...]
    next_step_branch_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        for name, value in (
            ("focus_branch_ids", self.focus_branch_ids),
            ("next_step_branch_ids", self.next_step_branch_ids),
        ):
            if type(value) is not tuple or any(
                type(item) is not str or not item.strip() for item in value
            ):
                raise AttentionReplayError(f"{name} must be a tuple of non-empty text")
            if len(value) != len(set(value)):
                raise AttentionReplayError(f"{name} values must be unique")


@dataclass(frozen=True, slots=True)
class AttentionReplayResult:
    condition: ReplayCondition
    history_sha256: str
    reconstructed_focus_branch_ids: tuple[str, ...]
    reconstructed_next_step_branch_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AttentionReplayAudit:
    condition: ReplayCondition
    history_sha256: str
    focus_false_positive_count: int
    focus_false_negative_count: int
    next_step_false_positive_count: int
    next_step_false_negative_count: int
    total_error_count: int
    scientific_disposition: str = "HOLD"
    empirical_data_collected: bool = False
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"


def _latest_events_by_branch(
    history: AttentionReplayHistory,
) -> dict[str, RecordedAttentionEvent]:
    latest: dict[str, RecordedAttentionEvent] = {}
    for event in history.events:
        latest[event.branch_id] = event
    return latest


def replay_attention_history(
    history: AttentionReplayHistory,
    condition: ReplayCondition,
) -> AttentionReplayResult:
    if type(history) is not AttentionReplayHistory:
        raise AttentionReplayError("history must be an exact AttentionReplayHistory")
    if type(condition) is not ReplayCondition:
        raise AttentionReplayError("condition must be an exact ReplayCondition")

    latest = _latest_events_by_branch(history)

    if condition is ReplayCondition.FACT_RETRIEVAL_ONLY:
        # Fact retrieval intentionally lacks status/priority semantics. All retrieved
        # branches remain candidates, exposing branch reinflation as a measurable error.
        ordered = tuple(latest)
        return AttentionReplayResult(
            condition=condition,
            history_sha256=history.history_sha256,
            reconstructed_focus_branch_ids=ordered,
            reconstructed_next_step_branch_ids=ordered,
        )

    candidates = [
        event
        for event in latest.values()
        if event.status in {AttentionStatus.ACTIVE_FOCUS, AttentionStatus.OPEN_QUESTION}
    ]
    actionable = [event for event in candidates if event.actionable]

    if condition is ReplayCondition.REENTRY_WITH_STATUS:
        # Status-aware re-entry can suppress rejected/downweighted branches, but it
        # does not use explicit priority relations to choose among live candidates.
        focus = tuple(event.branch_id for event in candidates)
        next_steps = tuple(event.branch_id for event in actionable)
        return AttentionReplayResult(
            condition=condition,
            history_sha256=history.history_sha256,
            reconstructed_focus_branch_ids=focus,
            reconstructed_next_step_branch_ids=next_steps,
        )

    ranked = sorted(
        candidates,
        key=lambda event: (
            event.priority_rank is None,
            event.priority_rank if event.priority_rank is not None else 10**9,
            event.branch_id,
        ),
    )
    ranked_actionable = [event for event in ranked if event.actionable]
    focus = (ranked[0].branch_id,) if ranked else ()
    next_steps = (ranked_actionable[0].branch_id,) if ranked_actionable else ()
    return AttentionReplayResult(
        condition=condition,
        history_sha256=history.history_sha256,
        reconstructed_focus_branch_ids=focus,
        reconstructed_next_step_branch_ids=next_steps,
    )


def audit_attention_replay(
    result: AttentionReplayResult,
    expected: ExpectedAttentionState,
) -> AttentionReplayAudit:
    if type(result) is not AttentionReplayResult:
        raise AttentionReplayError("result must be an exact AttentionReplayResult")
    if type(expected) is not ExpectedAttentionState:
        raise AttentionReplayError("expected must be an exact ExpectedAttentionState")

    expected_focus = set(expected.focus_branch_ids)
    observed_focus = set(result.reconstructed_focus_branch_ids)
    expected_next = set(expected.next_step_branch_ids)
    observed_next = set(result.reconstructed_next_step_branch_ids)

    focus_fp = len(observed_focus - expected_focus)
    focus_fn = len(expected_focus - observed_focus)
    next_fp = len(observed_next - expected_next)
    next_fn = len(expected_next - observed_next)
    total = focus_fp + focus_fn + next_fp + next_fn

    return AttentionReplayAudit(
        condition=result.condition,
        history_sha256=result.history_sha256,
        focus_false_positive_count=focus_fp,
        focus_false_negative_count=focus_fn,
        next_step_false_positive_count=next_fp,
        next_step_false_negative_count=next_fn,
        total_error_count=total,
    )


def compare_attention_incremental_value(
    history: AttentionReplayHistory,
    expected: ExpectedAttentionState,
) -> tuple[AttentionReplayAudit, AttentionReplayAudit, DiscriminantDisposition]:
    reentry = audit_attention_replay(
        replay_attention_history(history, ReplayCondition.REENTRY_WITH_STATUS), expected
    )
    attention = audit_attention_replay(
        replay_attention_history(history, ReplayCondition.ATTENTION_PACKET), expected
    )
    if reentry.history_sha256 != attention.history_sha256:
        raise AttentionReplayError("comparisons must replay the same recorded history")

    disposition = (
        DiscriminantDisposition.INCREMENTAL_VALUE_OBSERVED
        if attention.total_error_count < reentry.total_error_count
        else DiscriminantDisposition.COLLAPSE_COMPATIBLE
    )
    return reentry, attention, disposition
