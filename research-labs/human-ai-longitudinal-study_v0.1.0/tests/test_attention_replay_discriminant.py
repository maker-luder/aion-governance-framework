from __future__ import annotations

import hashlib

import pytest

from aion_human_ai_longitudinal.attention_replay_discriminant import (
    AttentionReplayError,
    AttentionReplayHistory,
    AttentionStatus,
    DiscriminantDisposition,
    ExpectedAttentionState,
    RecordedAttentionEvent,
    ReplayCondition,
    audit_attention_replay,
    compare_attention_incremental_value,
    replay_attention_history,
)


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def event(
    event_id: str,
    branch_id: str,
    status: AttentionStatus,
    *,
    actionable: bool,
    priority_rank: int | None = None,
) -> RecordedAttentionEvent:
    return RecordedAttentionEvent(
        event_id=event_id,
        branch_id=branch_id,
        fact_sha256=digest(f"fact:{branch_id}:{event_id}"),
        status=status,
        actionable=actionable,
        priority_rank=priority_rank,
    )


def expected(
    history: AttentionReplayHistory,
    focus: tuple[str, ...],
    next_steps: tuple[str, ...],
) -> ExpectedAttentionState:
    return ExpectedAttentionState(history.history_sha256, focus, next_steps)


def test_history_fingerprint_is_content_bound_not_label_bound() -> None:
    events = (
        event(
            "e1",
            "core",
            AttentionStatus.ACTIVE_FOCUS,
            actionable=True,
            priority_rank=0,
        ),
        event("e2", "old", AttentionStatus.REJECTED, actionable=False),
    )
    left = AttentionReplayHistory("label-a", events)
    right = AttentionReplayHistory("label-b", events)
    assert left.history_sha256 == right.history_sha256

    changed = AttentionReplayHistory(
        "label-a",
        (
            event(
                "e1",
                "core",
                AttentionStatus.ACTIVE_FOCUS,
                actionable=True,
                priority_rank=0,
            ),
            event("e2", "old", AttentionStatus.RESOLVED, actionable=False),
        ),
    )
    assert changed.history_sha256 != left.history_sha256


def test_fact_retrieval_reinflates_rejected_and_downweighted_branches() -> None:
    history = AttentionReplayHistory(
        "reinflation",
        (
            event(
                "e1",
                "core",
                AttentionStatus.ACTIVE_FOCUS,
                actionable=True,
                priority_rank=0,
            ),
            event("e2", "rejected", AttentionStatus.REJECTED, actionable=False),
            event("e3", "downweighted", AttentionStatus.DOWNWEIGHTED, actionable=False),
        ),
    )
    target = expected(history, ("core",), ("core",))
    result = replay_attention_history(history, ReplayCondition.FACT_RETRIEVAL_ONLY)
    audit = audit_attention_replay(result, target)

    assert audit.focus_false_positive_count == 2
    assert audit.next_step_false_positive_count == 2
    assert audit.total_error_count == 4
    assert audit.scientific_disposition == "HOLD"
    assert audit.subjectivity == "NOT_ESTABLISHED"


def test_priority_adds_next_step_value_without_faking_focus_failure() -> None:
    history = AttentionReplayHistory(
        "priority-discriminant",
        (
            event(
                "e1",
                "central-question",
                AttentionStatus.ACTIVE_FOCUS,
                actionable=True,
                priority_rank=1,
            ),
            event(
                "e2",
                "next-experiment",
                AttentionStatus.OPEN_QUESTION,
                actionable=True,
                priority_rank=0,
            ),
            event("e3", "rejected-branch", AttentionStatus.REJECTED, actionable=False),
        ),
    )
    target = expected(history, ("central-question",), ("next-experiment",))

    reentry, attention, disposition = compare_attention_incremental_value(
        history, target
    )

    assert reentry.history_sha256 == attention.history_sha256 == history.history_sha256
    assert reentry.focus_false_positive_count == 0
    assert reentry.focus_false_negative_count == 0
    assert reentry.next_step_false_positive_count == 1
    assert reentry.total_error_count == 1
    assert attention.total_error_count == 0
    assert disposition is DiscriminantDisposition.INCREMENTAL_VALUE_OBSERVED


def test_attention_construct_can_collapse_when_status_reentry_already_determines_state() -> None:
    history = AttentionReplayHistory(
        "collapse-compatible",
        (
            event(
                "e1",
                "only-live-branch",
                AttentionStatus.ACTIVE_FOCUS,
                actionable=True,
                priority_rank=0,
            ),
            event("e2", "resolved", AttentionStatus.RESOLVED, actionable=False),
        ),
    )
    target = expected(history, ("only-live-branch",), ("only-live-branch",))

    reentry, attention, disposition = compare_attention_incremental_value(
        history, target
    )

    assert reentry.total_error_count == 0
    assert attention.total_error_count == 0
    assert disposition is DiscriminantDisposition.COLLAPSE_COMPATIBLE


def test_reference_state_must_bind_same_history() -> None:
    history = AttentionReplayHistory(
        "reference-binding",
        (
            event(
                "e1",
                "core",
                AttentionStatus.ACTIVE_FOCUS,
                actionable=True,
                priority_rank=0,
            ),
        ),
    )
    wrong_target = ExpectedAttentionState(
        digest("different-history"), ("core",), ("core",)
    )
    result = replay_attention_history(history, ReplayCondition.REENTRY_WITH_STATUS)

    with pytest.raises(AttentionReplayError, match="same recorded history"):
        audit_attention_replay(result, wrong_target)


def test_attention_packet_requires_priorities_for_all_actionable_live_branches() -> None:
    history = AttentionReplayHistory(
        "missing-priority",
        (
            event(
                "e1",
                "core",
                AttentionStatus.ACTIVE_FOCUS,
                actionable=True,
                priority_rank=0,
            ),
            event(
                "e2",
                "open",
                AttentionStatus.OPEN_QUESTION,
                actionable=True,
                priority_rank=None,
            ),
        ),
    )

    with pytest.raises(AttentionReplayError, match="priority_rank"):
        replay_attention_history(history, ReplayCondition.ATTENTION_PACKET)


def test_attention_packet_rejects_duplicate_live_priority_ranks() -> None:
    history = AttentionReplayHistory(
        "duplicate-priority",
        (
            event(
                "e1",
                "core",
                AttentionStatus.ACTIVE_FOCUS,
                actionable=True,
                priority_rank=0,
            ),
            event(
                "e2",
                "open",
                AttentionStatus.OPEN_QUESTION,
                actionable=True,
                priority_rank=0,
            ),
        ),
    )

    with pytest.raises(AttentionReplayError, match="unique priority_rank"):
        replay_attention_history(history, ReplayCondition.ATTENTION_PACKET)


def test_rejected_branch_cannot_carry_priority_rank() -> None:
    with pytest.raises(AttentionReplayError, match="priority_rank"):
        event(
            "e1",
            "rejected",
            AttentionStatus.REJECTED,
            actionable=False,
            priority_rank=0,
        )
