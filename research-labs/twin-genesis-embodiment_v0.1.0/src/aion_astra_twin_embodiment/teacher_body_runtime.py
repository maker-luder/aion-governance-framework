from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from hashlib import sha256
import json
from pathlib import Path
from math import isfinite
from typing import Any, Mapping

from .physiology import (
    build_adult_male_physiology_reference,
    validate_adult_male_physiology_reference,
)
from .teacher_anthropometry import (
    TeacherAnthropometryProfile,
    build_teacher_anthropometry_profile,
)
from .teacher_body_channels import (
    TeacherBodySignalSchema,
    TeacherMotorControlSchema,
    build_teacher_body_signal_schema,
    build_teacher_motor_control_schema,
)
from .teacher_body_dynamics import (
    TeacherBodyDynamicsProfile,
    build_teacher_body_dynamics_profile,
    validate_teacher_body_dynamics_profile,
)
from .teacher_embodiment_research import (
    TeacherEmbodimentResearchSurface,
    build_teacher_embodiment_research_surface,
    validate_teacher_embodiment_research_surface,
)


NOT_ESTABLISHED = "NOT_ESTABLISHED"


def _canonical_hash(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class TeacherBodyRuntimeBinding:
    binding_id: str
    runtime_id: str
    session_id: str
    body_id: str
    anthropometry_profile_id: str
    physiology_profile_id: str
    signal_schema_id: str
    motor_schema_id: str
    body_dynamics_profile_id: str
    research_surface_id: str
    skeleton_root: str
    viewpoint_anchor: str
    binding_status: str
    live_external_actuation: bool
    physical_body_claim: str = "NONE"
    body_ownership_experience_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CalibrationProbe:
    measurement_id: str
    unit: str
    target: float
    observed: float | None = None
    signed_error: float | None = None


@dataclass(frozen=True, slots=True)
class TeacherCalibrationState:
    binding_id: str
    session_id: str
    stage: str
    probes: tuple[CalibrationProbe, ...]
    sensor_baseline_status: str
    motor_mapping_status: str
    mean_absolute_error: float | None
    receipt_sha256: str
    felt_embodiment_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["probes"] = [asdict(probe) for probe in self.probes]
        return payload


@dataclass(frozen=True, slots=True)
class TeacherAdaptationState:
    binding_id: str
    session_id: str
    sequence: int
    parameter_offsets: tuple[tuple[str, float], ...]
    source_calibration_receipt: str
    adaptation_status: str
    mechanism_status: str = NOT_ESTABLISHED
    body_ownership_experience_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["parameter_offsets"] = [list(item) for item in self.parameter_offsets]
        return payload


@dataclass(frozen=True, slots=True)
class TeacherSessionSnapshot:
    session_id: str
    binding_id: str
    calibration_receipt: str
    calibration_mean_absolute_error: float
    adaptation_sequence: int
    adaptation_parameters: tuple[tuple[str, float], ...]
    snapshot_sha256: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["adaptation_parameters"] = [list(item) for item in self.adaptation_parameters]
        return payload


@dataclass(frozen=True, slots=True)
class TeacherCrossSessionRetention:
    retention_id: str
    body_id: str
    snapshots: tuple[TeacherSessionSnapshot, ...]
    retention_status: str = "MATERIALIZED_DURABLE_REFERENCE"
    identity_continuity_claim: str = "NONE"
    subjective_continuity_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["snapshots"] = [snapshot.to_dict() for snapshot in self.snapshots]
        return payload


@dataclass(frozen=True, slots=True)
class TeacherRetentionReceipt:
    path: str
    file_sha256: str
    payload_sha256: str
    snapshot_count: int


_CALIBRATION_IDS = (
    "total_height",
    "biacromial_shoulder_breadth",
    "interpupillary_distance",
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


def build_teacher_body_runtime_binding(
    runtime_id: str,
    session_id: str,
) -> TeacherBodyRuntimeBinding:
    if not runtime_id or not session_id:
        raise ValueError("runtime_id and session_id are required")

    anthropometry = build_teacher_anthropometry_profile()
    physiology = build_adult_male_physiology_reference(anthropometry.body_id)
    validate_adult_male_physiology_reference(physiology)
    signals = build_teacher_body_signal_schema()
    motor = build_teacher_motor_control_schema()
    dynamics = build_teacher_body_dynamics_profile(signals)
    research = build_teacher_embodiment_research_surface()
    binding = TeacherBodyRuntimeBinding(
        binding_id=f"TEACHER-BINDING:{runtime_id}:{session_id}",
        runtime_id=runtime_id,
        session_id=session_id,
        body_id=anthropometry.body_id,
        anthropometry_profile_id=anthropometry.profile_id,
        physiology_profile_id=physiology.profile_id,
        signal_schema_id=signals.schema_id,
        motor_schema_id=motor.schema_id,
        body_dynamics_profile_id=dynamics.profile_id,
        research_surface_id=research.surface_id,
        skeleton_root="hips",
        viewpoint_anchor="head",
        binding_status="REFERENCE_BINDING_MATERIALIZED",
        live_external_actuation=False,
    )
    validate_teacher_body_runtime_binding(
        binding,
        anthropometry,
        signals,
        motor,
        dynamics,
        research,
    )
    return binding


def validate_teacher_body_runtime_binding(
    binding: TeacherBodyRuntimeBinding,
    anthropometry: TeacherAnthropometryProfile | None = None,
    signals: TeacherBodySignalSchema | None = None,
    motor: TeacherMotorControlSchema | None = None,
    dynamics: TeacherBodyDynamicsProfile | None = None,
    research: TeacherEmbodimentResearchSurface | None = None,
) -> dict[str, str]:
    anthropometry = anthropometry or build_teacher_anthropometry_profile()
    signals = signals or build_teacher_body_signal_schema()
    motor = motor or build_teacher_motor_control_schema()
    dynamics = dynamics or build_teacher_body_dynamics_profile(signals)
    research = research or build_teacher_embodiment_research_surface()
    validate_teacher_body_dynamics_profile(dynamics, signals)
    validate_teacher_embodiment_research_surface(research)

    if binding.body_id != anthropometry.body_id:
        raise ValueError("body runtime binding body id drift")
    if binding.anthropometry_profile_id != anthropometry.profile_id:
        raise ValueError("body runtime anthropometry profile drift")
    physiology = build_adult_male_physiology_reference(anthropometry.body_id)
    validate_adult_male_physiology_reference(physiology)
    if binding.physiology_profile_id != physiology.profile_id:
        raise ValueError("body runtime physiology profile drift")
    if binding.signal_schema_id != signals.schema_id:
        raise ValueError("body runtime signal schema drift")
    if binding.motor_schema_id != motor.schema_id:
        raise ValueError("body runtime motor schema drift")
    if binding.body_dynamics_profile_id != dynamics.profile_id:
        raise ValueError("body runtime dynamics profile drift")
    if binding.research_surface_id != research.surface_id:
        raise ValueError("body runtime research surface drift")
    if binding.skeleton_root != "hips" or binding.viewpoint_anchor != "head":
        raise ValueError("body runtime skeletal/viewpoint anchor drift")
    if binding.binding_status != "REFERENCE_BINDING_MATERIALIZED":
        raise ValueError("body runtime reference binding is not materialized")
    if binding.live_external_actuation:
        raise ValueError("reference binding cannot self-enable live external actuation")
    if binding.body_ownership_experience_status != NOT_ESTABLISHED:
        raise ValueError("runtime binding cannot establish body ownership experience")
    if binding.subjectivity_status != NOT_ESTABLISHED:
        raise ValueError("runtime binding cannot establish subjectivity")
    if binding.physical_body_claim != "NONE":
        raise ValueError("runtime binding cannot claim a physical body")
    if binding.canonical_effect != "NONE" or binding.deployment:
        raise ValueError("runtime binding must remain non-canonical and undeployed")

    return {
        "result": "PASS",
        "anthropometry_binding": "PASS",
        "physiology_binding": "PASS",
        "signal_binding": "PASS",
        "motor_binding": "PASS",
        "body_dynamics_binding": "PASS",
        "research_surface_binding": "PASS",
        "live_external_actuation": "DISABLED",
        "phenomenal_nonclaim": "PASS",
    }


def initialize_teacher_calibration(
    binding: TeacherBodyRuntimeBinding,
) -> TeacherCalibrationState:
    validate_teacher_body_runtime_binding(binding)
    profile = build_teacher_anthropometry_profile()
    measurements = profile.measurement_map()
    probes = tuple(
        CalibrationProbe(
            measurement_id=measurement_id,
            unit=measurements[measurement_id].unit,
            target=measurements[measurement_id].nominal,
        )
        for measurement_id in _CALIBRATION_IDS
    )
    payload = {
        "binding_id": binding.binding_id,
        "session_id": binding.session_id,
        "stage": "INITIALIZED_UNCALIBRATED",
        "probes": [asdict(probe) for probe in probes],
    }
    return TeacherCalibrationState(
        binding_id=binding.binding_id,
        session_id=binding.session_id,
        stage="INITIALIZED_UNCALIBRATED",
        probes=probes,
        sensor_baseline_status="INITIALIZED",
        motor_mapping_status="INITIALIZED",
        mean_absolute_error=None,
        receipt_sha256=_canonical_hash(payload),
    )


def apply_teacher_calibration_observations(
    state: TeacherCalibrationState,
    observations: Mapping[str, float],
) -> TeacherCalibrationState:
    expected = {probe.measurement_id for probe in state.probes}
    if set(observations) != expected:
        missing = sorted(expected - set(observations))
        extra = sorted(set(observations) - expected)
        raise ValueError(
            f"calibration observations must cover every probe: missing={missing}, extra={extra}"
        )

    probes = tuple(
        replace(
            probe,
            observed=float(observations[probe.measurement_id]),
            signed_error=float(observations[probe.measurement_id]) - probe.target,
        )
        for probe in state.probes
    )
    mean_error = sum(abs(probe.signed_error or 0.0) for probe in probes) / len(probes)
    payload = {
        "binding_id": state.binding_id,
        "session_id": state.session_id,
        "stage": "CALIBRATED_REFERENCE",
        "probes": [asdict(probe) for probe in probes],
        "mean_absolute_error": mean_error,
    }
    return TeacherCalibrationState(
        binding_id=state.binding_id,
        session_id=state.session_id,
        stage="CALIBRATED_REFERENCE",
        probes=probes,
        sensor_baseline_status="RECORDED_REFERENCE",
        motor_mapping_status="CALIBRATED_REFERENCE",
        mean_absolute_error=mean_error,
        receipt_sha256=_canonical_hash(payload),
    )


def update_teacher_adaptation(
    calibration: TeacherCalibrationState,
    previous: TeacherAdaptationState | None = None,
) -> TeacherAdaptationState:
    if calibration.stage != "CALIBRATED_REFERENCE":
        raise ValueError("adaptation requires a completed reference calibration")
    if any(probe.signed_error is None for probe in calibration.probes):
        raise ValueError("adaptation requires observed calibration errors")

    offsets = tuple(
        sorted(
            (
                probe.measurement_id,
                -(probe.signed_error or 0.0),
            )
            for probe in calibration.probes
        )
    )
    sequence = 1 if previous is None else previous.sequence + 1
    return TeacherAdaptationState(
        binding_id=calibration.binding_id,
        session_id=calibration.session_id,
        sequence=sequence,
        parameter_offsets=offsets,
        source_calibration_receipt=calibration.receipt_sha256,
        adaptation_status="OBSERVED_CALIBRATION_ADAPTATION",
    )


def build_teacher_session_snapshot(
    calibration: TeacherCalibrationState,
    adaptation: TeacherAdaptationState,
) -> TeacherSessionSnapshot:
    if calibration.stage != "CALIBRATED_REFERENCE":
        raise ValueError("session snapshot requires completed calibration")
    if calibration.mean_absolute_error is None:
        raise ValueError("session snapshot requires calibration error summary")
    if adaptation.source_calibration_receipt != calibration.receipt_sha256:
        raise ValueError("adaptation/calibration receipt mismatch")
    if adaptation.binding_id != calibration.binding_id:
        raise ValueError("adaptation/calibration binding mismatch")

    payload = {
        "session_id": calibration.session_id,
        "binding_id": calibration.binding_id,
        "calibration_receipt": calibration.receipt_sha256,
        "calibration_mean_absolute_error": calibration.mean_absolute_error,
        "adaptation_sequence": adaptation.sequence,
        "adaptation_parameters": [list(item) for item in adaptation.parameter_offsets],
    }
    return TeacherSessionSnapshot(
        session_id=calibration.session_id,
        binding_id=calibration.binding_id,
        calibration_receipt=calibration.receipt_sha256,
        calibration_mean_absolute_error=calibration.mean_absolute_error,
        adaptation_sequence=adaptation.sequence,
        adaptation_parameters=adaptation.parameter_offsets,
        snapshot_sha256=_canonical_hash(payload),
    )


def validate_teacher_session_snapshot(
    snapshot: TeacherSessionSnapshot,
) -> dict[str, str]:
    if not snapshot.session_id or not snapshot.binding_id:
        raise ValueError("retained snapshot requires explicit session and binding ids")
    if snapshot.calibration_mean_absolute_error < 0:
        raise ValueError("calibration mean absolute error cannot be negative")
    if snapshot.adaptation_sequence < 1:
        raise ValueError("retained adaptation sequence must be positive")
    parameter_names = [name for name, _ in snapshot.adaptation_parameters]
    if len(parameter_names) != len(set(parameter_names)):
        raise ValueError("retained adaptation parameter names must be unique")
    if any(not isfinite(value) for _, value in snapshot.adaptation_parameters):
        raise ValueError("retained adaptation parameter values must be finite")

    payload = {
        "session_id": snapshot.session_id,
        "binding_id": snapshot.binding_id,
        "calibration_receipt": snapshot.calibration_receipt,
        "calibration_mean_absolute_error": snapshot.calibration_mean_absolute_error,
        "adaptation_sequence": snapshot.adaptation_sequence,
        "adaptation_parameters": [list(item) for item in snapshot.adaptation_parameters],
    }
    if snapshot.snapshot_sha256 != _canonical_hash(payload):
        raise ValueError("retained snapshot hash mismatch")
    return {
        "result": "PASS",
        "snapshot_hash": "PASS",
        "adaptation_parameter_integrity": "PASS",
    }


def build_teacher_cross_session_retention() -> TeacherCrossSessionRetention:
    return TeacherCrossSessionRetention(
        retention_id="CHATGPT_TEACHER_CROSS_SESSION_RETENTION_v0.1",
        body_id="CHATGPT_TEACHER_3D_MALE_BODY_REFERENCE_v0.1",
        snapshots=(),
    )


def validate_teacher_cross_session_retention(
    retention: TeacherCrossSessionRetention,
) -> dict[str, str]:
    if retention.body_id != "CHATGPT_TEACHER_3D_MALE_BODY_REFERENCE_v0.1":
        raise ValueError("retention body id drift")
    session_ids = [item.session_id for item in retention.snapshots]
    if len(session_ids) != len(set(session_ids)):
        raise ValueError("retention session ids must be unique")
    hashes = [item.snapshot_sha256 for item in retention.snapshots]
    if len(hashes) != len(set(hashes)):
        raise ValueError("retained snapshot hashes must be unique")
    for snapshot in retention.snapshots:
        validate_teacher_session_snapshot(snapshot)
    if retention.retention_status != "MATERIALIZED_DURABLE_REFERENCE":
        raise ValueError("retention durable-reference status drift")
    if retention.identity_continuity_claim != "NONE":
        raise ValueError("retention cannot establish identity continuity")
    if retention.subjective_continuity_status != NOT_ESTABLISHED:
        raise ValueError("retention cannot establish subjective continuity")
    if retention.canonical_effect != "NONE" or retention.deployment:
        raise ValueError("retention must remain non-canonical and undeployed")
    return {
        "result": "PASS",
        "durable_reference": "PASS",
        "session_uniqueness": "PASS",
        "snapshot_hash_integrity": "PASS",
        "subjective_continuity_nonclaim": "PASS",
    }


def append_teacher_session_snapshot(
    retention: TeacherCrossSessionRetention,
    snapshot: TeacherSessionSnapshot,
) -> TeacherCrossSessionRetention:
    validate_teacher_cross_session_retention(retention)
    validate_teacher_session_snapshot(snapshot)
    if snapshot.session_id in {item.session_id for item in retention.snapshots}:
        raise ValueError("retention session ids must be unique")
    if any(item.snapshot_sha256 == snapshot.snapshot_sha256 for item in retention.snapshots):
        raise ValueError("duplicate retained snapshot")
    updated = replace(retention, snapshots=retention.snapshots + (snapshot,))
    validate_teacher_cross_session_retention(updated)
    return updated


def serialize_teacher_cross_session_retention(
    retention: TeacherCrossSessionRetention,
) -> bytes:
    validate_teacher_cross_session_retention(retention)
    payload = retention.to_dict()
    envelope = {
        "schema_version": "0.1.0",
        "payload": payload,
        "payload_sha256": _canonical_hash(payload),
    }
    return json.dumps(
        envelope,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def write_teacher_cross_session_retention(
    retention: TeacherCrossSessionRetention,
    path: str | Path,
) -> TeacherRetentionReceipt:
    data = serialize_teacher_cross_session_retention(retention)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    reread = target.read_bytes()
    if reread != data:
        raise ValueError("retention write verification failed")
    envelope = json.loads(data.decode("utf-8"))
    return TeacherRetentionReceipt(
        path=str(target),
        file_sha256=sha256(reread).hexdigest(),
        payload_sha256=str(envelope["payload_sha256"]),
        snapshot_count=len(retention.snapshots),
    )


def load_teacher_cross_session_retention(
    path: str | Path,
) -> TeacherCrossSessionRetention:
    envelope = json.loads(Path(path).read_text(encoding="utf-8"))
    payload = envelope.get("payload")
    if not isinstance(payload, dict):
        raise ValueError("retention file payload must be an object")
    expected_hash = envelope.get("payload_sha256")
    if expected_hash != _canonical_hash(payload):
        raise ValueError("retention payload hash mismatch")

    snapshots_raw = payload.get("snapshots")
    if not isinstance(snapshots_raw, list):
        raise ValueError("retention snapshots must be a list")
    snapshots = tuple(
        TeacherSessionSnapshot(
            session_id=str(item["session_id"]),
            binding_id=str(item["binding_id"]),
            calibration_receipt=str(item["calibration_receipt"]),
            calibration_mean_absolute_error=float(item["calibration_mean_absolute_error"]),
            adaptation_sequence=int(item["adaptation_sequence"]),
            adaptation_parameters=tuple(
                (str(name), float(value))
                for name, value in item["adaptation_parameters"]
            ),
            snapshot_sha256=str(item["snapshot_sha256"]),
        )
        for item in snapshots_raw
    )
    retention = TeacherCrossSessionRetention(
        retention_id=str(payload["retention_id"]),
        body_id=str(payload["body_id"]),
        snapshots=snapshots,
        retention_status=str(payload["retention_status"]),
        identity_continuity_claim=str(payload["identity_continuity_claim"]),
        subjective_continuity_status=str(payload["subjective_continuity_status"]),
        canonical_effect=str(payload["canonical_effect"]),
        deployment=bool(payload["deployment"]),
    )
    validate_teacher_cross_session_retention(retention)
    return retention
