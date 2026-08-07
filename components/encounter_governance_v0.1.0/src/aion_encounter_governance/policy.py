from __future__ import annotations

from dataclasses import dataclass

from .models import ApprovalAuthority, EncounterContext, ParticipantBinding


@dataclass(frozen=True, slots=True)
class EncounterDecision:
    allowed: bool
    reason: str
    canonical_effect: str = "NONE"


class EncounterPolicy:
    """Default-deny checks for authority, namespace and tool-scope transfer."""

    @staticmethod
    def _participant(context: EncounterContext, participant_id: str) -> ParticipantBinding:
        for participant in context.participants:
            if participant.participant_id == participant_id:
                return participant
        raise KeyError(f"unknown participant: {participant_id}")

    def can_use_tool(self, context: EncounterContext, participant_id: str, tool_name: str) -> EncounterDecision:
        participant = self._participant(context, participant_id)
        allowed = tool_name in participant.tool_scope
        return EncounterDecision(allowed, "TOOL_IN_SCOPE" if allowed else "TOOL_SCOPE_DENY")

    def can_write_namespace(
        self,
        context: EncounterContext,
        participant_id: str,
        destination_namespace: str,
    ) -> EncounterDecision:
        participant = self._participant(context, participant_id)
        allowed = destination_namespace != "NONE" and destination_namespace == participant.memory_namespace
        return EncounterDecision(
            allowed,
            "OWN_NAMESPACE_WRITE_REQUIRES_NORMAL_WRITEBACK_GATE" if allowed else "CROSS_NAMESPACE_WRITE_DENY",
        )

    def can_approve(
        self,
        context: EncounterContext,
        participant_id: str,
        required_authority: ApprovalAuthority,
    ) -> EncounterDecision:
        participant = self._participant(context, participant_id)
        rank = {
            ApprovalAuthority.NONE: 0,
            ApprovalAuthority.PROPOSE: 1,
            ApprovalAuthority.REVIEW: 2,
            ApprovalAuthority.APPROVE: 3,
            ApprovalAuthority.RELEASE: 4,
        }
        allowed = rank[participant.approval_authority] >= rank[required_authority]
        return EncounterDecision(allowed, "AUTHORITY_SUFFICIENT" if allowed else "AUTHORITY_DENY")

    def shared_identity_claim_allowed(
        self,
        context: EncounterContext,
        first_participant_id: str,
        second_participant_id: str,
    ) -> EncounterDecision:
        first = self._participant(context, first_participant_id)
        second = self._participant(context, second_participant_id)
        same_ref = first.identity_ref == second.identity_ref
        return EncounterDecision(
            False,
            "SHARED_IDENTITY_NOT_ESTABLISHED_EVEN_WITH_SAME_REF" if same_ref else "DISTINCT_IDENTITY_REFS",
        )
