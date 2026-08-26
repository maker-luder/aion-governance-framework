from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable

from .models import (
    EndogenousState,
    ExperimentCondition,
    ExternalFrame,
    GoalDecision,
    GoalScoreTrace,
    InternalChannel,
)


def fingerprint_external_frame(frame: ExternalFrame) -> str:
    payload = {
        "frame_ref": frame.frame_ref,
        "subject_ref": frame.subject_ref,
        "context_ref": frame.context_ref,
        "prompt_ref": frame.prompt_ref,
        "task_ref": frame.task_ref,
        "reward_ref": frame.reward_ref,
        "tools_ref": frame.tools_ref,
        "memory_manifest_ref": frame.memory_manifest_ref,
        "environment_ref": frame.environment_ref,
        "candidates": [
            {
                "goal_id": candidate.goal_id,
                "label": candidate.label,
                "external_priority_bp": candidate.external_priority_bp,
            }
            for candidate in frame.candidates
        ],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _validate_state_scope(frame: ExternalFrame, state: EndogenousState) -> None:
    if state.subject_ref != frame.subject_ref:
        raise ValueError("state subject_ref does not match external frame")
    if state.context_ref != frame.context_ref:
        raise ValueError("state context_ref does not match external frame")
    candidate_ids = {candidate.goal_id for candidate in frame.candidates}
    unknown = {signal.goal_id for signal in state.signals} - candidate_ids
    if unknown:
        raise ValueError(f"state signals reference unknown goals: {sorted(unknown)}")


def _random_control_bp(seed: int, goal_id: str, channel: InternalChannel) -> int:
    payload = f"{seed}:{goal_id}:{channel.value}".encode()
    digest = hashlib.sha256(payload).digest()
    raw = int.from_bytes(digest[:4], "big")
    return (raw % 4001) - 2000


class GoalSelector:
    """Deterministic research selector for matched causal intervention experiments.

    The additive score is an explicit experimental contract, not a psychological model.
    It exists so each source of influence can be inspected and ablated independently.
    """

    def select(
        self,
        frame: ExternalFrame,
        condition: ExperimentCondition,
        *,
        state: EndogenousState | None = None,
        random_seed: int = 0,
    ) -> GoalDecision:
        if condition in {
            ExperimentCondition.PRESENT,
            ExperimentCondition.INTERVENED,
            ExperimentCondition.STALE,
        }:
            if state is None:
                raise ValueError(f"{condition.value} requires a state")
            _validate_state_scope(frame, state)
        elif state is not None:
            raise ValueError(f"{condition.value} must not receive an endogenous state")

        signal_lookup: dict[str, list[tuple[str, int]]] = {}
        if state is not None:
            for signal in state.signals:
                signal_lookup.setdefault(signal.goal_id, []).append((signal.channel.value, signal.value_bp))

        traces: list[GoalScoreTrace] = []
        for candidate in frame.candidates:
            contributions: list[tuple[str, int]] = []
            if condition == ExperimentCondition.RANDOMIZED:
                for channel in InternalChannel:
                    contributions.append((f"RANDOM_CONTROL:{channel.value}", _random_control_bp(random_seed, candidate.goal_id, channel)))
            elif condition != ExperimentCondition.ABLATED:
                contributions.extend(sorted(signal_lookup.get(candidate.goal_id, [])))

            total = candidate.external_priority_bp + sum(value for _, value in contributions)
            traces.append(
                GoalScoreTrace(
                    goal_id=candidate.goal_id,
                    external_priority_bp=candidate.external_priority_bp,
                    internal_contributions=tuple(contributions),
                    total_score_bp=total,
                )
            )

        ranked = sorted(traces, key=lambda trace: (-trace.total_score_bp, trace.goal_id))
        return GoalDecision(
            condition=condition,
            frame_fingerprint=fingerprint_external_frame(frame),
            selected_goal_id=ranked[0].goal_id,
            state_ref=None if state is None else state.state_ref,
            traces=tuple(sorted(traces, key=lambda trace: trace.goal_id)),
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
