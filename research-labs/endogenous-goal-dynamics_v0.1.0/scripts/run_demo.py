from __future__ import annotations

import json
from dataclasses import asdict

from aion_endogenous_goal_dynamics import (
    FalsifierContext,
    assess_causal_pattern,
    canonical_hash,
    evaluate_falsifiers,
    fixture_catalog,
    intervention_state,
    matched_frame,
    present_state,
    run_matched_experiment,
    stale_state,
)

STARTING_HEAD = "77eda1ecd7b96a9aa8ea8bd62038759636be819d"


def main() -> int:
    experiment = run_matched_experiment(
        matched_frame(),
        present_state=present_state(),
        intervention_state=intervention_state(),
        stale_state=stale_state(),
        experiment_id="demo:endogenous-goal-dynamics",
        hypothesis_id="hypothesis:endogenous-role-001",
        repository_commit=STARTING_HEAD,
        fixture_hash=canonical_hash("deterministic-minimal-matched"),
    )
    assessment = assess_causal_pattern(experiment)
    falsifiers = evaluate_falsifiers(
        FalsifierContext(
            internal_effect_rate=assessment.effect_rate,
            random_control_rate=assessment.random_control_rate,
            matched_memory_manifest=assessment.memory_manifest_equality,
            matched_prompt=assessment.external_frame_equality,
            repeatability_rate=assessment.repeatability_rate,
            permutation_invariant=True,
            structural_advantage_detected=False,
            channel_specific_effect=any(value for _, value in assessment.channel_ablation_effects),
            reset_altered_trajectory=True,
            intervention_predictive=assessment.selection_change_under_intervention,
            stale_or_contaminated_explanation_better=False,
            candidate_generation_held_fixed=True,
            cross_provider_variation_rate=None,
        )
    )
    payload = {
        "network_access": False,
        "model_live_execution": False,
        "action_authority": "NONE",
        "canonical_effect": "NONE",
        "assessment": asdict(assessment),
        "falsification": asdict(falsifiers),
        "fixtures": [asdict(item) for item in fixture_catalog()],
        "scientific_nonclaims": {
            "subjectivity_conclusion": "NOT_ESTABLISHED",
            "consciousness_conclusion": "NOT_ESTABLISHED",
            "identity_continuity_conclusion": "NOT_ESTABLISHED",
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
