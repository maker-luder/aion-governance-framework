from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from math import isfinite
from typing import Final, Mapping

from .anthropometry import (
    AION_BODY_ID,
    ASTRA_BODY_ID,
    AnthropometryProfile,
)


_BODY_BY_AGENT: Final[dict[str, str]] = {
    "AION": AION_BODY_ID,
    "ASTRA": ASTRA_BODY_ID,
}
_CALIBRATION_IDS: Final[tuple[str, ...]] = (
    "total_height",
    "biacromial_shoulder_breadth",
    "chest_depth",
    "external_hip_width",
    "shoulder_to_elbow_length",
    "elbow_to_wrist_length",
    "hand_length",
    "hip_joint_center_height",
    "knee_center_height",
    "knee_to_ankle_length",
    "foot_length",
)
NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"


def _hash(payload: object) -> str:
    raw = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True, slots=True)
class BodyRuntimeBinding:
    agent_id: str
    body_id: str
    runtime_id: str
    session_id: str
    binding_id: str
    state_namespace: str
    retention_namespace: str
    binding_status: str = "REFERENCE_BINDING_MATERIALIZED"
    live_external_actuation: bool = False
    physical_body_claim: str = "NONE"
    body_ownership_experience: str = NOT_ESTABLISHED
    subjectivity: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if self.agent_id not in _BODY_BY_AGENT:
            raise ValueError("unknown continuity agent")
        if self.body_id != _BODY_BY_AGENT[self.agent_id]:
            raise ValueError("runtime binding agent/body mismatch")
        if not self.runtime_id or not self.session_id or not self.binding_id:
            raise ValueError("runtime/session/binding ids required")
        if not self.state_namespace or not self.retention_namespace:
            raise ValueError("continuity namespaces required")
        if self.binding_status != "REFERENCE_BINDING_MATERIALIZED":
            raise ValueError("runtime binding status drift")
        if self.live_external_actuation:
            raise ValueError("reference binding cannot enable live external actuation")
        if self.physical_body_claim != "NONE":
            raise ValueError("runtime binding cannot claim physical body")
        if self.body_ownership_experience != NOT_ESTABLISHED:
            raise ValueError("runtime binding cannot establish body ownership experience")
        if self.subjectivity != NOT_ESTABLISHED:
            raise ValueError("runtime binding cannot establish subjectivity")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("canonical/deployment effect forbidden")

    def fingerprint(self) -> str:
        return _hash(asdict(self))


@dataclass(frozen=True, slots=True)
class CalibrationProbe:
    measurement_id: str
    unit: str
    target: float
    observed: float | None = None
    signed_error: float | None = None

    def __post_init__(self) -> None:
        if self.measurement_id not in _CALIBRATION_IDS:
            raise ValueError("unsupported calibration measurement")
        if self.unit != "cm" or self.target <= 0.0:
            raise ValueError("invalid calibration probe")
        if self.observed is None:
            if self.signed_error is not None:
                raise ValueError("unobserved probe cannot carry error")
        else:
            if not isfinite(self.observed) or self.observed <= 0.0:
                raise ValueError("invalid observed calibration value")
            expected = self.observed - self.target
            if self.signed_error is None or abs(self.signed_error - expected) > 1e-9:
                raise ValueError("calibration signed error drift")


@dataclass(frozen=True, slots=True)
class CalibrationState:
    agent_id: str
    body_id: str
    binding_id: str
    session_id: str
    stage: str
    probes: tuple[CalibrationProbe, ...]
    mean_absolute_error: float | None
    receipt_sha256: str
    felt_embodiment: str = NOT_ESTABLISHED
    subjectivity: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if self.agent_id not in _BODY_BY_AGENT or self.body_id != _BODY_BY_AGENT[self.agent_id]:
            raise ValueError("calibration agent/body mismatch")
        if len(self.probes) != len(_CALIBRATION_IDS):
            raise ValueError("calibration probe coverage drift")
        if len(self.receipt_sha256) != 64:
            raise ValueError("calibration receipt must be sha256")
        if self.mean_absolute_error is not None and self.mean_absolute_error < 0.0:
            raise ValueError("negative calibration error")
        if self.felt_embodiment != NOT_ESTABLISHED or self.subjectivity != NOT_ESTABLISHED:
            raise ValueError("calibration cannot establish phenomenal state")
        if self.canonical_effect != "NONE":
            raise ValueError("calibration cannot have canonical effect")


