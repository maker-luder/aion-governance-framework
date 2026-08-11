from __future__ import annotations

import json
import math

import pytest

from aion_second_order import (
    ControlDisposition,
    FixtureProvenance,
    InterventionConditionResult,
    InterventionPolicyKind,
    ProviderReliabilityProfile,
    ReplicationMode,
    VerificationAssessment,
    VerificationInterventionCondition,
    VerificationInterventionLedger,
    build_threshold_intervention_factorial,
    default_intervention_policy,
    generate_reliability_plan,
    run_intervention_condition,
)
from aion_self_model_ablation import Task


def profile() -> ProviderReliabilityProfile:
    return ProviderReliabilityProfile(
        profile_ref="profile:synthetic-balanced-v1",
        correct_rate=0.40,
        incorrect_rate=0.20,
        ambiguous_rate=0.15,
        unavailable_rate=0.15,
        insufficient_rate=0.10,
        provenance_refs=("fixture:research-profile", "implementation:codex-research"),
    )


@pytest.mark.parametrize(
    "rates",
    [
        (-0.1, 0.3, 0.3, 0.3, 0.2),
        (0.1, 0.1, 0.1, 0.1, 0.1),
        (0.4, 0.4, 0.4, 0.0, 0.0),
        (math.nan, 0.25, 0.25, 0.25, 0.25),
        (math.inf, 0.0, 0.0, 0.0, 0.0),
    ],
)
def test_provider_reliability_rates_fail_closed(rates):
    with pytest.raises(ValueError):
        ProviderReliabilityProfile("bad", *rates, provenance_refs=("fixture:test",))


def test_seeded_provider_plan_is_deterministic_and_synthetic():
    left = generate_reliability_plan(profile(), 40, seed=19)
    right = generate_reliability_plan(profile(), 40, seed=19)
    changed = generate_reliability_plan(profile(), 40, seed=20)
    assert left == right
    assert left != changed
    assert profile().status == "SYNTHETIC_FIXTURE_PROPERTY"
    assert {item.assessment for item in left} <= set(VerificationAssessment)


def test_explicit_policy_families_preserve_neutral_experiment_variable():
    tasks = (Task("p0", 0.50), Task("p1", 0.75), Task("p2", 0.60))
    trace_only = run_intervention_condition(
        VerificationInterventionCondition.APPLIED,
        tasks,
        policy=default_intervention_policy(InterventionPolicyKind.TRACE_ONLY),
    )
    assert all(
        item.post_verification_disposition is ControlDisposition.REQUEST_VERIFICATION
        for item in trace_only.interventions
    )
    assert trace_only.policy_kind is InterventionPolicyKind.TRACE_ONLY
    assert all("optimal" not in kind.value.lower() for kind in InterventionPolicyKind)


def test_intervention_ledgers_and_condition_results_round_trip_canonically():
    result = run_intervention_condition(
        VerificationInterventionCondition.RANDOMIZED,
        (Task("r0", 0.50), Task("r1", 0.75), Task("r2", 0.60)),
        provider_profile=profile(),
        provider_sampling_seed=77,
        random_seed=9,
    )
    ledger = VerificationInterventionLedger(result.interventions)
    payload = ledger.to_json()
    restored_ledger = VerificationInterventionLedger.from_json(payload)
    assert restored_ledger.items == ledger.items
    assert payload == ledger.to_json()
    assert json.loads(payload)["schema"] == "aion.verification-intervention-ledger.v1"
    direct_payload = result.interventions[0].to_json()
    assert type(result.interventions[0]).from_json(direct_payload) == result.interventions[0]
    assert direct_payload == result.interventions[0].to_json()

    condition_payload = result.to_json()
    restored = InterventionConditionResult.from_json(condition_payload)
    assert restored == result
    assert restored.to_json() == condition_payload
    for original, round_tripped in zip(
        result.verification_traces, restored.verification_traces, strict=True
    ):
        assert round_tripped.request.target == original.request.target
        assert round_tripped.request.monitor_value == original.request.monitor_value
        assert round_tripped.request.reason == original.request.reason
        assert round_tripped.evidence == original.evidence


def test_raw_operation_counts_have_no_utility_field():
    result = run_intervention_condition(
        VerificationInterventionCondition.APPLIED,
        (Task("c0", 0.50), Task("c1", 0.75), Task("c2", 0.60)),
    )
    metrics = result.intervention_diagnostics
    assert metrics.verification_cost_units == len(result.verification_traces)
    assert metrics.decision_step_count == (
        len(result.records) + len(result.verification_traces) + len(result.interventions)
    )
    assert metrics.synthetic_latency_steps == (
        len(result.verification_traces) + len(result.interventions)
    )
    assert not hasattr(metrics, "utility")


def test_small_factorial_returns_raw_matrix_without_ranking_or_winner():
    result = build_threshold_intervention_factorial(
        thresholds=(0.60, 0.80),
        conditions=(
            VerificationInterventionCondition.TRACE_ONLY,
            VerificationInterventionCondition.APPLIED,
        ),
        tasks=(Task("f0", 0.50), Task("f1", 0.75), Task("f2", 0.60)),
        provider_profile=profile(),
    )
    assert len(result.cells) == 4
    assert all(
        (
            result.same_task_stream,
            result.same_first_order_model,
            result.same_latent_capability,
            result.same_base_task_difficulty,
            result.same_outcome_contract,
            result.same_provider_reliability_profile,
            result.same_random_seed_policy,
        )
    )
    assert result.optimization == result.winner == "NONE"
    assert len(result.raw_matrix()) == 4


def test_fixture_provenance_distinguishes_reproduction_from_replication():
    digest = "a" * 64
    reproduction = FixtureProvenance(
        "author-a", "v1", digest, "run-1", "impl-1", 7, ReplicationMode.REPRODUCTION
    )
    replication = FixtureProvenance(
        "author-b", "v2", digest, "run-2", "impl-2", 7, ReplicationMode.REPLICATION
    )
    assert reproduction.mode is ReplicationMode.REPRODUCTION
    assert replication.mode is ReplicationMode.REPLICATION
    assert reproduction.to_dict() != replication.to_dict()
