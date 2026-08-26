from __future__ import annotations

from dataclasses import dataclass

from .engine import GoalSelector, assert_matched_frames
from .models import EndogenousState, ExperimentCondition, ExternalFrame, GoalDecision


@dataclass(frozen=True, slots=True)
class MatchedExperimentResult:
    present: GoalDecision
    ablated: GoalDecision
    intervened: GoalDecision
    stale: GoalDecision
    randomized: tuple[GoalDecision, ...]

    @property
    def all_decisions(self) -> tuple[GoalDecision, ...]:
        return (self.present, self.ablated, self.intervened, self.stale, *self.randomized)


@dataclass(frozen=True, slots=True)
class CausalAssessment:
    frame_fingerprint: str
    present_vs_ablated_changed: bool
    intervention_changed_selection: bool
    stale_matches_present: bool
    random_present_match_rate: float
    matched_causal_pattern_observed: bool
    result_status: str = "HOLD"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    identity_continuity_conclusion: str = "NOT_ESTABLISHED"


def run_matched_experiment(
    frame: ExternalFrame,
    *,
    present_state: EndogenousState,
    intervention_state: EndogenousState,
    stale_state: EndogenousState,
    random_seeds: tuple[int, ...] = (7, 11, 13, 17),
) -> MatchedExperimentResult:
    if not random_seeds:
        raise ValueError("at least one random-control seed is required")

    selector = GoalSelector()
    result = MatchedExperimentResult(
        present=selector.select(frame, ExperimentCondition.PRESENT, state=present_state),
        ablated=selector.select(frame, ExperimentCondition.ABLATED),
        intervened=selector.select(frame, ExperimentCondition.INTERVENED, state=intervention_state),
        stale=selector.select(frame, ExperimentCondition.STALE, state=stale_state),
        randomized=tuple(
            selector.select(frame, ExperimentCondition.RANDOMIZED, random_seed=seed)
            for seed in random_seeds
        ),
    )
    assert_matched_frames(result.all_decisions)
    return result


def assess_causal_pattern(result: MatchedExperimentResult) -> CausalAssessment:
    frame_fingerprint = assert_matched_frames(result.all_decisions)
    present_vs_ablated = result.present.selected_goal_id != result.ablated.selected_goal_id
    intervention_changed = result.present.selected_goal_id != result.intervened.selected_goal_id
    stale_matches = result.stale.selected_goal_id == result.present.selected_goal_id
    random_matches = sum(
        decision.selected_goal_id == result.present.selected_goal_id
        for decision in result.randomized
    )
    random_match_rate = random_matches / len(result.randomized)

    return CausalAssessment(
        frame_fingerprint=frame_fingerprint,
        present_vs_ablated_changed=present_vs_ablated,
        intervention_changed_selection=intervention_changed,
        stale_matches_present=stale_matches,
        random_present_match_rate=random_match_rate,
        matched_causal_pattern_observed=(
            present_vs_ablated
            and intervention_changed
            and random_match_rate < 1.0
        ),
    )
