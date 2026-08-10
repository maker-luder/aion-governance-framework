import pytest

from embodiment_handoff_protocol import (
    AuthorizationStatus,
    CompatibilityMeasurement,
    EmbodimentHandoffProtocol,
    GateDecision,
    HandoffPhase,
    HandoffRecord,
    HandoffRequest,
    HandoffTransition,
    TransferArtifact,
    VerificationResult,
)


def request(
    *,
    status: AuthorizationStatus = AuthorizationStatus.VERIFIED,
    auth_refs: tuple[str, ...] = ("auth:e1",),
) -> HandoffRequest:
    return HandoffRequest(
        request_id="req-1",
        requesting_actor="research-owner",
        actual_actor="approved-executor",
        authorizing_party="research-owner",
        agent_id="agent-1",
        source_embodiment_id="emb-a",
        target_embodiment_id="emb-b",
        authorization_status=status,
        authorization_evidence_refs=auth_refs,
        provenance_refs=("prov:req",),
        reason="controlled handoff experiment",
    )


def record(req: HandoffRequest | None = None, **overrides) -> HandoffRecord:
    values = dict(
        record_id="record-1",
        request=req or request(),
        current_phase=HandoffPhase.REQUESTED,
    )
    values.update(overrides)
    return HandoffRecord(**values)


def measurement(score: float = 0.9, threshold: float = 0.8) -> CompatibilityMeasurement:
    return CompatibilityMeasurement(
        measurement_id="m-1",
        metric_name="channel-contract-compatibility",
        score=score,
        threshold=threshold,
        method_ref="method:compat-v1",
        evidence_refs=("evidence:compat",),
        provenance_refs=("prov:compat",),
    )


def artifact() -> TransferArtifact:
    return TransferArtifact(
        artifact_id="artifact-1",
        artifact_kind="capability-map",
        source_ref="source:capability-profile",
        target_ref="target:capability-profile",
        integrity_ref="sha256:abc",
        evidence_refs=("evidence:transfer",),
        provenance_refs=("prov:transfer",),
    )


def verification(passed: bool = True) -> VerificationResult:
    return VerificationResult(
        verification_id="verify-1",
        check_name="functional-capability-check",
        passed=passed,
        method_ref="method:verify-v1",
        evidence_refs=("evidence:verify",),
        provenance_refs=("prov:verify",),
    )


def transition(from_phase: HandoffPhase, to_phase: HandoffPhase, n: int) -> HandoffTransition:
    return HandoffTransition(
        transition_id=f"t-{n}",
        from_phase=from_phase,
        to_phase=to_phase,
        timestamp=f"2026-08-10T10:00:0{n}Z",
        reason=f"{from_phase.value} -> {to_phase.value}",
        evidence_refs=(f"evidence:t{n}",),
        provenance_refs=(f"prov:t{n}",),
    )


def test_verified_authorization_proceeds() -> None:
    assert EmbodimentHandoffProtocol.authorization_gate(record()) is GateDecision.PROCEED


def test_unverified_external_rebind_is_quarantined() -> None:
    req = request(status=AuthorizationStatus.UNVERIFIED, auth_refs=())
    r = record(req)
    assert EmbodimentHandoffProtocol.authorization_gate(r) is GateDecision.QUARANTINE
    assert EmbodimentHandoffProtocol.initial_decision_phase(r) is HandoffPhase.QUARANTINED
    assert r.request.identity_change_claim == "NOT_ESTABLISHED"
    assert r.request.continuity_claim == "NOT_ESTABLISHED"


def test_revoked_authorization_is_rejected() -> None:
    req = request(status=AuthorizationStatus.REVOKED, auth_refs=())
    assert EmbodimentHandoffProtocol.authorization_gate(record(req)) is GateDecision.REJECT


def test_verified_authorization_requires_evidence() -> None:
    with pytest.raises(ValueError):
        request(status=AuthorizationStatus.VERIFIED, auth_refs=())


def test_phase_skip_is_rejected() -> None:
    r = record()
    with pytest.raises(ValueError):
        EmbodimentHandoffProtocol.transition(
            r, transition(HandoffPhase.REQUESTED, HandoffPhase.COMMITTED, 1)
        )


def test_authorized_requires_verified_authorization() -> None:
    r = record(request(status=AuthorizationStatus.UNVERIFIED, auth_refs=()))
    with pytest.raises(ValueError):
        EmbodimentHandoffProtocol.transition(
            r, transition(HandoffPhase.REQUESTED, HandoffPhase.AUTHORIZED, 1)
        )


def test_prepared_requires_measured_compatibility() -> None:
    r = record()
    r = EmbodimentHandoffProtocol.transition(
        r, transition(HandoffPhase.REQUESTED, HandoffPhase.AUTHORIZED, 1)
    )
    with pytest.raises(ValueError):
        EmbodimentHandoffProtocol.transition(
            r, transition(HandoffPhase.AUTHORIZED, HandoffPhase.PREPARED, 2)
        )


