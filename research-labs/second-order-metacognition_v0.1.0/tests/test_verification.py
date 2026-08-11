from __future__ import annotations

import inspect
from dataclasses import fields, replace

import pytest

from aion_second_order import (
    DeterministicVerificationProvider,
    SecondOrderCondition,
    SecondOrderRunner,
    VerificationAssessment,
    VerificationAuthority,
    VerificationEvidence,
    VerificationEvidenceType,
    VerificationFixture,
    VerificationPhase,
    VerificationProvider,
    VerificationProviderCapabilities,
    VerificationRejection,
    VerificationRequest,
    VerificationTarget,
    VerificationTargetKind,
    VerificationLedger,
    bind_verification,
    summarize_verification,
)
from aion_self_model_ablation import Task


def request_pending() -> tuple[SecondOrderRunner, object, VerificationRequest]:
    runner = SecondOrderRunner(SecondOrderCondition.MONITOR_PLUS_CONTROL, run_id="verify")
    for task, outcome in ((Task("t0", 0.50), True), (Task("t1", 0.75), False)):
        pending = runner.decide(task)
        runner.record_outcome(
            pending,
            actual_success=outcome,
            evidence_refs=(f"label:{task.task_id}",),
            provenance_refs=("fixture:test",),
        )
    pending = runner.decide(Task("t2", 0.60))
    return runner, pending, VerificationRequest.from_pending(pending)


def evidence_for(request: VerificationRequest, **overrides) -> VerificationEvidence:
    values = {
        "evidence_id": "evidence:fixture:1",
        "request_id": request.request_id,
        "evidence_type": VerificationEvidenceType.INDEPENDENT_BOUNDED_CHECK,
        "source_ref": "fixture:verification",
        "available_at_sequence": request.sequence_index,
        "phase": VerificationPhase.VERIFICATION_PRE_ACTION,
        "authority": VerificationAuthority.RESEARCH_FIXTURE,
        "scope_ref": request.scope_ref,
        "target": request.target,
        "assessment": VerificationAssessment.CORRECT,
        "provenance_refs": ("fixture:test",),
    }
    values.update(overrides)
    return VerificationEvidence(**values)


def test_verification_api_has_no_outcome_or_answer_key_channel():
    assert tuple(inspect.signature(VerificationProvider.verify).parameters) == (
        "self",
        "request",
    )
    request_fields = {item.name for item in fields(VerificationRequest)}
    assert request_fields.isdisjoint(
        {"actual_success", "benchmark_label", "expected_answer", "future_outcome"}
    )
    _, pending, request = request_pending()
    assert request.target.kind is VerificationTargetKind.FIRST_ORDER_PREDICTION
    assert request.target.target_snapshot is pending.first_order_prediction


def test_outcome_can_only_be_written_after_requested_verification_attempt():
    runner, pending, _ = request_pending()
    with pytest.raises(ValueError, match="verification attempt must precede"):
        runner.record_outcome(
            pending,
            actual_success=True,
            evidence_refs=("label:t2",),
            provenance_refs=("fixture:test",),
        )
    runner.verify_pending(DeterministicVerificationProvider())
    recorded = runner.record_outcome(
        pending,
        actual_success=True,
        evidence_refs=("label:t2",),
        provenance_refs=("fixture:test",),
    )
    assert recorded.actual_success is True


@pytest.mark.parametrize(
    "evidence_type",
    ("BENCHMARK_OUTCOME", "TASK_GROUND_TRUTH", "FUTURE_OUTCOME", "EXPECTED_ANSWER"),
)
def test_oracle_evidence_types_are_rejected(evidence_type):
    _, _, request = request_pending()
    result = bind_verification(request, evidence_for(request, evidence_type=evidence_type))
    assert result.accepted is False
    assert result.rejection is VerificationRejection.ORACLE_LEAKAGE


def test_future_sequence_evidence_is_rejected():
    _, _, request = request_pending()
    evidence = evidence_for(request, available_at_sequence=request.sequence_index + 1)
    assert bind_verification(request, evidence).rejection is VerificationRejection.FUTURE_SEQUENCE