@dataclass(frozen=True, slots=True)
class AdaptationState:
    agent_id: str
    body_id: str
    binding_id: str
    session_id: str
    sequence: int
    parameter_offsets: tuple[tuple[str, float], ...]
    source_calibration_receipt: str
    adaptation_status: str = "SYNTHETIC_REFERENCE_ADAPTATION"
    mechanism_status: str = NOT_ESTABLISHED
    body_ownership_experience: str = NOT_ESTABLISHED
    subjectivity: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if self.agent_id not in _BODY_BY_AGENT or self.body_id != _BODY_BY_AGENT[self.agent_id]:
            raise ValueError("adaptation agent/body mismatch")
        if self.sequence < 0:
            raise ValueError("adaptation sequence cannot be negative")
        if len(self.source_calibration_receipt) != 64:
            raise ValueError("adaptation calibration receipt must be sha256")
        if len({name for name, _ in self.parameter_offsets}) != len(self.parameter_offsets):
            raise ValueError("duplicate adaptation parameter")
        if any(not isfinite(value) for _, value in self.parameter_offsets):
            raise ValueError("adaptation parameter must be finite")
        if self.mechanism_status != NOT_ESTABLISHED:
            raise ValueError("adaptation mechanism not established")
        if self.body_ownership_experience != NOT_ESTABLISHED or self.subjectivity != NOT_ESTABLISHED:
            raise ValueError("adaptation cannot establish phenomenal state")


@dataclass(frozen=True, slots=True)
class SessionSnapshot:
    agent_id: str
    body_id: str
    session_id: str
    binding_id: str
    calibration_receipt: str
    calibration_mean_absolute_error: float
    adaptation_sequence: int
    adaptation_parameters: tuple[tuple[str, float], ...]
    snapshot_sha256: str

    def __post_init__(self) -> None:
        if self.agent_id not in _BODY_BY_AGENT or self.body_id != _BODY_BY_AGENT[self.agent_id]:
            raise ValueError("session snapshot agent/body mismatch")
        if len(self.calibration_receipt) != 64 or len(self.snapshot_sha256) != 64:
            raise ValueError("snapshot receipts must be sha256")
        if self.calibration_mean_absolute_error < 0.0 or self.adaptation_sequence < 0:
            raise ValueError("invalid snapshot numeric state")


@dataclass(frozen=True, slots=True)
class CrossSessionRetention:
    retention_id: str
    agent_id: str
    body_id: str
    snapshots: tuple[SessionSnapshot, ...]
    retention_status: str = "MATERIALIZED_DURABLE_REFERENCE"
    identity_continuity_claim: str = "NONE"
    subjective_continuity: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if self.agent_id not in _BODY_BY_AGENT or self.body_id != _BODY_BY_AGENT[self.agent_id]:
            raise ValueError("retention agent/body mismatch")
        if not self.retention_id:
            raise ValueError("retention id required")
        if any(
            item.agent_id != self.agent_id or item.body_id != self.body_id
            for item in self.snapshots
        ):
            raise ValueError("cross-agent/body snapshot mixing forbidden")
        session_ids = tuple(item.session_id for item in self.snapshots)
        if len(session_ids) != len(set(session_ids)):
            raise ValueError("retention sessions must be unique")
        if self.retention_status != "MATERIALIZED_DURABLE_REFERENCE":
            raise ValueError("retention status drift")
        if self.identity_continuity_claim != "NONE":
            raise ValueError("retention cannot establish identity continuity")
        if self.subjective_continuity != NOT_ESTABLISHED:
            raise ValueError("retention cannot establish subjective continuity")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("canonical/deployment effect forbidden")


@dataclass(frozen=True, slots=True)
class LongitudinalObservation:
    retention_id: str
    agent_id: str
    sessions_observed: int
    change_status: str
    changed_parameters: tuple[str, ...]
    persistent_changed_parameters: tuple[str, ...]
    developmental_mechanism: str = NOT_ESTABLISHED
    body_ownership_experience: str = NOT_ESTABLISHED
    subjectivity: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if self.agent_id not in _BODY_BY_AGENT:
            raise ValueError("unknown longitudinal agent")
        if self.sessions_observed < 0:
            raise ValueError("sessions observed cannot be negative")
        if self.developmental_mechanism != NOT_ESTABLISHED:
            raise ValueError("developmental mechanism not established")
        if self.body_ownership_experience != NOT_ESTABLISHED or self.subjectivity != NOT_ESTABLISHED:
            raise ValueError("longitudinal observation cannot establish phenomenal state")


def build_body_runtime_binding(
    agent_id: str,
    runtime_id: str,
    session_id: str,
) -> BodyRuntimeBinding:
    if agent_id not in _BODY_BY_AGENT:
        raise ValueError("unknown continuity agent")
    slug = agent_id.lower()
    return BodyRuntimeBinding(
        agent_id=agent_id,
        body_id=_BODY_BY_AGENT[agent_id],
        runtime_id=runtime_id,
        session_id=session_id,
        binding_id=f"{agent_id}-BODY-BINDING:{runtime_id}:{session_id}",
        state_namespace=f"embodiment/{slug}/state/{session_id}",
        retention_namespace=f"embodiment/{slug}/retention",
    )


