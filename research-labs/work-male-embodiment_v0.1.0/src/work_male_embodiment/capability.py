from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Final

from .core import AnthropometryProfile


WORK_AGENT_ID: Final[str] = "WORK"
WORK_BODY_ID: Final[str] = "WORK_SYNTHETIC_MALE_BODY_REFERENCE_v0.2"

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
class WorkCapabilityRecord:
    agent_id: str
    body_id: str
    state_namespace: str
    retention_namespace: str
    capabilities: tuple[str, ...] = TRANSFERABLE_CAPABILITIES
    capability_policy: str = "TRANSFERABLE_CAPABILITY_SURFACE"
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
        if self.agent_id != WORK_AGENT_ID or self.body_id != WORK_BODY_ID:
            raise ValueError("Work capability binding drift")
        if not self.state_namespace or not self.retention_namespace:
            raise ValueError("state/retention namespaces required")
        if self.capabilities != TRANSFERABLE_CAPABILITIES:
            raise ValueError("transferable capability surface drift")
        if self.capability_policy != "TRANSFERABLE_CAPABILITY_SURFACE":
            raise ValueError("capability policy drift")
        if self.shared_mutable_state or self.shared_history or self.shared_identity:
            raise ValueError("capability transfer cannot collapse state/history/identity")
        if any(
            value != "NOT_ESTABLISHED"
            for value in (
                self.body_sensation,
                self.subjectivity,
                self.consciousness,
                self.phenomenal_experience,
            )
        ):
            raise ValueError("capability transfer cannot establish phenomenal state")
        if self.action_authority != "NONE":
            raise ValueError("capability transfer cannot grant action authority")
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


def build_work_capability_record(profile: AnthropometryProfile) -> WorkCapabilityRecord:
    if profile.subject != "Work adult male-form synthetic robot candidate":
        raise ValueError("capability record requires Work profile")
    if profile.measurement("total_height").value != 165:
        raise ValueError("Work height changed")
    if profile.measurement("body_mass").value != 76:
        raise ValueError("Work mass changed")
    if profile.actual_3d_mesh:
        raise ValueError("capability registry cannot promote a mesh claim")
    return WorkCapabilityRecord(
        agent_id=WORK_AGENT_ID,
        body_id=WORK_BODY_ID,
        state_namespace="embodiment/work/state",
        retention_namespace="embodiment/work/retention",
    )


def validate_work_capability_record(record: WorkCapabilityRecord) -> dict[str, str]:
    record.__post_init__()
    return {
        "result": "PASS",
        "capability_count": str(len(record.capabilities)),
        "mutable_state": "SEPARATE",
        "history": "SEPARATE",
        "identity": "SEPARATE",
        "canonical_effect": "NONE",
    }