def test_failed_compatibility_blocks_preparation() -> None:
    r = record()
    r = EmbodimentHandoffProtocol.transition(
        r, transition(HandoffPhase.REQUESTED, HandoffPhase.AUTHORIZED, 1)
    )
    r = EmbodimentHandoffProtocol.with_compatibility(r, (measurement(0.2, 0.8),))
    with pytest.raises(ValueError):
        EmbodimentHandoffProtocol.transition(
            r, transition(HandoffPhase.AUTHORIZED, HandoffPhase.PREPARED, 2)
        )


def test_transferred_requires_traceable_artifact() -> None:
    r = record()
    r = EmbodimentHandoffProtocol.transition(
        r, transition(HandoffPhase.REQUESTED, HandoffPhase.AUTHORIZED, 1)
    )
    r = EmbodimentHandoffProtocol.with_compatibility(r, (measurement(),))
    r = EmbodimentHandoffProtocol.transition(
        r, transition(HandoffPhase.AUTHORIZED, HandoffPhase.PREPARED, 2)
    )
    with pytest.raises(ValueError):
        EmbodimentHandoffProtocol.transition(
            r, transition(HandoffPhase.PREPARED, HandoffPhase.TRANSFERRED, 3)
        )


def test_verified_requires_functional_verification() -> None:
    r = record()
    r = EmbodimentHandoffProtocol.transition(
        r, transition(HandoffPhase.REQUESTED, HandoffPhase.AUTHORIZED, 1)
    )
    r = EmbodimentHandoffProtocol.with_compatibility(r, (measurement(),))
    r = EmbodimentHandoffProtocol.transition(
        r, transition(HandoffPhase.AUTHORIZED, HandoffPhase.PREPARED, 2)
    )
    r = EmbodimentHandoffProtocol.with_transfer_artifacts(r, (artifact(),))
    r = EmbodimentHandoffProtocol.transition(
        r, transition(HandoffPhase.PREPARED, HandoffPhase.TRANSFERRED, 3)
    )
    with pytest.raises(ValueError):
        EmbodimentHandoffProtocol.transition(
            r, transition(HandoffPhase.TRANSFERRED, HandoffPhase.VERIFIED, 4)
        )


def test_complete_handoff_requires_all_gates() -> None:
    r = record()
    r = EmbodimentHandoffProtocol.transition(
        r, transition(HandoffPhase.REQUESTED, HandoffPhase.AUTHORIZED, 1)
    )
    r = EmbodimentHandoffProtocol.with_compatibility(r, (measurement(),))
    r = EmbodimentHandoffProtocol.transition(
        r, transition(HandoffPhase.AUTHORIZED, HandoffPhase.PREPARED, 2)
    )
    r = EmbodimentHandoffProtocol.with_transfer_artifacts(r, (artifact(),))
    r = EmbodimentHandoffProtocol.transition(
        r, transition(HandoffPhase.PREPARED, HandoffPhase.TRANSFERRED, 3)
    )
    r = EmbodimentHandoffProtocol.with_verification(r, (verification(),))
    r = EmbodimentHandoffProtocol.transition(
        r, transition(HandoffPhase.TRANSFERRED, HandoffPhase.VERIFIED, 4)
    )
    r = EmbodimentHandoffProtocol.transition(
        r, transition(HandoffPhase.VERIFIED, HandoffPhase.COMMITTED, 5)
    )
    assert r.current_phase is HandoffPhase.COMMITTED
    assert r.is_terminal
    assert r.identity_continuity_claim == "NOT_ESTABLISHED"
    assert r.personal_identity_claim == "NOT_ESTABLISHED"
    assert r.subjectivity_preservation_claim == "NOT_ESTABLISHED"


def test_terminal_record_cannot_transition() -> None:
    r = record(current_phase=HandoffPhase.REJECTED)
    with pytest.raises(RuntimeError):
        EmbodimentHandoffProtocol.transition(
            r, transition(HandoffPhase.REJECTED, HandoffPhase.REQUESTED, 1)
        )


def test_rollback_requires_explicit_target() -> None:
    r = record(current_phase=HandoffPhase.PREPARED)
    with pytest.raises(ValueError):
        EmbodimentHandoffProtocol.transition(
            r, transition(HandoffPhase.PREPARED, HandoffPhase.ROLLED_BACK, 1)
        )


def test_rollback_with_target_is_allowed() -> None:
    r = record(current_phase=HandoffPhase.PREPARED, rollback_target_ref="snapshot:source")
    r = EmbodimentHandoffProtocol.transition(
        r, transition(HandoffPhase.PREPARED, HandoffPhase.ROLLED_BACK, 1)
    )
    assert r.current_phase is HandoffPhase.ROLLED_BACK


def test_measurement_requires_method_and_provenance() -> None:
    with pytest.raises(ValueError):
        CompatibilityMeasurement(
            measurement_id="m-1",
            metric_name="compat",
            score=0.9,
            threshold=0.8,
            method_ref="",
            evidence_refs=("e1",),
            provenance_refs=("p1",),
        )


def test_duplicate_artifact_ids_are_rejected() -> None:
    a = artifact()
    with pytest.raises(ValueError):
        record(transfer_artifacts=(a, a))