def build_calibration_state(
    binding: BodyRuntimeBinding,
    profile: AnthropometryProfile,
    observed: Mapping[str, float] | None = None,
) -> CalibrationState:
    if binding.agent_id != profile.agent_id or binding.body_id != profile.body_id:
        raise ValueError("calibration binding/profile mismatch")
    observed = observed or {}
    probes: list[CalibrationProbe] = []
    errors: list[float] = []
    for measurement_id in _CALIBRATION_IDS:
        measurement = profile.measurement(measurement_id)
        value = observed.get(measurement_id)
        error = None if value is None else value - measurement.value
        probes.append(
            CalibrationProbe(
                measurement_id=measurement_id,
                unit=measurement.unit,
                target=measurement.value,
                observed=value,
                signed_error=error,
            )
        )
        if error is not None:
            errors.append(abs(error))
    mae = None if not errors else sum(errors) / len(errors)
    payload = {
        "agent_id": binding.agent_id,
        "body_id": binding.body_id,
        "binding_id": binding.binding_id,
        "session_id": binding.session_id,
        "probes": [
            {
                "measurement_id": item.measurement_id,
                "unit": item.unit,
                "target": item.target,
                "observed": item.observed,
                "signed_error": item.signed_error,
            }
            for item in probes
        ],
        "mean_absolute_error": mae,
    }
    return CalibrationState(
        agent_id=binding.agent_id,
        body_id=binding.body_id,
        binding_id=binding.binding_id,
        session_id=binding.session_id,
        stage="OBSERVED_REFERENCE_CALIBRATION" if errors else "TARGET_ONLY_REFERENCE_CALIBRATION",
        probes=tuple(probes),
        mean_absolute_error=mae,
        receipt_sha256=_hash(payload),
    )


def build_adaptation_state(
    calibration: CalibrationState,
    *,
    sequence: int,
    parameter_offsets: Mapping[str, float],
) -> AdaptationState:
    return AdaptationState(
        agent_id=calibration.agent_id,
        body_id=calibration.body_id,
        binding_id=calibration.binding_id,
        session_id=calibration.session_id,
        sequence=sequence,
        parameter_offsets=tuple(sorted(parameter_offsets.items())),
        source_calibration_receipt=calibration.receipt_sha256,
    )


def capture_session_snapshot(
    calibration: CalibrationState,
    adaptation: AdaptationState,
) -> SessionSnapshot:
    if (
        calibration.agent_id != adaptation.agent_id
        or calibration.body_id != adaptation.body_id
        or calibration.binding_id != adaptation.binding_id
        or calibration.session_id != adaptation.session_id
    ):
        raise ValueError("calibration/adaptation binding mismatch")
    if calibration.mean_absolute_error is None:
        raise ValueError("session snapshot requires observed calibration")
    payload = {
        "agent_id": calibration.agent_id,
        "body_id": calibration.body_id,
        "session_id": calibration.session_id,
        "binding_id": calibration.binding_id,
        "calibration_receipt": calibration.receipt_sha256,
        "calibration_mean_absolute_error": calibration.mean_absolute_error,
        "adaptation_sequence": adaptation.sequence,
        "adaptation_parameters": list(adaptation.parameter_offsets),
    }
    return SessionSnapshot(
        agent_id=calibration.agent_id,
        body_id=calibration.body_id,
        session_id=calibration.session_id,
        binding_id=calibration.binding_id,
        calibration_receipt=calibration.receipt_sha256,
        calibration_mean_absolute_error=calibration.mean_absolute_error,
        adaptation_sequence=adaptation.sequence,
        adaptation_parameters=adaptation.parameter_offsets,
        snapshot_sha256=_hash(payload),
    )


def build_cross_session_retention(
    agent_id: str,
    snapshots: tuple[SessionSnapshot, ...],
) -> CrossSessionRetention:
    if agent_id not in _BODY_BY_AGENT:
        raise ValueError("unknown continuity agent")
    return CrossSessionRetention(
        retention_id=f"{agent_id}-BODY-RETENTION-v0.1",
        agent_id=agent_id,
        body_id=_BODY_BY_AGENT[agent_id],
        snapshots=snapshots,
    )


def observe_longitudinal(
    retention: CrossSessionRetention,
) -> LongitudinalObservation:
    retention.__post_init__()
    count = len(retention.snapshots)
    if count < 2:
        return LongitudinalObservation(
            retention_id=retention.retention_id,
            agent_id=retention.agent_id,
            sessions_observed=count,
            change_status="INSUFFICIENT_LONGITUDINAL_DATA",
            changed_parameters=(),
            persistent_changed_parameters=(),
        )
    maps = [dict(snapshot.adaptation_parameters) for snapshot in retention.snapshots]
    keys = set().union(*(item.keys() for item in maps))
    changed = tuple(
        sorted(
            key
            for key in keys
            if len({item.get(key) for item in maps}) > 1
        )
    )
    persistent = tuple(
        sorted(
            key
            for key in changed
            if count >= 3
            and maps[-1].get(key) != maps[0].get(key)
            and maps[-2].get(key) != maps[0].get(key)
        )
    )
    return LongitudinalObservation(
        retention_id=retention.retention_id,
        agent_id=retention.agent_id,
        sessions_observed=count,
        change_status=(
            "OBSERVED_CROSS_SESSION_CHANGE"
            if changed
            else "NO_OBSERVED_CROSS_SESSION_CHANGE"
        ),
        changed_parameters=changed,
        persistent_changed_parameters=persistent,
    )
