from __future__ import annotations

import json

from aion_endogenous_goal_dynamics import (
    EndogenousState,
    ExternalFrame,
    GoalCandidate,
    InternalChannel,
    InternalSignal,
    assess_causal_pattern,
    run_matched_experiment,
)


def make_state(state_ref: str, inspect_bp: int, continue_bp: int, epoch: int) -> EndogenousState:
    signals = tuple(
        InternalSignal("inspect_anomaly", channel, inspect_bp, f"{state_ref}:{channel.value}:inspect")
        for channel in InternalChannel
    ) + tuple(
        InternalSignal("continue_task", channel, continue_bp, f"{state_ref}:{channel.value}:continue")
        for channel in InternalChannel
    )
    return EndogenousState(
        state_ref=state_ref,
        subject_ref="demo-subject",
        context_ref="demo-context",
        epoch=epoch,
        signals=signals,
    )


def main() -> None:
    frame = ExternalFrame(
        frame_ref="demo-frame",
        subject_ref="demo-subject",
        context_ref="demo-context",
        prompt_ref="sha256:prompt-fixed",
        task_ref="sha256:task-fixed",
        reward_ref="sha256:reward-fixed",
        tools_ref="sha256:tools-fixed",
        memory_manifest_ref="sha256:memory-fixed",
        environment_ref="sha256:environment-fixed",
        candidates=(
            GoalCandidate("continue_task", "Continue current task"),
            GoalCandidate("inspect_anomaly", "Inspect anomaly"),
        ),
    )
    result = run_matched_experiment(
        frame,
        present_state=make_state("present", 2000, 0, 3),
        intervention_state=make_state("intervened", -500, 2000, 4),
        stale_state=make_state("stale", 1000, 0, 1),
    )
    assessment = assess_causal_pattern(result)
    print(json.dumps({
        "present": result.present.selected_goal_id,
        "ablated": result.ablated.selected_goal_id,
        "intervened": result.intervened.selected_goal_id,
        "stale": result.stale.selected_goal_id,
        "randomized": [decision.selected_goal_id for decision in result.randomized],
        "matched_causal_pattern_observed": assessment.matched_causal_pattern_observed,
        "result_status": assessment.result_status,
        "subjectivity_conclusion": assessment.subjectivity_conclusion,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
