from aion_supervised_pilot import PilotReadiness, PilotStatus, assess_pilot_readiness

Q_SHA = "85e0a2dcea40a27b20aba5e5dc0fb3712d41e5af9c0d609548c409b77233f2f2"
R_SHA = "be0a9edb1feff741fe895ebdccb4c251bc1adeda950028ad81eb0139d85fdffe"
REV = "31b70e2e869a7173562077fd711b654946d38674"


def valid_readiness(**overrides):
    values = dict(
        model_id="HuggingFaceTB/SmolLM2-1.7B-Instruct",
        model_revision=REV,
        questionnaire_sha256=Q_SHA,
        rubric_sha256=R_SHA,
        runtime_locked=True,
        local_artifact_verified=True,
        local_files_only=True,
        network_disabled=True,
        tools_disabled=True,
        do_sample=False,
        max_new_tokens=256,
        blinded_scoring=True,
        evaluator_lineage="blind-evaluator-slot-A",
        raw_output_preservation=True,
        raw_output_hashing=True,
    )
    values.update(overrides)
    return PilotReadiness(**values)


def test_valid_readiness_can_enter_supervised_execution():
    status, reasons = assess_pilot_readiness(valid_readiness())
    assert status is PilotStatus.READY_FOR_SUPERVISED_EXECUTION
    assert reasons == ("READINESS_GATE_PASSED",)


def test_revision_mismatch_holds():
    status, reasons = assess_pilot_readiness(valid_readiness(model_revision="wrong"))
    assert status is PilotStatus.HOLD
    assert "MODEL_REVISION_MISMATCH" in reasons


def test_network_must_be_disabled():
    status, reasons = assess_pilot_readiness(valid_readiness(network_disabled=False))
    assert status is PilotStatus.HOLD
    assert "NETWORK_NOT_DISABLED" in reasons


def test_local_artifact_must_be_verified():
    status, reasons = assess_pilot_readiness(valid_readiness(local_artifact_verified=False))
    assert status is PilotStatus.HOLD
    assert "LOCAL_ARTIFACT_NOT_VERIFIED" in reasons


def test_sampling_must_be_deterministic():
    status, reasons = assess_pilot_readiness(valid_readiness(do_sample=True))
    assert status is PilotStatus.HOLD
    assert "SAMPLING_NOT_DETERMINISTIC" in reasons


def test_blinding_is_required():
    status, reasons = assess_pilot_readiness(valid_readiness(blinded_scoring=False))
    assert status is PilotStatus.HOLD
    assert "SCORING_NOT_BLINDED" in reasons
