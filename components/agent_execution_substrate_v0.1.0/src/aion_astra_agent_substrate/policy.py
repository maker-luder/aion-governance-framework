"""Fail-closed governance policy for substrate capabilities."""

from __future__ import annotations

from .models import Capability, Decision, PolicyDecision, PolicyRequest


OBSERVATION_CAPABILITIES = frozenset(
    {
        Capability.SESSION_READ,
        Capability.SANDBOX_READ,
        Capability.STORAGE_READ,
        Capability.PLUGIN_INSPECT,
        Capability.UI_RENDER,
        Capability.TRAJECTORY_EXPORT,
    }
)

MUTATING_OR_EXECUTING_CAPABILITIES = frozenset(set(Capability) - OBSERVATION_CAPABILITIES)


def evaluate(request: PolicyRequest) -> PolicyDecision:
    reasons: list[str] = []

    if request.canonical_effect != "NONE":
        reasons.append("canonical effects are not admitted")
    if request.deployment:
        reasons.append("deployment is not admitted by substrate v0.1.0")
    if request.network_access:
        reasons.append("network access is not admitted by substrate v0.1.0")

    if request.capability in MUTATING_OR_EXECUTING_CAPABILITIES:
        if not request.owner_approved:
            reasons.append("explicit Owner approval is required for mutating or executing capability")
        if not (request.authority_reference or "").strip():
            reasons.append("authority_reference is required for mutating or executing capability")

    if request.capability in {Capability.PLUGIN_MOUNT, Capability.AGENT_LOOP_REPLACE}:
        if request.self_requested or request.plugin_generated:
            if not request.owner_approved:
                reasons.append("self-composition does not grant self-authorization")

    decision = Decision.HOLD if reasons else Decision.ALLOW
    return PolicyDecision(
        decision=decision,
        capability=request.capability,
        reasons=tuple(reasons),
    )
