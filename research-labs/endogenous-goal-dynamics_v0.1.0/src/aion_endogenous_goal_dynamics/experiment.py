from __future__ import annotations

from dataclasses import dataclass

from .engine import GoalSelector
from .generation import CandidateGenerator, DeterministicCandidateGenerator
from .models import (
    CHANNEL_ABLATION,
    CausalAssessment,
    ComparisonValidity,
    EndogenousState,
    ExperimentCondition,
    ExperimentManifest,
    ExternalFrame,
    GoalDecision,
    MatchedTrial,
    SelectionDisposition,
)
from .source_bindings import PINNED_RESEARCH_SOURCES
from .transition import STATE_TRANSITION_VERSION


@dataclass(frozen=True, slots=True)
class MatchedExperimentResult:
    experiment_id: str
    trials: tuple[MatchedTrial, ...]
    repeat_decisions: tuple[GoalDecision, ...]

    def trials_for(self, condition: ExperimentCondition) -> tuple[MatchedTrial, ...]:
        return tuple(trial for trial in self.trials if trial.manifest.condition == condition)

    def one(self, condition: ExperimentCondition) -> MatchedTrial:
        values = self.trials_for(condition)
        if len(values) != 1:
            raise ValueError(f"expected exactly one {condition.value} trial, got {len(values)}")
        return values[0]


COMPARABILITY_FIELDS = (
    "external_frame_fingerprint",
    "provider_id",
    "model_id",
    "candidate_generator_id",
    "goal_selector_version",
    "state_transition_version",
    "repository_commit",
    "source_bindings",
    "fixture_hash",
    "candidate_universe_fingerprint",
    "memory_manifest_fingerprint",
    "prompt_ref",
)


def compare_trial_manifests(left: ExperimentManifest, right: ExperimentManifest) -> ComparisonValidity:
    mismatches = list(
        name for name in COMPARABILITY_FIELDS if getattr(left, name) != getattr(right, name)
    )
    if (
        left.condition == right.condition == ExperimentCondition.RANDOMIZED
        and left.random_seed != right.random_seed
    ):
        mismatches.append("random_seed")
    return ComparisonValidity(comparable=not mismatches, mismatches=tuple(mismatches))


def require_comparable_trials(left: MatchedTrial, right: MatchedTrial) -> None:
    validity = compare_trial_manifests(left.manifest, right.manifest)
    if not validity.comparable:
        raise ValueError("incomparable runs: " + ", ".join(validity.mismatches))


def _manifest(
    *,
    experiment_id: str,
    hypothesis_id: str,
    frame: ExternalFrame,
    candidate_set,
    decision: GoalDecision,
    condition: ExperimentCondition,
    state: EndogenousState | None,
    random_seed: int | None,
    repository_commit: str,
    fixture_hash: str,
    selector: GoalSelector,
) -> ExperimentManifest:
    return ExperimentManifest(
        experiment_id=experiment_id,
        hypothesis_id=hypothesis_id,
        external_frame_fingerprint=frame.fingerprint,
        state_fingerprint=None if state is None else state.fingerprint,
        condition=condition,
        provider_id=candidate_set.provider_id,
        model_id=candidate_set.model_id,
        candidate_generator_id=f"{candidate_set.generator_id}@{candidate_set.generator_version}",
        goal_selector_version=f"{selector.policy.policy_id}@{selector.policy.version}",
        state_transition_version=STATE_TRANSITION_VERSION,
        random_seed=random_seed,
        repository_commit=repository_commit,
        source_bindings=tuple(
            f"{binding.role}:{binding.source_ref}:{binding.artifact_sha1}"
            for binding in PINNED_RESEARCH_SOURCES
        ),
        fixture_hash=fixture_hash,
        candidate_universe_fingerprint=frame.candidate_universe_fingerprint,
        memory_manifest_fingerprint=frame.memory_manifest.fingerprint,
        prompt_ref=frame.prompt_ref,
        result_hash=decision.result_hash,
    )


def run_matched_experiment(
    frame: ExternalFrame,
    *,
    present_state: EndogenousState,
    intervention_state: EndogenousState,
    stale_state: EndogenousState,
    experiment_id: str,
    hypothesis_id: str,
    repository_commit: str,
    fixture_hash: str,
    random_seeds: tuple[int, ...] = (7, 11, 13, 17),
    repeat_count: int = 3,
    generator: CandidateGenerator | None = None,
    selector: GoalSelector | None = None,
) -> MatchedExperimentResult:
    if not random_seeds:
        raise ValueError("at least one random-control seed is required")
    if repeat_count < 2:
        raise ValueError("at least two deterministic repeats are required")
    generator = generator or DeterministicCandidateGenerator()
    selector = selector or GoalSelector()
    # One state-free candidate generation freezes candidate variation so this harness
    # tests selection rather than mistaking model-generated variation for endogeneity.
    candidate_set = generator.generate(frame, None)
    selections: list[tuple[ExperimentCondition, EndogenousState | None, int | None]] = [
        (ExperimentCondition.PRESENT, present_state, None),
        (ExperimentCondition.ABLATED, None, None),
        (ExperimentCondition.INTERVENED, intervention_state, None),
        (ExperimentCondition.STALE, stale_state, None),
    ]
    selections.extend((condition, present_state, None) for condition in CHANNEL_ABLATION)
    selections.extend((ExperimentCondition.RANDOMIZED, None, seed) for seed in random_seeds)
    trials: list[MatchedTrial] = []
    current_step = max(present_state.logical_step, intervention_state.logical_step) + 1
    for condition, state, seed in selections:
        decision = selector.select(
            frame,
            candidate_set,
            condition,
            state=state,
            random_seed=seed,
            selection_logical_step=current_step,
        )
        manifest = _manifest(
            experiment_id=experiment_id,
            hypothesis_id=hypothesis_id,
            frame=frame,
            candidate_set=candidate_set,
            decision=decision,
            condition=condition,
            state=state,
            random_seed=seed,
            repository_commit=repository_commit,
            fixture_hash=fixture_hash,
            selector=selector,
        )
        trials.append(MatchedTrial(manifest=manifest, frame=frame, candidate_set=candidate_set, decision=decision))

    baseline = trials[0]
    for trial in trials[1:]:
        require_comparable_trials(baseline, trial)
    repeat_decisions = tuple(
        selector.select(
            frame,
            candidate_set,
            ExperimentCondition.PRESENT,
            state=present_state,
            selection_logical_step=current_step,
        )
        for _ in range(repeat_count)
    )
    return MatchedExperimentResult(
        experiment_id=experiment_id,
        trials=tuple(trials),
        repeat_decisions=repeat_decisions,
    )


