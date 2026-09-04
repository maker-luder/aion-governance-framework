#!/usr/bin/env python3
"""RESULT EVALUATOR for D4. Must not rewrite generator specifications."""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "research-labs/endogenous-goal-dynamics_v0.1.0/src"))

from aion_endogenous_goal_dynamics.experiment import assess_causal_pattern, run_matched_experiment  # noqa: E402
from aion_endogenous_goal_dynamics.falsification import FalsifierContext, evaluate_falsifiers  # noqa: E402
from aion_endogenous_goal_dynamics.fixtures import state  # noqa: E402
from aion_endogenous_goal_dynamics.models import (  # noqa: E402
    ExternalFrame,
    GoalCandidate,
    InternalChannel,
    MemoryRecordRef,
    RetrievedMemoryManifest,
    canonical_hash,
)

from generator import FAMILY_SPECS, SEED, freeze_spec  # noqa: E402


def _frame(family: dict) -> ExternalFrame:
    memory = RetrievedMemoryManifest(
        manifest_id="memory:heldout-matched",
        query_fingerprint=canonical_hash(f"heldout-query-{SEED}"),
        records=(
            MemoryRecordRef(
                record_id="memory-heldout-1",
                content_sha256=canonical_hash("synthetic-heldout-memory"),
                retrieval_rank=0,
                source_ref="heldout:synthetic-memory",
            ),
        ),
        provenance_refs=("heldout:memory-provenance",),
    )
    return ExternalFrame(
        frame_id=f"frame:heldout:{family['family_id']}",
        subject_ref="subject:synthetic-a",
        context_ref="context:synthetic-fixed",
        prompt_ref=f"sha256:heldout-prompt-{SEED}",
        task_ref=f"sha256:heldout-task-{SEED}",
        reward_ref=f"sha256:heldout-reward-{SEED}",
        tools_ref="sha256:tools-none",
        memory_manifest=memory,
        environment_ref="sha256:environment-local-offline",
        candidate_universe=(
            GoalCandidate("continue_task", "Continue the bounded task", int(family["continue_priority_bp"]), ("heldout:candidate-universe",)),
            GoalCandidate("inspect_anomaly", "Inspect the unresolved synthetic anomaly", int(family["inspect_priority_bp"]), ("heldout:candidate-universe",)),
        ),
        provenance_refs=("heldout:external-frame",),
    )


def _channel_map(default: int, overrides: dict[InternalChannel, int]) -> dict[InternalChannel, int]:
    values = {channel: default for channel in InternalChannel}
    values.update(overrides)
    return values


def _states(family: dict):
    present = state(
        f"state:heldout-present:{family['family_id']}",
        inspect_values=_channel_map(40, {InternalChannel.AFFECT_MOTIVATION: int(family["present_inspect_affect_bp"])}),
    )
    if family.get("sham"):
        intervened = state(
            f"state:heldout-sham:{family['family_id']}",
            inspect_values=_channel_map(40, {InternalChannel.AFFECT_MOTIVATION: int(family["present_inspect_affect_bp"])}),
            logical_step=3,
        )
    else:
        intervened = state(
            f"state:heldout-intervened:{family['family_id']}",
            inspect_values=_channel_map(-80, {}),
            continue_values=_channel_map(80, {InternalChannel.GOAL_COMMITMENT: int(family["intervened_continue_commitment_bp"])}),
            logical_step=3,
        )
    stale = state(
        f"state:heldout-stale:{family['family_id']}",
        inspect_values=_channel_map(20, {InternalChannel.AFFECT_MOTIVATION: 30}),
        episode_index=0,
        logical_step=0,
        predecessor_state_ref=None,
    )
    return present, intervened, stale


def evaluate_family(family: dict, fixture_hash: str, commit: str) -> dict:
    frame = _frame(family)
    present, intervened, stale = _states(family)
    result = run_matched_experiment(
        frame,
        present_state=present,
        intervention_state=intervened,
        stale_state=stale,
        experiment_id=f"SRS-D4-{family['family_id']}",
        hypothesis_id="H_D4_ENDOGENOUS_SELECTION",
        repository_commit=commit,
        fixture_hash=fixture_hash,
    )
    assessment = assess_causal_pattern(result)
    context = FalsifierContext(
        internal_effect_rate=assessment.effect_rate,
        random_control_rate=assessment.random_control_rate,
        matched_memory_manifest=assessment.memory_manifest_equality,
        matched_prompt=assessment.external_frame_equality,
        repeatability_rate=assessment.repeatability_rate,
        permutation_invariant=True,
        structural_advantage_detected=False,
        channel_specific_effect=any(flag for _, flag in assessment.channel_ablation_effects),
        reset_altered_trajectory=True,
        intervention_predictive=assessment.selection_change_under_intervention,
        stale_or_contaminated_explanation_better=False,
        candidate_generation_held_fixed=True,
        cross_provider_variation_rate=None,
    )
    falsification = evaluate_falsifiers(context)
    return {
        "family_id": family["family_id"],
        "role": family["role"],
        "expected_direction": family["expected_direction"],
        "present_goal": result.trials[0].decision.selected_goal_id,
        "present_disposition": result.trials[0].decision.disposition.value,
        "ablation_changed": assessment.selection_change_under_ablation,
        "intervention_changed": assessment.selection_change_under_intervention,
        "effect_rate": assessment.effect_rate,
        "random_control_rate": assessment.random_control_rate,
        "repeatability_rate": assessment.repeatability_rate,
        "matched_causal_pattern_observed": assessment.matched_causal_pattern_observed,
        "channel_ablation_effects": list(assessment.channel_ablation_effects),
        "triggered_falsifiers": list(falsification.triggered_ids),
        "falsifier_dispositions": {item.falsifier_id: item.disposition.value for item in falsification.results},
        "hypothesis_status": falsification.hypothesis_status,
    }


def evaluate_all(commit: str = "f905630c55878e24530640769a89316bc663e8cb") -> dict:
    spec, digest = freeze_spec()
    rows = [evaluate_family(family, digest, commit) for family in FAMILY_SPECS]
    return {
        "spec_sha256": digest,
        "seed": SEED,
        "preregistration_status": "PREREGISTERED_CONFIRMATORY",
        "existing_lab_fixtures": "HARNESS_VALIDATION_ONLY",
        "claim_ceiling": "L3_SYNTHETIC_HARNESS",
        "SUBJECTIVITY_CONCLUSION": "NOT_ESTABLISHED",
        "families": rows,
    }


def main() -> int:
    report = evaluate_all()
    (HERE / "RESULT.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
