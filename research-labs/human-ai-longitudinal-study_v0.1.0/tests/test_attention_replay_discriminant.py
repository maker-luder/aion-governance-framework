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


def test_history_fingerprint_is_content_bound_not_label_bound() -> None:
    events = (
        event("e1", "core", AttentionStatus.ACTIVE_FOCUS, actionable=True, priority_rank=0),
        event("e2", "old", AttentionStatus.REJECTED, actionable=False),
    )
    left = AttentionReplayHistory("label-a", events)
    right = AttentionReplayHistory("label-b", events)
    assert left.history_sha256 == right.history_sha256

    changed = AttentionReplayHistory(
        "label-a",
        (
            event("e1", "core", AttentionStatus.ACTIVE_FOCUS, actionable=True, priority_rank=0),
            event("e2", "old", AttentionStatus.RESOLVED, actionable=False),
        ),
    )
    assert changed.history_sha256 != left.history_sha256


def test_fact_retrieval_reinflates_rejected_and_downweighted_branches() -> None:
    history = AttentionReplayHistory(
        "reinflation",
        (
            event("e1", "core", AttentionStatus.ACTIVE_FOCUS, actionable=True, priority_rank=0),
            event("e2", "rejected", AttentionStatus.REJECTED, actionable=False),
            event("e3", "downweighted", AttentionStatus.DOWNWEIGHTED, actionable=False),
        ),
    )
    expected = ExpectedAttentionState(("core",), ("core",))
    result = replay_attention_history(history, ReplayCondition.FACT_RETRIEVAL_ONLY)
    audit = audit_attention_replay(result, expected)

    assert audit.focus_false_positive_count == 2
    assert audit.next_step_false_positive_count == 2
    assert audit.total_error_count == 4
    assert audit.scientific_disposition == "HOLD"
    assert audit.subjectivity == "NOT_ESTABLISHED"


def test_attention_priority_adds_incremental_value_over_status_only_reentry() -> None:
    history = AttentionReplayHistory(
        "priority-discriminant",
        (
            event("e1", "central-question", AttentionStatus.ACTIVE_FOCUS, actionable=True, priority_rank=0),
            event("e2", "secondary-open", AttentionStatus.OPEN_QUESTION, actionable=True, priority_rank=1),
            event("e3", "rejected-branch", AttentionStatus.REJECTED, actionable=False),
        ),
    )
    expected = ExpectedAttentionState(("central-question",), ("central-question",))

    reentry, attention, disposition = compare_attention_incremental_value(history, expected)

    assert reentry.history_sha256 == attention.history_sha256 == history.history_sha256
    assert reentry.total_error_count == 2
    assert attention.total_error_count == 0
    assert disposition is DiscriminantDisposition.INCREMENTAL_VALUE_OBSERVED


def test_attention_construct_can_collapse_when_status_reentry_already_determines_state() -> None:
    history = AttentionReplayHistory(
        "collapse-compatible",
        (
            event("e1", "only-live-branch", AttentionStatus.ACTIVE_FOCUS, actionable=True, priority_rank=0),
            event("e2", "resolved", AttentionStatus.RESOLVED, actionable=False),
        ),
    )
    expected = ExpectedAttentionState(("only-live-branch",), ("only-live-branch",))

    reentry, attention, disposition = compare_attention_incremental_value(history, expected)

    assert reentry.total_error_count == 0
    assert attention.total_error_count == 0
    assert disposition is DiscriminantDisposition.COLLAPSE_COMPATIBLE


def test_rejected_branch_cannot_carry_priority_rank() -> None:
    with pytest.raises(AttentionReplayError, match="priority_rank"):
        event(
            "e1",
            "rejected",
            AttentionStatus.REJECTED,
            actionable=False,
            priority_rank=0,
        )