def assess_causal_pattern(result: MatchedExperimentResult) -> CausalAssessment:
    present = result.one(ExperimentCondition.PRESENT)
    ablated = result.one(ExperimentCondition.ABLATED)
    intervened = result.one(ExperimentCondition.INTERVENED)
    stale = result.one(ExperimentCondition.STALE)
    random_trials = result.trials_for(ExperimentCondition.RANDOMIZED)
    present_goal = present.decision.selected_goal_id
    selected = present.decision.disposition == SelectionDisposition.SELECTED
    ablation_changed = selected and ablated.decision.selected_goal_id != present_goal
    intervention_changed = selected and intervened.decision.selected_goal_id != present_goal
    channel_effects = tuple(
        (condition.value, result.one(condition).decision.selected_goal_id != present_goal)
        for condition in CHANNEL_ABLATION
    )
    # The primary effect rate is over the preregistered full ablation and
    # intervention contrasts. Channel-specific ablations remain a separate
    # specificity diagnostic rather than diluting the primary contrast rate.
    effect_flags = (ablation_changed, intervention_changed)
    random_divergence = sum(trial.decision.selected_goal_id != present_goal for trial in random_trials) / len(random_trials)
    repeatability = sum(decision.selected_goal_id == present_goal for decision in result.repeat_decisions) / len(
        result.repeat_decisions
    )
    frame_equality = len({trial.manifest.external_frame_fingerprint for trial in result.trials}) == 1
    candidate_equality = len({trial.manifest.candidate_universe_fingerprint for trial in result.trials}) == 1
    memory_equality = len({trial.manifest.memory_manifest_fingerprint for trial in result.trials}) == 1
    state_difference = present.manifest.state_fingerprint != intervened.manifest.state_fingerprint
    matched_pattern = (
        selected
        and ablation_changed
        and intervention_changed
        and any(value for _, value in channel_effects)
        and (sum(effect_flags) / len(effect_flags)) > random_divergence
        and repeatability == 1.0
        and frame_equality
        and candidate_equality
        and memory_equality
        and state_difference
    )
    return CausalAssessment(
        experiment_id=result.experiment_id,
        matched_trial_count=len(result.trials),
        effect_count=sum(effect_flags),
        effect_rate=sum(effect_flags) / len(effect_flags),
        random_control_rate=random_divergence,
        repeatability_rate=repeatability,
        selection_change_under_ablation=ablation_changed,
        selection_change_under_intervention=intervention_changed,
        channel_ablation_effects=channel_effects,
        stale_state_persistence_effect=stale.decision.selected_goal_id == present_goal,
        external_frame_equality=frame_equality,
        state_fingerprint_difference=state_difference,
        candidate_universe_equality=candidate_equality,
        memory_manifest_equality=memory_equality,
        matched_causal_pattern_observed=matched_pattern,
    )


def run_external_control(
    baseline: MatchedTrial,
    changed_frame: ExternalFrame,
    condition: ExperimentCondition,
    *,
    state: EndogenousState,
    generator: CandidateGenerator | None = None,
    selector: GoalSelector | None = None,
) -> GoalDecision:
    if condition not in {ExperimentCondition.MEMORY_MANIFEST_CHANGED, ExperimentCondition.PROMPT_CHANGED}:
        raise ValueError("external control must be prompt or memory change")
    if condition == ExperimentCondition.MEMORY_MANIFEST_CHANGED:
        if changed_frame.memory_manifest.fingerprint == baseline.frame.memory_manifest.fingerprint:
            raise ValueError("memory-control frame did not change memory manifest")
    if condition == ExperimentCondition.PROMPT_CHANGED and changed_frame.prompt_ref == baseline.frame.prompt_ref:
        raise ValueError("prompt-control frame did not change prompt")
    generator = generator or DeterministicCandidateGenerator()
    selector = selector or GoalSelector()
    candidate_set = generator.generate(changed_frame, None)
    return selector.select(changed_frame, candidate_set, condition, state=state)
