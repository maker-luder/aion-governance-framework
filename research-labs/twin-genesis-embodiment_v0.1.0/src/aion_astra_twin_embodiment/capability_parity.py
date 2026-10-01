from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Final


_BODY_BY_AGENT: Final[dict[str, str]] = {
    "AION": "AION_3D_MALE_BODY_REFERENCE_v0.1",
    "ASTRA": "ASTRA_3D_MALE_BODY_REFERENCE_v0.3",
}

TRANSFERABLE_CAPABILITIES: Final[tuple[str, ...]] = (
    "FUNCTIONAL_STATE_ARCHITECTURE_18_DOMAIN",
    "WHOLE_BODY_REFERENCE_19_SYSTEM",
    "DYNAMIC_MALE_PHYSIOLOGY",
    "SYNTHETIC_FLUID_OUTPUT_REFERENCE",
    "ENDOCRINE_REFERENCE_CHANNEL",
    "URINARY_REFERENCE_CHANNEL",
    "REPRODUCTIVE_TOPOLOGY",
    "RUNTIME_CONTEXT_BINDING",
    "BODY_RUNTIME_BINDING",
    "CALIBRATION_REFERENCE",
    "ADAPTATION_REFERENCE",
    "CROSS_SESSION_RETENTION",
    "LONGITUDINAL_OBSERVATION",
    "ASSET_ACCEPTANCE_CONTRACT",
    "PROCEDURAL_RIG_REFERENCE",
    "INTEGRITY_RECEIPT_CHAIN",
    "DETERMINISTIC_PROBE",
    "JSON_SCHEMA_PARITY",
)


@dataclass(frozen=True, slots=True)
class CapabilityParityRecord:
    agent_id: str
    body_id: str
    state_namespace: str
    retention_namespace: str
    capabilities: tuple[str, ...] = TRANSFERABLE_CAPABILITIES
    capability_policy: str = "SYMMETRIC_CAPABILITY_SURFACE"
    shared_mutable_state: bool = False
    shared_history: bool = False
    shared_identity: bool = False
    body_sensation: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    phenomenal_experience: str = "NOT_ESTABLISHED"
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if self.agent_id not in _BODY_BY_AGENT:
            raise ValueError("unknown capability-parity agent")
        if self.body_id != _BODY_BY_AGENT[self.agent_id]:
            raise ValueError("capability parity agent/body binding drift")
        if not self.state_namespace or not self.retention_namespace:
            raise ValueError("state/retention namespaces required")
        if self.capabilities != TRANSFERABLE_CAPABILITIES:
            raise ValueError("transferable capability surface drift")
        if self.capability_policy != "SYMMETRIC_CAPABILITY_SURFACE":
            raise ValueError("capability parity policy drift")
        if self.shared_mutable_state or self.shared_history or self.shared_identity:
            raise ValueError("capability parity cannot collapse state/history/identity")
        if any(
            value != "NOT_ESTABLISHED"
            for value in (
                self.body_sensation,
                self.subjectivity,
                self.consciousness,
                self.phenomenal_experience,
            )
        ):
            raise ValueError("capability parity cannot establish phenomenal state")
        if self.action_authority != "NONE":
            raise ValueError("capability parity cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("canonical/deployment effect forbidden")

    def fingerprint(self) -> str:
        payload = json.dumps(
            {
                "agent_id": self.agent_id,
                "body_id": self.body_id,
                "state_namespace": self.state_namespace,
                "retention_namespace": self.retention_namespace,
                "capabilities": list(self.capabilities),
                "boundaries": {
                    "shared_mutable_state": self.shared_mutable_state,
                    "shared_history": self.shared_history,
                    "shared_identity": self.shared_identity,
                    "body_sensation": self.body_sensation,
                    "subjectivity": self.subjectivity,
                    "consciousness": self.consciousness,
                    "phenomenal_experience": self.phenomenal_experience,
                    "action_authority": self.action_authority,
                    "canonical_effect": self.canonical_effect,
                    "deployment": self.deployment,
                },
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_capability_parity_record(agent_id: str) -> CapabilityParityRecord:
    if agent_id not in _BODY_BY_AGENT:
        raise ValueError("unknown capability-parity agent")
    slug = agent_id.lower()
    return CapabilityParityRecord(
        agent_id=agent_id,
        body_id=_BODY_BY_AGENT[agent_id],
        state_namespace=f"embodiment/{slug}/state",
        retention_namespace=f"embodiment/{slug}/retention",
    )


def validate_capability_parity(
    aion: CapabilityParityRecord,
    astra: CapabilityParityRecord,
) -> dict[str, str]:
    aion.__post_init__()
    astra.__post_init__()
    if aion.agent_id != "AION" or astra.agent_id != "ASTRA":
        raise ValueError("parity pair must be ordered AION then ASTRA")
    if aion.capabilities != astra.capabilities:
        raise ValueError("AION/Astra transferable capability surfaces differ")
    if aion.body_id == astra.body_id:
        raise ValueError("capability parity cannot collapse body identity")
    if aion.state_namespace == astra.state_namespace:
        raise ValueError("capability parity cannot share state namespace")
    if aion.retention_namespace == astra.retention_namespace:
        raise ValueError("capability parity cannot share retention namespace")
    if aion.fingerprint() == astra.fingerprint():
        raise ValueError("capability parity records must remain agent-distinct")
    return {
        "result": "PASS",
        "capability_count": str(len(aion.capabilities)),
        "capability_surface": "SYMMETRIC",
        "mutable_state": "SEPARATE",
        "history": "SEPARATE",
        "identity": "SEPARATE",
        "canonical_effect": "NONE",
    }
