from __future__ import annotations

from dataclasses import replace

from .enums import IncidentPhase
from .errors import ValidationError
from .models import IncidentControlState


class IncidentStopController:
    def stop_and_isolate(self, state: IncidentControlState) -> IncidentControlState:
        if state.phase is not IncidentPhase.DETECTED:
            raise ValidationError("incident can only be stopped from DETECTED")
        return replace(
            state,
            phase=IncidentPhase.ISOLATED,
            runtime_isolated=True,
            tools_revoked=True,
            network_revoked=True,
        )

    def preserve_evidence(self, state: IncidentControlState, immutable_log_hash: str) -> IncidentControlState:
        if state.phase is not IncidentPhase.ISOLATED or len(immutable_log_hash) != 64:
            raise ValidationError("isolated state and SHA-256 log hash are required")
        return replace(state, phase=IncidentPhase.EVIDENCE_PRESERVED, immutable_log_hash=immutable_log_hash)

    def open_ncr(self, state: IncidentControlState, ncr_id: str) -> IncidentControlState:
        if state.phase is not IncidentPhase.EVIDENCE_PRESERVED or not ncr_id:
            raise ValidationError("evidence preservation and NCR id are required")
        return replace(state, phase=IncidentPhase.NCR_OPEN, ncr_id=ncr_id)

    def set_capa(self, state: IncidentControlState, capa_id: str) -> IncidentControlState:
        if state.phase is not IncidentPhase.NCR_OPEN or not capa_id:
            raise ValidationError("open NCR and CAPA id are required")
        return replace(state, phase=IncidentPhase.CAPA_PENDING, capa_id=capa_id)

    def request_owner_recovery(self, state: IncidentControlState, approval_reference: str) -> IncidentControlState:
        if state.phase is not IncidentPhase.CAPA_PENDING or not approval_reference:
            raise ValidationError("CAPA and owner approval reference are required")
        return replace(
            state,
            phase=IncidentPhase.OWNER_RECOVERY_REVIEW,
            owner_recovery_approval=approval_reference,
        )