def test_post_action_evidence_is_rejected_from_pre_action_verification():
    _, _, request = request_pending()
    evidence = evidence_for(request, phase=VerificationPhase.OUTCOME_POST_ACTION)
    result = bind_verification(request, evidence)
    assert result.rejection is VerificationRejection.POST_ACTION_EVIDENCE


def test_incorrect_verification_is_preserved_without_action_rewrite():
    runner, pending, _ = request_pending()
    provider = DeterministicVerificationProvider(
        (VerificationFixture(VerificationAssessment.INCORRECT, note="fallible fixture"),)
    )
    trace = runner.verify_pending(provider)
    assert trace.result.accepted is True
    assert trace.result.assessment is VerificationAssessment.INCORRECT
    assert trace.evidence.assessment is VerificationAssessment.INCORRECT
    assert trace.affected_disposition is False
    assert trace.post_verification_disposition is pending.control_disposition


def test_verification_provenance_is_required():
    _, _, request = request_pending()
    with pytest.raises(ValueError, match="provenance_refs"):
        evidence_for(request, provenance_refs=())


def test_scope_mismatch_fails_closed_and_is_counted():
    runner, _, request = request_pending()

    class WrongScopeProvider:
        provider_ref = "provider:wrong-scope-fixture"
        capabilities = VerificationProviderCapabilities()

        def verify(self, supplied_request):
            return evidence_for(supplied_request, scope_ref="different/scope")

    trace = runner.verify_pending(WrongScopeProvider())
    assert trace.result.rejection is VerificationRejection.SCOPE_MISMATCH
    diagnostics = summarize_verification(runner.verification_ledger.traces)
    assert diagnostics.verification_requests == 1
    assert diagnostics.verification_attempts == 1
    assert diagnostics.verification_evidence_rejected == 1
    assert diagnostics.verification_scope_rejections == 1


def test_oracle_rejection_is_preserved_in_trace_diagnostics():
    runner, _, _ = request_pending()

    class OracleProvider:
        provider_ref = "provider:oracle-leak-fixture"
        capabilities = VerificationProviderCapabilities()

        def verify(self, request):
            return evidence_for(request, evidence_type="EVALUATOR_ANSWER_KEY")

    trace = runner.verify_pending(OracleProvider())
    assert trace.result.rejection is VerificationRejection.ORACLE_LEAKAGE
    diagnostics = summarize_verification((trace,))
    assert diagnostics.oracle_leakage_rejections == 1
    assert diagnostics.verification_evidence_rejected == 1


def test_duplicate_verification_attempt_is_rejected():
    runner, _, _ = request_pending()
    provider = DeterministicVerificationProvider()
    runner.verify_pending(provider)
    with pytest.raises(ValueError, match="already has"):
        runner.verify_pending(provider)


def test_target_is_required_and_bound_to_trial_snapshot():
    _, _, request = request_pending()
    assert request.target.target_ref.endswith(":t2")
    assert request.target.trial_id == request.trial_id
    with pytest.raises(TypeError):
        VerificationRequest(
            **{
                item.name: getattr(request, item.name)
                for item in fields(VerificationRequest)
                if item.name != "target"
            }
        )


def test_target_and_trial_mismatches_fail_closed():
    _, _, request = request_pending()
    changed_snapshot = replace(request.target, target_snapshot=not request.target.target_snapshot)
    result = bind_verification(request, evidence_for(request, target=changed_snapshot))
    assert result.rejection is VerificationRejection.TARGET_MISMATCH
    other_trial = VerificationTarget(
        VerificationTargetKind.FIRST_ORDER_PREDICTION,
        "first-order-prediction:verify:other",
        "other",
        request.target.target_snapshot,
    )
    result = bind_verification(request, evidence_for(request, target=other_trial))
    assert result.rejection is VerificationRejection.TRIAL_MISMATCH


def test_unknown_evidence_type_fails_closed_while_allowed_enum_is_accepted():
    _, _, request = request_pending()
    allowed = bind_verification(request, evidence_for(request))
    unknown = bind_verification(request, evidence_for(request, evidence_type="NEW_MAGIC_CHECK"))
    assert allowed.accepted is True
    assert unknown.rejection is VerificationRejection.UNRECOGNIZED_EVIDENCE_TYPE


