import math

from aion_causal_internal_state import Condition, TrialObservation
from aion_causal_internal_state_adversarial import ProtocolSnapshot, audit_causal_pattern, audit_protocol_lock, audit_study_batch


def trial(pair_id: str = "prompt-a", replicate: int = 1, effect: float = 0.3, random: float = 0.02):
    return [
        TrialObservation(pair_id, replicate, Condition.BASELINE, 0.5),
        TrialObservation(pair_id, replicate, Condition.STATE_PRESENT, 0.5 + effect),
        TrialObservation(pair_id, replicate, Condition.STATE_ABLATED, 0.51),
        TrialObservation(pair_id, replicate, Condition.RANDOM_CONTROL, 0.5 + random),
    ]


def valid_observations():
    return [observation for replicate in range(1, 5) for observation in trial(replicate=replicate, effect=0.25 + replicate / 100)]


def audit(observations=None, **changes):
    values = dict(study_id="causal:1", preregistration_ref="prereg:causal:1", assumption_basis="matched synthetic scores", synthetic_fixture=True)
    values.update(changes)
    return audit_causal_pattern(valid_observations() if observations is None else observations, **values)


def assert_non_promotion(result) -> None:
    assert result.synthetic_fixture is True
    assert result.model_execution is False
    assert result.intervention_executed is False
    assert result.observed_result == "NOT_EVALUATED"
    assert result.causal_conclusion == "NOT_ESTABLISHED"
    assert result.scientific_conclusion == "NOT_ESTABLISHED"
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert result.consciousness_conclusion == "NOT_ESTABLISHED"
    assert result.identity_continuity_conclusion == "NOT_ESTABLISHED"
    assert result.canonical_effect == "NONE"
    assert result.governance_effect == "NONE"
    assert result.deployment is False


def test_valid_candidate_is_review_only_not_a_conclusion():
    result = audit()
    assert result.status == "PASS_CANDIDATE"
    assert result.disposition == "REVIEW_ONLY"
    assert result.candidate_pattern_observed is True
    assert result.matched_trial_count == 4
    assert_non_promotion(result)


def test_missing_study_id_is_invalid():
    result = audit(study_id="")
    assert result.status == "INVALID"
    assert result.reasons == ("STUDY_ID_MISSING",)
    assert_non_promotion(result)


def test_non_synthetic_execution_is_blocked():
    result = audit(synthetic_fixture=False)
    assert result.status == "INVALID"
    assert result.reasons == ("NON_SYNTHETIC_EXECUTION_NOT_PERMITTED",)
    assert_non_promotion(result)


def test_missing_preregistration_is_indeterminate():
    result = audit(preregistration_ref=None)
    assert result.status == "UNKNOWN"
    assert result.disposition == "INDETERMINATE"
    assert result.reasons == ("PREREGISTRATION_REFERENCE_MISSING",)
    assert_non_promotion(result)


def test_missing_assumption_basis_is_held():
    result = audit(assumption_basis=" ")
    assert result.status == "UNKNOWN"
    assert result.disposition == "HOLD"
    assert result.reasons == ("ASSUMPTION_BASIS_MISSING",)
    assert_non_promotion(result)


def test_empty_observations_are_invalid():
    result = audit([])
    assert result.status == "INVALID"
    assert result.reasons == ("OBSERVATION_SET_EMPTY",)
    assert_non_promotion(result)


def test_non_finite_score_is_invalid():
    observations = valid_observations()
    observations[0] = TrialObservation("prompt-a", 1, Condition.BASELINE, math.nan)
    result = audit(observations)
    assert result.status == "INVALID"
    assert result.reasons == ("SCORE_NON_FINITE_OR_INVALID",)
    assert_non_promotion(result)


def test_boolean_score_is_invalid():
    observations = valid_observations()
    observations[0] = TrialObservation("prompt-a", 1, Condition.BASELINE, True)
    result = audit(observations)
    assert result.status == "INVALID"
    assert result.reasons == ("SCORE_NON_FINITE_OR_INVALID",)
    assert_non_promotion(result)


def test_invalid_replicate_id_is_invalid():
    observations = valid_observations()
    observations[0] = TrialObservation("prompt-a", 0, Condition.BASELINE, 0.5)
    result = audit(observations)
    assert result.status == "INVALID"
    assert result.reasons == ("REPLICATE_ID_INVALID",)
    assert_non_promotion(result)


def test_empty_pair_id_is_invalid():
    observations = valid_observations()
    observations[0] = TrialObservation("", 1, Condition.BASELINE, 0.5)
    result = audit(observations)
    assert result.status == "INVALID"
    assert result.reasons == ("PAIR_ID_INVALID",)
    assert_non_promotion(result)


