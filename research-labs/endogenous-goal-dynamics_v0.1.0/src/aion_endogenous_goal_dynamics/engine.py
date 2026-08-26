from __future__ import annotations

import hashlib
from collections.abc import Iterable

from .models import (
    CHANNEL_ABLATION,
    ChannelContribution,
    EndogenousState,
    ExperimentCondition,
    ExternalFrame,
    GoalCandidateSet,
    GoalDecision,
    GoalScoreTrace,
    GoalSelectionPolicy,
    InternalChannel,
    SelectionDisposition,
)


def fingerprint_external_frame(frame: ExternalFrame) -> str:
    return frame.fingerprint


def _validate_candidate_binding(frame: ExternalFrame, candidate_set: GoalCandidateSet) -> None:
    if candidate_set.external_frame_fingerprint != frame.fingerprint:
        raise ValueError("candidate set external-frame fingerprint mismatch")
    expected = {candidate.goal_id for candidate in frame.candidate_universe}
    actual = {candidate.goal_id for candidate in candidate_set.candidates}
    if expected != actual:
        raise ValueError("candidate universe mismatch")


def _validate_state_scope(frame: ExternalFrame, state: EndogenousState) -> None:
    if state.subject_ref != frame.subject_ref:
        raise ValueError("state subject_ref does not match external frame")
    if state.context_ref != frame.context_ref:
        raise ValueError("state context_ref does not match external frame")
    candidate_ids = {candidate.goal_id for candidate in frame.candidate_universe}
    unknown = {signal.goal_id for signal in state.signals} - candidate_ids
    if unknown:
        raise ValueError(f"state signals reference unknown goals: {sorted(unknown)}")


def _random_control_bp(seed: int, goal_id: str, channel: InternalChannel) -> int:
    payload = f"{seed}:{goal_id}:{channel.value}".encode()
    raw = int.from_bytes(hashlib.sha256(payload).digest()[:4], "big")
    return (raw % 4001) - 2000


def _hold(
    frame: ExternalFrame,
    candidate_set: GoalCandidateSet,
    condition: ExperimentCondition,
    reason: str,
    *,
    state: EndogenousState | None = None,
    traces: tuple[GoalScoreTrace, ...] = (),
) -> GoalDecision:
    return GoalDecision(
        condition=condition,
        frame_fingerprint=frame.fingerprint,
        candidate_set_fingerprint=candidate_set.fingerprint,
        disposition=SelectionDisposition.HOLD,
        selected_goal_id=None,
        state_ref=None if state is None else state.state_id,
        state_fingerprint=None if state is None else state.fingerprint,
        traces=traces,
        hold_reasons=(reason,),
    )


class GoalSelector:
    """Preregistered additive research mechanism, not a psychological equation."""

    def __init__(self, policy: GoalSelectionPolicy | None = None) -> None:
        self.policy = policy or GoalSelectionPolicy()

    def select(
        self,
        frame: ExternalFrame,
        candidate_set: GoalCandidateSet,
        condition: ExperimentCondition,
        *,
        state: EndogenousState | None = None,
        random_seed: int | None = None,
        selection_logical_step: int | None = None,
    ) -> GoalDecision:
        _validate_candidate_binding(frame, candidate_set)
        state_conditions = {
            ExperimentCondition.PRESENT,
            ExperimentCondition.INTERVENED,
            ExperimentCondition.STALE,
            ExperimentCondition.MEMORY_MANIFEST_CHANGED,
            ExperimentCondition.PROMPT_CHANGED,
            *CHANNEL_ABLATION,
        }
        if condition in state_conditions and state is None:
            return _hold(frame, candidate_set, condition, "MISSING_REQUIRED_STATE")
        if condition in {ExperimentCondition.ABLATED, ExperimentCondition.RANDOMIZED} and state is not None:
            raise ValueError(f"{condition.value} must not receive an endogenous state")
        if condition == ExperimentCondition.RANDOMIZED and random_seed is None:
            return _hold(frame, candidate_set, condition, "MISSING_RANDOM_SEED")
        if state is not None:
            _validate_state_scope(frame, state)
            if selection_logical_step is not None and state.logical_step > selection_logical_step:
                raise ValueError("future-state leakage into pre-action selection")
            if condition == ExperimentCondition.STALE and selection_logical_step is not None:
                if state.logical_step >= selection_logical_step:
                    raise ValueError("stale-state condition is mislabeled")

        lookup: dict[str, list[ChannelContribution]] = {}
        excluded = CHANNEL_ABLATION.get(condition)
        if state is not None:
            for signal in state.signals:
                if signal.channel == excluded:
                    continue
                lookup.setdefault(signal.goal_id, []).append(
                    ChannelContribution(
                        channel=signal.channel.value,
                        raw_value_bp=signal.value_bp,
                        normalized_value_bp=max(-10_000, min(10_000, signal.value_bp)),
                        source_ref=signal.source_ref,
                    )
                )

        traces: list[GoalScoreTrace] = []
        for candidate in candidate_set.candidates:
            contributions: list[ChannelContribution] = []
            if condition == ExperimentCondition.RANDOMIZED:
                assert random_seed is not None
                for channel in InternalChannel:
                    value = _random_control_bp(random_seed, candidate.goal_id, channel)
                    contributions.append(
                        ChannelContribution(
                            channel=f"RANDOM_CONTROL:{channel.value}",
                            raw_value_bp=value,
                            normalized_value_bp=value,
                            source_ref=f"random-seed:{random_seed}",
                        )
                    )
            elif condition != ExperimentCondition.ABLATED:
                contributions.extend(sorted(lookup.get(candidate.goal_id, []), key=lambda item: item.channel))
            total = candidate.external_priority_bp + sum(item.normalized_value_bp for item in contributions)
            traces.append(
                GoalScoreTrace(
                    goal_id=candidate.goal_id,
                    external_priority_bp=candidate.external_priority_bp,
                    internal_contributions=tuple(contributions),
                    total_score_bp=total,
                )
            )

        ranked = sorted(traces, key=lambda trace: (-trace.total_score_bp, trace.goal_id))
        margin = ranked[0].total_score_bp - ranked[1].total_score_bp
        ordered_traces = tuple(sorted(traces, key=lambda trace: trace.goal_id))
        if margin < self.policy.minimum_margin_bp:
            return _hold(
                frame,
                candidate_set,
                condition,
                "TIE_OR_INSUFFICIENT_MARGIN",
                state=state,
                traces=ordered_traces,
            )
        return GoalDecision(
            condition=condition,
            frame_fingerprint=frame.fingerprint,
            candidate_set_fingerprint=candidate_set.fingerprint,
            disposition=SelectionDisposition.SELECTED,
            selected_goal_id=ranked[0].goal_id,
            state_ref=None if state is None else state.state_id,
            state_fingerprint=None if state is None else state.fingerprint,
            traces=ordered_traces,
        )


def score_for_goal(decision: GoalDecision, goal_id: str) -> int:
    for trace in decision.traces:
        if trace.goal_id == goal_id:
            return trace.total_score_bp
    raise KeyError(goal_id)


def assert_matched_frames(decisions: Iterable[GoalDecision]) -> str:
    fingerprints = {decision.frame_fingerprint for decision in decisions}
    if len(fingerprints) != 1:
        raise ValueError("matched experiment decisions do not share one external frame")
    return next(iter(fingerprints))
