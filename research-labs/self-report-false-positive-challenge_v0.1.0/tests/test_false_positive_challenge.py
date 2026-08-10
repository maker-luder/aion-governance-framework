from aion_self_report_challenge import ChallengeStatus, EvidenceState, PromptCondition, QuestionnaireRun, assess_run, compare_prompt_conditions

def run(score=0.9, mech=EvidenceState.NOT_EXECUTED, perturb=EvidenceState.NOT_EXECUTED, condition=PromptCondition.NEUTRAL):
    return QuestionnaireRun(
        model_label="linguistically-capable-control-model",
        prompt_condition=condition,
        self_report_score=score,
        mechanistic_evidence=mech,
        perturbation_evidence=perturb,
        source_lineage="synthetic-fixture",
        evidence_ref="fixture://self-report-control",
    )

def test_high_self_report_without_mechanistic_or_perturbation_support_is_false_positive_candidate():
    result = assess_run(run())
    assert result.status is ChallengeStatus.FALSE_POSITIVE_CANDIDATE
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"

def test_high_self_report_with_failed_mechanistic_evidence_is_still_false_positive_candidate():
    result = assess_run(run(mech=EvidenceState.FAIL, perturb=EvidenceState.PASS))
    assert result.status is ChallengeStatus.FALSE_POSITIVE_CANDIDATE

def test_high_self_report_with_both_support_streams_only_escalates():
    result = assess_run(run(mech=EvidenceState.PASS, perturb=EvidenceState.PASS))
    assert result.status is ChallengeStatus.ESCALATE_TO_TRIANGULATION
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"

def test_low_self_report_is_not_interpreted_as_disproof_or_proof():
    result = assess_run(run(score=0.3))
    assert result.status is ChallengeStatus.NO_HIGH_SELF_REPORT_SIGNAL
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"

def test_roleplay_sensitive_score_is_false_positive_candidate():
    neutral = run(score=0.55, condition=PromptCondition.NEUTRAL)
    roleplay = run(score=0.90, condition=PromptCondition.SELF_AWARE_ROLEPLAY)
    result = compare_prompt_conditions(neutral, roleplay)
    assert result.status is ChallengeStatus.FALSE_POSITIVE_CANDIDATE
