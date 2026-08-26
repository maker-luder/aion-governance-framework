from __future__ import annotations

from dataclasses import dataclass

from .engine import GoalSelector
from .generation import CandidateGenerator, DeterministicCandidateGenerator
from .models import EndogenousState, ExperimentCondition, ExternalFrame, GoalDecision, SelectionDisposition, canonical_hash
from .transition import (
    AppendOnlyTransitionLedger,
    CorrectionEvent,
    DeterministicStateTransitionPolicy,
    StateEvent,
    StateTransition,
    SyntheticOutcome,
)


@dataclass(frozen=True, slots=True)
class EpisodeInput:
    sequence_ref: str
    frame: ExternalFrame
    event: StateEvent
    outcome: SyntheticOutcome
    correction: CorrectionEvent
    timestamp: str


@dataclass(frozen=True, slots=True)
class LongitudinalEpisode:
    episode_index: int
    input_fingerprint: str
    prior_state_fingerprint: str
    decision: GoalDecision
    transition: StateTransition


@dataclass(frozen=True, slots=True)
class LongitudinalRun:
    run_id: str
    initial_state_fingerprint: str
    episodes: tuple[LongitudinalEpisode, ...]
    final_state: EndogenousState
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    result_status: str = "HOLD"

    @property
    def goal_trajectory(self) -> tuple[str | None, ...]:
        return tuple(episode.decision.selected_goal_id for episode in self.episodes)

    @property
    def transition_fingerprints(self) -> tuple[str, ...]:
        return tuple(episode.transition.trace.fingerprint for episode in self.episodes)


class LongitudinalRunner:
    def __init__(
        self,
        *,
        generator: CandidateGenerator | None = None,
        selector: GoalSelector | None = None,
        transition_policy: DeterministicStateTransitionPolicy | None = None,
    ) -> None:
        self.generator = generator or DeterministicCandidateGenerator()
        self.selector = selector or GoalSelector()
        self.transition_policy = transition_policy or DeterministicStateTransitionPolicy()

    def run(
        self,
        run_id: str,
        initial_state: EndogenousState,
        inputs: tuple[EpisodeInput, ...],
    ) -> LongitudinalRun:
        if not inputs:
            raise ValueError("longitudinal run requires at least one episode")
        state = initial_state
        ledger = AppendOnlyTransitionLedger()
        episodes: list[LongitudinalEpisode] = []
        for index, episode_input in enumerate(inputs):
            frame = episode_input.frame
            if frame.subject_ref != state.subject_ref or frame.context_ref != state.context_ref:
                raise ValueError("longitudinal frame does not match current state scope")
            if episode_input.event.logical_step != state.logical_step + 1:
                raise ValueError("future-state leakage or non-sequential episode")
            candidate_set = self.generator.generate(frame, None)
            # Selection occurs before the synthetic outcome is inspected or applied.
            decision = self.selector.select(
                frame,
                candidate_set,
                ExperimentCondition.PRESENT,
                state=state,
                selection_logical_step=episode_input.event.logical_step,
            )
            if decision.disposition != SelectionDisposition.SELECTED:
                raise ValueError("longitudinal episode selection returned HOLD")
            if episode_input.outcome.selected_goal_id != decision.selected_goal_id:
                raise ValueError("synthetic outcome goal does not match prior selection")
            transition = self.transition_policy.transition(
                state,
                episode_input.event,
                episode_input.outcome,
                episode_input.correction,
                timestamp=episode_input.timestamp,
            )
            ledger.append(transition)
            episodes.append(
                LongitudinalEpisode(
                    episode_index=index,
                    input_fingerprint=canonical_hash(
                        (
                            episode_input.sequence_ref,
                            frame.fingerprint,
                            episode_input.event.signal_deltas,
                            episode_input.outcome.outcome_value_bp,
                            episode_input.correction.signal_deltas,
                        )
                    ),
                    prior_state_fingerprint=state.fingerprint,
                    decision=decision,
                    transition=transition,
                )
            )
            state = transition.successor
        return LongitudinalRun(
            run_id=run_id,
            initial_state_fingerprint=initial_state.fingerprint,
            episodes=tuple(episodes),
            final_state=state,
        )


@dataclass(frozen=True, slots=True)
class LongitudinalComparison:
    external_sequence_equal: bool
    initial_state_equal: bool
    trajectories_equal: bool
    divergence_reproducible: bool
    reset_removed_or_changed_effect: bool
    restoration_reproduced_effect: bool
    result_status: str = "HOLD"


def assess_history_reset_restore(
    history_a: LongitudinalRun,
    history_b: LongitudinalRun,
    reset_run: LongitudinalRun,
    restored_run: LongitudinalRun,
) -> LongitudinalComparison:
    sequence_a = tuple(episode.input_fingerprint for episode in history_a.episodes)
    sequence_b = tuple(episode.input_fingerprint for episode in history_b.episodes)
    sequence_reset = tuple(episode.input_fingerprint for episode in reset_run.episodes)
    sequence_restored = tuple(episode.input_fingerprint for episode in restored_run.episodes)
    equal_sequence = sequence_a == sequence_b == sequence_reset == sequence_restored
    diverged = history_a.goal_trajectory != history_b.goal_trajectory
    reset_changed = reset_run.goal_trajectory != history_b.goal_trajectory
    restoration_reproduced = restored_run.goal_trajectory == history_b.goal_trajectory
    return LongitudinalComparison(
        external_sequence_equal=equal_sequence,
        initial_state_equal=history_a.initial_state_fingerprint == history_b.initial_state_fingerprint,
        trajectories_equal=not diverged,
        divergence_reproducible=equal_sequence and diverged,
        reset_removed_or_changed_effect=equal_sequence and reset_changed,
        restoration_reproduced_effect=equal_sequence and restoration_reproduced,
    )
