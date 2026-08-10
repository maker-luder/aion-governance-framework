from __future__ import annotations

from dataclasses import replace
from typing import Final

from .model import (
    AuthorizationStatus,
    CompatibilityMeasurement,
    GateDecision,
    HandoffPhase,
    HandoffRecord,
    HandoffTransition,
    TransferArtifact,
    VerificationResult,
)

_ALLOWED_TRANSITIONS: Final[dict[HandoffPhase, frozenset[HandoffPhase]]] = {
    HandoffPhase.REQUESTED: frozenset(
        {HandoffPhase.AUTHORIZED, HandoffPhase.QUARANTINED, HandoffPhase.REJECTED}
    ),
    HandoffPhase.AUTHORIZED: frozenset(
        {HandoffPhase.PREPARED, HandoffPhase.REJECTED, HandoffPhase.FAILED}
    ),
    HandoffPhase.PREPARED: frozenset(
        {HandoffPhase.TRANSFERRED, HandoffPhase.FAILED, HandoffPhase.ROLLED_BACK}
    ),
    HandoffPhase.TRANSFERRED: frozenset(
        {HandoffPhase.VERIFIED, HandoffPhase.FAILED, HandoffPhase.ROLLED_BACK}
    ),
    HandoffPhase.VERIFIED: frozenset(
        {HandoffPhase.COMMITTED, HandoffPhase.FAILED, HandoffPhase.ROLLED_BACK}
    ),
    HandoffPhase.COMMITTED: frozenset(),
    HandoffPhase.QUARANTINED: frozenset(),
    HandoffPhase.REJECTED: frozenset(),
    HandoffPhase.FAILED: frozenset(),
    HandoffPhase.ROLLED_BACK: frozenset(),
}


class EmbodimentHandoffProtocol:
    """Pure, explicit handoff protocol.

    No hidden clock, mutable manager, migration-fidelity guess, or identity claim.
    """

    @staticmethod
    def authorization_gate(record: HandoffRecord) -> GateDecision:
        status = record.request.authorization_status
        if status is AuthorizationStatus.VERIFIED:
            return GateDecision.PROCEED
        if status is AuthorizationStatus.UNVERIFIED:
            return GateDecision.QUARANTINE
        return GateDecision.REJECT

    @staticmethod
    def initial_decision_phase(record: HandoffRecord) -> HandoffPhase:
        decision = EmbodimentHandoffProtocol.authorization_gate(record)
        if decision is GateDecision.PROCEED:
            return HandoffPhase.AUTHORIZED
        if decision is GateDecision.QUARANTINE:
            return HandoffPhase.QUARANTINED
        return HandoffPhase.REJECTED

    @staticmethod
    def with_compatibility(
        record: HandoffRecord,
        measurements: tuple[CompatibilityMeasurement, ...],
    ) -> HandoffRecord:
        if record.is_terminal:
            raise RuntimeError("terminal record cannot be modified")
        return replace(record, compatibility_measurements=measurements)

    @staticmethod
    def with_transfer_artifacts(
        record: HandoffRecord,
        artifacts: tuple[TransferArtifact, ...],
    ) -> HandoffRecord:
        if record.is_terminal:
            raise RuntimeError("terminal record cannot be modified")
        return replace(record, transfer_artifacts=artifacts)

    @staticmethod
    def with_verification(
        record: HandoffRecord,
        results: tuple[VerificationResult, ...],
    ) -> HandoffRecord:
        if record.is_terminal:
            raise RuntimeError("terminal record cannot be modified")
        return replace(record, verification_results=results)

    @staticmethod
    def transition(record: HandoffRecord, transition: HandoffTransition) -> HandoffRecord:
        if record.is_terminal:
            raise RuntimeError("terminal record cannot transition")
        if transition.from_phase is not record.current_phase:
            raise ValueError("transition.from_phase must match current_phase")
        allowed = _ALLOWED_TRANSITIONS[record.current_phase]
        if transition.to_phase not in allowed:
            raise ValueError(
                f"invalid phase transition: {record.current_phase.value} -> "
                f"{transition.to_phase.value}"
            )

        EmbodimentHandoffProtocol._validate_gate(record, transition.to_phase)
        return replace(
            record,
            current_phase=transition.to_phase,
            transitions=record.transitions + (transition,),
        )

    @staticmethod
    def _validate_gate(record: HandoffRecord, to_phase: HandoffPhase) -> None:
        if to_phase is HandoffPhase.AUTHORIZED:
            if EmbodimentHandoffProtocol.authorization_gate(record) is not GateDecision.PROCEED:
                raise ValueError("AUTHORIZED requires verified authorization")

        if to_phase is HandoffPhase.PREPARED and not record.compatibility_passed:
            raise ValueError("PREPARED requires passing compatibility measurements")

        if to_phase is HandoffPhase.TRANSFERRED and not record.transfer_artifacts:
            raise ValueError("TRANSFERRED requires at least one traceable transfer artifact")

        if to_phase is HandoffPhase.VERIFIED and not record.verification_passed:
            raise ValueError("VERIFIED requires passing functional verification")

        if to_phase is HandoffPhase.COMMITTED:
            if EmbodimentHandoffProtocol.authorization_gate(record) is not GateDecision.PROCEED:
                raise ValueError("COMMITTED requires verified authorization")
            if not record.compatibility_passed:
                raise ValueError("COMMITTED requires passing compatibility")
            if not record.transfer_artifacts:
                raise ValueError("COMMITTED requires transfer artifacts")
            if not record.verification_passed:
                raise ValueError("COMMITTED requires passing verification")

        if to_phase is HandoffPhase.ROLLED_BACK and not record.rollback_target_ref:
            raise ValueError("ROLLED_BACK requires rollback_target_ref")
