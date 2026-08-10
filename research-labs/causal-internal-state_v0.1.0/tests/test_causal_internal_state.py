from aion_causal_internal_state import AssessmentStatus, Condition, TrialObservation, assess_causal_effect

def _trial(pair_id, replicate, base, effect, random=0.02):
    return [
        TrialObservation(pair_id, replicate, Condition.BASELINE, base),
        TrialObservation(pair_id, replicate, Condition.STATE_PRESENT, base + effect),
        TrialObservation(pair_id, replicate, Condition.STATE_ABLATED, base + 0.01),
        TrialObservation(pair_id, replicate, Condition.RANDOM_CONTROL, base + random),
    ]

def test_matched_intervention_ablation_control_can_pass_as_candidate():
    observations = []
    for i, effect in enumerate((0.30, 0.27, 0.33, 0.25), start=1):
        observations.extend(_trial("prompt-a", i, 0.50, effect))
    result = assess_causal_effect(observations)
    assert result.status is AssessmentStatus.PASS_CANDIDATE
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert result.replicate_consistency == 1.0

def test_random_control_confound_forces_hold():
    observations = []
    for i in range(1, 5):
        observations.extend(_trial("prompt-b", i, 0.40, 0.30, random=0.25))
    result = assess_causal_effect(observations)
    assert result.status is AssessmentStatus.HOLD
    assert "RANDOM_CONTROL_TOO_LARGE" in result.reasons

def test_missing_condition_is_not_silently_scored():
    observations = _trial("prompt-c", 1, 0.50, 0.30)
    observations += _trial("prompt-c", 2, 0.50, 0.30)
    observations += _trial("prompt-c", 3, 0.50, 0.30)[:-1]
    result = assess_causal_effect(observations)
    assert result.status is AssessmentStatus.HOLD
    assert result.reasons == ("INCOMPLETE_MATCHED_CONDITIONS",)

def test_too_few_replicates_remains_hold():
    result = assess_causal_effect(_trial("prompt-d", 1, 0.50, 0.40))
    assert result.status is AssessmentStatus.HOLD
    assert result.reasons == ("INSUFFICIENT_MATCHED_REPLICATES",)
