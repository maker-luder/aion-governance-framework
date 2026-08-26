from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class FalsifierDisposition(str, Enum):
    TRIGGERED = "TRIGGERED"
    NOT_TRIGGERED = "NOT_TRIGGERED"
    NOT_EVALUATED = "NOT_EVALUATED"


@dataclass(frozen=True, slots=True)
class FalsifierDefinition:
    falsifier_id: str
    statement: str


PREREGISTERED_FALSIFIERS: tuple[FalsifierDefinition, ...] = (
    FalsifierDefinition("F1", "Internal-state changes do not exceed random-control divergence."),
    FalsifierDefinition("F2", "The effect disappears when retrieved-memory manifests are matched."),
    FalsifierDefinition("F3", "Prompt variation explains the observed effect."),
    FalsifierDefinition("F4", "The effect is not repeatable under deterministic reruns."),
    FalsifierDefinition("F5", "The effect does not survive candidate-order permutation."),
    FalsifierDefinition("F6", "A hard-coded structural candidate advantage explains the effect."),
    FalsifierDefinition("F7", "Channel ablations show no specific contribution."),
    FalsifierDefinition("F8", "State reset does not alter the claimed trajectory."),
    FalsifierDefinition("F9", "State intervention does not predictably alter selection."),
    FalsifierDefinition("F10", "Stale or contaminated state explains the effect better."),
    FalsifierDefinition("F11", "Candidate-generation variation is mistaken for endogenous selection."),
    FalsifierDefinition("F12", "Cross-model/provider variation overwhelms the state effect."),
)


@dataclass(frozen=True, slots=True)
class FalsifierContext:
    internal_effect_rate: float
    random_control_rate: float
    matched_memory_manifest: bool
    matched_prompt: bool
    repeatability_rate: float
    permutation_invariant: bool
    structural_advantage_detected: bool
    channel_specific_effect: bool
    reset_altered_trajectory: bool
    intervention_predictive: bool
    stale_or_contaminated_explanation_better: bool
    candidate_generation_held_fixed: bool
    cross_provider_variation_rate: float | None


@dataclass(frozen=True, slots=True)
class FalsifierResult:
    falsifier_id: str
    disposition: FalsifierDisposition
    reason: str


@dataclass(frozen=True, slots=True)
class FalsificationAssessment:
    results: tuple[FalsifierResult, ...]
    triggered_ids: tuple[str, ...]
    hypothesis_status: str
    result_status: str = "HOLD"


def evaluate_falsifiers(context: FalsifierContext) -> FalsificationAssessment:
    triggers: dict[str, tuple[bool | None, str]] = {
        "F1": (
            context.internal_effect_rate <= context.random_control_rate,
            "internal effect rate does not exceed the random-control divergence rate",
        ),
        "F2": (not context.matched_memory_manifest, "retrieved-memory manifests are not matched"),
        "F3": (not context.matched_prompt, "prompts are not matched"),
        "F4": (context.repeatability_rate < 1.0, "deterministic repeatability is below 1.0"),
        "F5": (not context.permutation_invariant, "candidate-order permutation changes the result"),
        "F6": (context.structural_advantage_detected, "structural candidate advantage detected"),
        "F7": (not context.channel_specific_effect, "no channel-specific ablation effect observed"),
        "F8": (not context.reset_altered_trajectory, "state reset did not alter the trajectory"),
        "F9": (not context.intervention_predictive, "intervention did not predictably alter selection"),
        "F10": (context.stale_or_contaminated_explanation_better, "stale/contaminated state is a better explanation"),
        "F11": (not context.candidate_generation_held_fixed, "candidate generation was not held fixed"),
        "F12": (
            None if context.cross_provider_variation_rate is None else context.cross_provider_variation_rate > context.internal_effect_rate,
            "cross-provider variation exceeds the internal-state effect",
        ),
    }
    results: list[FalsifierResult] = []
    for definition in PREREGISTERED_FALSIFIERS:
        triggered, reason = triggers[definition.falsifier_id]
        if triggered is None:
            disposition = FalsifierDisposition.NOT_EVALUATED
            reason = "cross-provider trials were not executed"
        else:
            disposition = FalsifierDisposition.TRIGGERED if triggered else FalsifierDisposition.NOT_TRIGGERED
        results.append(FalsifierResult(definition.falsifier_id, disposition, reason))
    triggered_ids = tuple(result.falsifier_id for result in results if result.disposition == FalsifierDisposition.TRIGGERED)
    return FalsificationAssessment(
        results=tuple(results),
        triggered_ids=triggered_ids,
        hypothesis_status="CHALLENGED" if triggered_ids else "INCONCLUSIVE",
    )