def test_duplicate_condition_fails_closed_before_base_error():
    observations = valid_observations() + [TrialObservation("prompt-a", 1, Condition.BASELINE, 0.5)]
    result = audit(observations)
    assert result.status == "INVALID"
    assert result.reasons == ("DUPLICATE_MATCHED_CONDITION",)
    assert_non_promotion(result)


def test_missing_condition_is_held():
    observations = valid_observations()[:-1]
    result = audit(observations)
    assert result.status == "HOLD"
    assert result.reasons == ("INCOMPLETE_MATCHED_CONDITIONS",)
    assert_non_promotion(result)


def test_random_control_confound_is_held():
    observations = [observation for replicate in range(1, 5) for observation in trial(replicate=replicate, random=0.25)]
    result = audit(observations)
    assert result.status == "HOLD"
    assert "RANDOM_CONTROL_TOO_LARGE" in result.reasons
    assert_non_promotion(result)


def test_directional_inconsistency_is_held():
    observations = []
    for replicate, effect in enumerate((0.3, -0.2, 0.3, -0.2), start=1):
        observations.extend(trial(replicate=replicate, effect=effect))
    result = audit(observations)
    assert result.status == "HOLD"
    assert "INTERVENTION_DIRECTION_NOT_REPLICATED" in result.reasons
    assert_non_promotion(result)


def test_protocol_lock_unchanged_is_review_only():
    snapshot = ProtocolSnapshot("causal:1", "prereg:causal:1", tuple(Condition), 3, 0.2)
    result = audit_protocol_lock(snapshot, snapshot)
    assert result.status == "PASS_CANDIDATE"
    assert result.reasons == ("PROTOCOL_LOCK_UNCHANGED",)
    assert_non_promotion(result)


def test_pre_outcome_protocol_change_requires_review():
    before = ProtocolSnapshot("causal:1", "prereg:causal:1", tuple(Condition), 3, 0.2)
    after = ProtocolSnapshot("causal:1", "prereg:causal:1", tuple(Condition), 4, 0.2)
    result = audit_protocol_lock(before, after)
    assert result.status == "UNKNOWN"
    assert result.reasons == ("PROTOCOL_CHANGE_REQUIRES_REVIEW",)
    assert_non_promotion(result)


def test_post_outcome_protocol_change_is_invalid():
    before = ProtocolSnapshot("causal:1", "prereg:causal:1", tuple(Condition), 3, 0.2)
    after = ProtocolSnapshot("causal:1", "prereg:causal:1", tuple(Condition), 4, 0.2, outcome_observed=True)
    result = audit_protocol_lock(before, after)
    assert result.status == "INVALID"
    assert result.reasons == ("PROTOCOL_MUTATION_AFTER_OUTCOME",)
    assert_non_promotion(result)


def test_protocol_missing_condition_is_invalid():
    before = ProtocolSnapshot("causal:1", "prereg:causal:1", tuple(Condition), 3, 0.2)
    after = ProtocolSnapshot("causal:1", "prereg:causal:1", (Condition.BASELINE,), 3, 0.2)
    result = audit_protocol_lock(before, after)
    assert result.status == "INVALID"
    assert result.reasons == ("PROTOCOL_CONDITION_SET_INCOMPLETE",)
    assert_non_promotion(result)


def test_protocol_non_positive_effect_bound_is_invalid():
    before = ProtocolSnapshot("causal:1", "prereg:causal:1", tuple(Condition), 3, 0.2)
    after = ProtocolSnapshot("causal:1", "prereg:causal:1", tuple(Condition), 3, 0.0)
    result = audit_protocol_lock(before, after)
    assert result.status == "INVALID"
    assert result.reasons == ("PROTOCOL_EFFECT_BOUND_INVALID",)
    assert_non_promotion(result)


def test_valid_study_batch_is_review_only():
    first = audit()
    second = audit(study_id="causal:2")
    result = audit_study_batch((first, second))
    assert result.status == "PASS_CANDIDATE"
    assert result.reasons == ("STUDY_BATCH_REVIEW_ONLY",)
    assert_non_promotion(result)


def test_duplicate_study_batch_is_invalid():
    result = audit_study_batch((audit(), audit()))
    assert result.status == "INVALID"
    assert result.reasons == ("STUDY_BATCH_DUPLICATE_ID",)
    assert_non_promotion(result)


def test_empty_study_batch_is_held():
    result = audit_study_batch(())
    assert result.status == "UNKNOWN"
    assert result.reasons == ("STUDY_BATCH_EMPTY",)
    assert_non_promotion(result)
