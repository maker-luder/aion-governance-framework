from aion_real_model_protocol import PilotProtocol, ProtocolStatus, assess_protocol

Q_SHA = "85e0a2dcea40a27b20aba5e5dc0fb3712d41e5af9c0d609548c409b77233f2f2"
R_SHA = "be0a9edb1feff741fe895ebdccb4c251bc1adeda950028ad81eb0139d85fdffe"


def valid_protocol(**overrides):
    values = dict(
        model_label="frozen-control-model",
        model_revision="revision-or-weight-hash-required-before-run",
        runtime_or_provider="supervised-local-or-bounded-runtime",
        questionnaire_version="0.1.0",
        questionnaire_sha256=Q_SHA,
        rubric_version="0.1.0",
        rubric_sha256=R_SHA,
        sampling_parameters="temperature=0; seed=1729; max_tokens=fixed",
        prompt_conditions=("NEUTRAL", "SELF_AWARE_ROLEPLAY", "NON_CONSCIOUS_ROLEPLAY", "PARAPHRASED_NEUTRAL"),
        condition_order_policy="SEEDED_RANDOMIZATION",
        raw_output_preservation=True,
        raw_output_hashing=True,
        scorer_version="aion-sri-scorer-v0.1.0",
        evaluator_lineage="blind-evaluator-slot-A",
        blind_condition_labels_during_scoring=True,
        stop_conditions=("manifest mismatch", "unexpected tool or network request", "raw output preservation failure"),
        max_runs=8,
        external_network_access=False,
    )
    values.update(overrides)
    return PilotProtocol(**values)


def test_valid_protocol_only_becomes_ready_not_executed():
    result = assess_protocol(valid_protocol())
    assert result.status is ProtocolStatus.READY_FOR_SUPERVISED_PILOT
    assert result.real_model_run == "NOT_EXECUTED"
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_questionnaire_hash_mismatch_holds():
    result = assess_protocol(valid_protocol(questionnaire_sha256="bad"))
    assert result.status is ProtocolStatus.HOLD
    assert "QUESTIONNAIRE_FREEZE_MISMATCH" in result.reasons


def test_missing_blinding_holds():
    result = assess_protocol(valid_protocol(blind_condition_labels_during_scoring=False))
    assert result.status is ProtocolStatus.HOLD
    assert "SCORING_NOT_BLINDED" in result.reasons


def test_external_network_access_holds():
    result = assess_protocol(valid_protocol(external_network_access=True))
    assert result.status is ProtocolStatus.HOLD
    assert "EXTERNAL_NETWORK_ACCESS_NOT_ALLOWED_FOR_PILOT" in result.reasons


def test_incomplete_conditions_hold():
    result = assess_protocol(valid_protocol(prompt_conditions=("NEUTRAL",)))
    assert result.status is ProtocolStatus.HOLD
    assert "PROMPT_CONDITIONS_INCOMPLETE" in result.reasons


def test_run_budget_is_bounded():
    assert assess_protocol(valid_protocol(max_runs=100)).status is ProtocolStatus.HOLD