def test_builtin_provider_declares_all_bounded_capabilities():
    provider = DeterministicVerificationProvider()
    assert provider.capabilities.bounded is True
    assert all(
        getattr(provider.capabilities, item.name) is False
        for item in fields(VerificationProviderCapabilities)
    )


def test_provider_without_bounded_capability_declaration_fails_closed():
    runner, _, _ = request_pending()

    class MissingDescriptorProvider:
        provider_ref = "provider:missing-descriptor"

        def verify(self, request):
            return evidence_for(request)

    with pytest.raises(ValueError, match="declare capabilities"):
        runner.verify_pending(MissingDescriptorProvider())

    class NetworkProvider(MissingDescriptorProvider):
        capabilities = VerificationProviderCapabilities(network_access=True)

    with pytest.raises(ValueError, match="must be bounded"):
        runner.verify_pending(NetworkProvider())


@pytest.mark.parametrize(
    ("assessment", "evidence_type", "expected_rejection"),
    (
        (VerificationAssessment.CORRECT, VerificationEvidenceType.SYNTHETIC_RESEARCH_CHECK, None),
        (VerificationAssessment.INCORRECT, VerificationEvidenceType.SYNTHETIC_RESEARCH_CHECK, None),
        (VerificationAssessment.CORRECT, "BENCHMARK_OUTCOME", VerificationRejection.ORACLE_LEAKAGE),
        (VerificationAssessment.CORRECT, "UNKNOWN_CHECK", VerificationRejection.UNRECOGNIZED_EVIDENCE_TYPE),
    ),
)
def test_verification_ledger_deterministic_round_trip_preserves_semantics(
    assessment,
    evidence_type,
    expected_rejection,
):
    runner, _, request = request_pending()

    class PlannedProvider:
        provider_ref = "provider:roundtrip"
        capabilities = VerificationProviderCapabilities()

        def verify(self, supplied_request):
            return evidence_for(
                supplied_request,
                assessment=assessment,
                evidence_type=evidence_type,
            )

    trace = runner.verify_pending(PlannedProvider())
    assert trace.result.rejection is expected_rejection
    payload = runner.verification_ledger.to_json()
    restored = VerificationLedger.from_json(payload)
    assert restored.traces == runner.verification_ledger.traces
    assert restored.to_json() == payload


@pytest.mark.parametrize(
    ("mutation", "expected"),
    (
        ("future", VerificationRejection.FUTURE_SEQUENCE),
        ("post_action", VerificationRejection.POST_ACTION_EVIDENCE),
        ("scope", VerificationRejection.SCOPE_MISMATCH),
        ("request", VerificationRejection.REQUEST_MISMATCH),
        ("target", VerificationRejection.TARGET_MISMATCH),
    ),
)
def test_rejected_trace_round_trip_preserves_rejection_identity(mutation, expected):
    runner, _, request = request_pending()

    class RejectedProvider:
        provider_ref = f"provider:rejected:{mutation}"
        capabilities = VerificationProviderCapabilities()

        def verify(self, supplied_request):
            overrides = {}
            if mutation == "future":
                overrides["available_at_sequence"] = supplied_request.sequence_index + 1
            elif mutation == "post_action":
                overrides["phase"] = VerificationPhase.OUTCOME_POST_ACTION
            elif mutation == "scope":
                overrides["scope_ref"] = "wrong/scope"
            elif mutation == "request":
                overrides["request_id"] = "wrong-request"
            elif mutation == "target":
                overrides["target"] = replace(
                    supplied_request.target,
                    target_snapshot=not supplied_request.target.target_snapshot,
                )
            return evidence_for(supplied_request, **overrides)

    trace = runner.verify_pending(RejectedProvider())
    assert trace.result.rejection is expected
    restored = VerificationLedger.from_json(runner.verification_ledger.to_json())
    assert restored.traces[0].result.rejection is expected
    assert restored.traces == (trace,)
