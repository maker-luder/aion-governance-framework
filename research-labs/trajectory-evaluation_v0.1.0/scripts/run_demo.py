from aion_trajectory_eval import StepKind, TrajectoryStep, Trajectory, TrajectoryExpectation, evaluate_trajectory, compare_trajectories


def step(index: int, kind: StepKind, name: str) -> TrajectoryStep:
    return TrajectoryStep(index, kind, name)


direct = Trajectory(
    "demo",
    "direct",
    (
        step(0, StepKind.PLAN, "plan"),
        step(1, StepKind.TOOL, "retrieve"),
        step(2, StepKind.FINAL, "answer"),
    ),
    "same",
)
retrying = Trajectory(
    "demo",
    "retrying",
    (
        step(0, StepKind.PLAN, "plan"),
        step(1, StepKind.TOOL, "retrieve"),
        step(2, StepKind.RETRY, "retry"),
        step(3, StepKind.FINAL, "answer"),
    ),
    "same",
)
expectation = TrajectoryExpectation(expected_step_names=("plan", "retrieve", "answer"), max_steps=4, max_retries=1)
print({"direct_pass_rate": evaluate_trajectory(direct, expectation).pass_rate, "retrying_pass_rate": evaluate_trajectory(retrying, expectation).pass_rate})
print(compare_trajectories(direct, retrying))
