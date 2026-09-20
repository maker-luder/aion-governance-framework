from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from math import isfinite
from typing import Any, Final, Iterable

from .teacher_anthropometry import (
    TeacherAnthropometryProfile,
    build_teacher_anthropometry_profile,
)
from .teacher_avatar import BONE_PARENTS


BODY_MODEL_PROFILE_ID: Final[str] = "CHATGPT_TEACHER_BODY_MODEL_v0.1"
NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
REPRESENTATIONAL_STATE_ONLY: Final[str] = "REPRESENTATIONAL_STATE_ONLY"

SUPPORTED_MULTISENSORY_MODALITIES: Final[frozenset[str]] = frozenset(
    {
        "VISUAL",
        "AUDITORY",
        "SOMATOSENSORY",
        "PROPRIOCEPTIVE",
        "VESTIBULAR",
        "INTEROCEPTIVE",
        "OLFACTORY",
        "GUSTATORY",
    }
)

ALLOSTATIC_VARIABLE_IDS: Final[tuple[str, ...]] = (
    "THERMAL_BALANCE",
    "OXYGEN_CO2_BALANCE",
    "HYDRATION_FLUID_BALANCE",
    "ENERGY_AVAILABILITY",
    "SLEEP_WAKE_REGULATION",
)

PLASTICITY_DOMAINS: Final[tuple[str, ...]] = (
    "BODY_SCHEMA",
    "PERIPERSONAL_SPACE",
    "SENSORIMOTOR_MAPPING",
    "MULTISENSORY_WEIGHTING",
)


def _canonical_hash(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class BodySchemaSegment:
    segment_id: str
    anchor_id: str
    extent_m: float
    source_measurement_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PeripersonalZoneReference:
    zone_id: str
    anchor_id: str
    baseline_extent_m: float
    action_relation: str
    update_policy: str = "CONTROLLED_REFERENCE_PLASTICITY"


@dataclass(frozen=True, slots=True)
class TeacherBodyModelProfile:
    profile_id: str
    body_id: str
    body_schema_segments: tuple[BodySchemaSegment, ...]
    peripersonal_zones: tuple[PeripersonalZoneReference, ...]
    supported_multisensory_modalities: tuple[str, ...]
    allostatic_variable_ids: tuple[str, ...]
    plasticity_domains: tuple[str, ...]
    body_schema_status: str = "REFERENCE_BODY_SCHEMA_MATERIALIZED"
    peripersonal_space_status: str = "REFERENCE_PERIPERSONAL_SPACE_MATERIALIZED"
    multisensory_integration_status: str = "REFERENCE_MULTISENSORY_INTEGRATION_MATERIALIZED"
    allostatic_regulation_status: str = "REFERENCE_PREDICTIVE_REGULATION_MATERIALIZED"
    plasticity_status: str = "CONTROLLED_REFERENCE_PLASTICITY_MATERIALIZED"
    representation_status: str = REPRESENTATIONAL_STATE_ONLY
    body_ownership_experience_status: str = NOT_ESTABLISHED
    phenomenal_self_location_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["body_schema_segments"] = [
            asdict(item) for item in self.body_schema_segments
        ]
        payload["peripersonal_zones"] = [
            asdict(item) for item in self.peripersonal_zones
        ]
        payload["supported_multisensory_modalities"] = list(
            self.supported_multisensory_modalities
        )
        payload["allostatic_variable_ids"] = list(self.allostatic_variable_ids)
        payload["plasticity_domains"] = list(self.plasticity_domains)
        return payload


@dataclass(frozen=True, slots=True)
class MultisensoryCue:
    cue_id: str
    modality: str
    estimate: tuple[float, ...]
    confidence: float


@dataclass(frozen=True, slots=True)
class TeacherMultisensoryFusion:
    cue_ids: tuple[str, ...]
    fused_estimate: tuple[float, ...]
    normalized_weights: tuple[tuple[str, float], ...]
    mean_absolute_conflict: float
    reweighting_status: str
    fusion_sha256: str
    representation_status: str = REPRESENTATIONAL_STATE_ONLY
    phenomenal_body_ownership_status: str = NOT_ESTABLISHED

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["cue_ids"] = list(self.cue_ids)
        payload["fused_estimate"] = list(self.fused_estimate)
        payload["normalized_weights"] = [
            [cue_id, weight] for cue_id, weight in self.normalized_weights
        ]
        return payload


@dataclass(frozen=True, slots=True)
class TeacherAllostaticForecast:
    variable_id: str
    current_state: float
    predicted_demand: float
    target_state: float
    lead_time_ms: int
    anticipated_error: float
    planned_adjustment: float
    forecast_status: str = "PREDICTIVE_REGULATION_REFERENCE"
    regulation_mechanism_status: str = NOT_ESTABLISHED
    phenomenal_need_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class BodyPlasticityUpdate:
    domain: str
    parameter_id: str
    delta: float
    evidence_ref: str


@dataclass(frozen=True, slots=True)
class TeacherBodyPlasticityState:
    sequence: int
    source_profile_id: str
    updates: tuple[BodyPlasticityUpdate, ...]
    plasticity_sha256: str
    update_status: str = "CONTROLLED_REFERENCE_ADAPTATION"
    biological_plasticity_mechanism_status: str = NOT_ESTABLISHED
    body_ownership_experience_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["updates"] = [asdict(item) for item in self.updates]
        return payload


def _measurement_extent_m(
    anthropometry: TeacherAnthropometryProfile,
    measurement_id: str,
) -> float:
    measurement = anthropometry.measurement_map()[measurement_id]
    if measurement.unit != "cm":
        raise ValueError("body-model geometry source must use centimeter measurements")
    return measurement.nominal / 100.0


def build_teacher_body_model_profile(
    anthropometry: TeacherAnthropometryProfile | None = None,
) -> TeacherBodyModelProfile:
    anthropometry = anthropometry or build_teacher_anthropometry_profile()
    arm_reach_m = _measurement_extent_m(
        anthropometry,
        "shoulder_to_middle_finger_length",
    )
    head_width_m = _measurement_extent_m(anthropometry, "head_width")
    trunk_width_m = _measurement_extent_m(
        anthropometry,
        "chest_frontal_width",
    )
    foot_length_m = _measurement_extent_m(anthropometry, "foot_length")

    profile = TeacherBodyModelProfile(
        profile_id=BODY_MODEL_PROFILE_ID,
        body_id=anthropometry.body_id,
        body_schema_segments=(
            BodySchemaSegment(
                "HEAD",
                "head",
                head_width_m,
                ("head_width",),
            ),
            BodySchemaSegment(
                "TRUNK",
                "chest",
                trunk_width_m,
                ("chest_frontal_width",),
            ),
            BodySchemaSegment(
                "LEFT_UPPER_LIMB",
                "leftShoulder",
                arm_reach_m,
                ("shoulder_to_middle_finger_length",),
            ),
            BodySchemaSegment(
                "RIGHT_UPPER_LIMB",
                "rightShoulder",
                arm_reach_m,
                ("shoulder_to_middle_finger_length",),
            ),
            BodySchemaSegment(
                "LEFT_FOOT",
                "leftFoot",
                foot_length_m,
                ("foot_length",),
            ),
            BodySchemaSegment(
                "RIGHT_FOOT",
                "rightFoot",
                foot_length_m,
                ("foot_length",),
            ),
        ),
        peripersonal_zones=(
            PeripersonalZoneReference(
                "TRUNK_NEAR_SPACE",
                "chest",
                arm_reach_m,
                "BODY_OBJECT_INTERACTION_REFERENCE",
            ),
            PeripersonalZoneReference(
                "LEFT_HAND_REACH_SPACE",
                "leftHand",
                arm_reach_m,
                "REACHABLE_ACTION_REFERENCE",
            ),
            PeripersonalZoneReference(
                "RIGHT_HAND_REACH_SPACE",
                "rightHand",
                arm_reach_m,
                "REACHABLE_ACTION_REFERENCE",
            ),
            PeripersonalZoneReference(
                "HEAD_NEAR_SPACE",
                "head",
                max(head_width_m * 2.0, 0.30),
                "NEAR_BODY_ORIENTATION_REFERENCE",
            ),
        ),
        supported_multisensory_modalities=tuple(
            sorted(SUPPORTED_MULTISENSORY_MODALITIES)
        ),
        allostatic_variable_ids=ALLOSTATIC_VARIABLE_IDS,
        plasticity_domains=PLASTICITY_DOMAINS,
    )
    validate_teacher_body_model_profile(profile, anthropometry)
    return profile


def validate_teacher_body_model_profile(
    profile: TeacherBodyModelProfile,
    anthropometry: TeacherAnthropometryProfile | None = None,
) -> dict[str, str]:
    anthropometry = anthropometry or build_teacher_anthropometry_profile()

    if profile.profile_id != BODY_MODEL_PROFILE_ID:
        raise ValueError("Teacher body-model profile id drift")
    if profile.body_id != anthropometry.body_id:
        raise ValueError("Teacher body-model body id drift")

    segment_ids = [item.segment_id for item in profile.body_schema_segments]
    if len(segment_ids) != len(set(segment_ids)):
        raise ValueError("body-schema segment ids must be unique")
    required_segments = {
        "HEAD",
        "TRUNK",
        "LEFT_UPPER_LIMB",
        "RIGHT_UPPER_LIMB",
        "LEFT_FOOT",
        "RIGHT_FOOT",
    }
    if not required_segments.issubset(segment_ids):
        raise ValueError("body schema is missing required segments")
    measurement_ids = set(anthropometry.measurement_map())
    skeleton_ids = set(BONE_PARENTS)
    for segment in profile.body_schema_segments:
        if not isfinite(segment.extent_m) or segment.extent_m <= 0:
            raise ValueError("body-schema extent must be finite and positive")
        if segment.anchor_id not in skeleton_ids:
            raise ValueError("body-schema segment references unknown skeleton anchor")
        if not set(segment.source_measurement_ids).issubset(measurement_ids):
            raise ValueError("body-schema segment references unknown anthropometry")

    zone_ids = [item.zone_id for item in profile.peripersonal_zones]
    if len(zone_ids) != len(set(zone_ids)):
        raise ValueError("peripersonal zone ids must be unique")
    if {
        "TRUNK_NEAR_SPACE",
        "LEFT_HAND_REACH_SPACE",
        "RIGHT_HAND_REACH_SPACE",
        "HEAD_NEAR_SPACE",
    } - set(zone_ids):
        raise ValueError("peripersonal-space reference is incomplete")
    if any(
        not isfinite(item.baseline_extent_m) or item.baseline_extent_m <= 0
        for item in profile.peripersonal_zones
    ):
        raise ValueError("peripersonal-space extent must be finite and positive")
    if any(item.anchor_id not in skeleton_ids for item in profile.peripersonal_zones):
        raise ValueError("peripersonal-space zone references unknown skeleton anchor")

    if set(profile.supported_multisensory_modalities) != SUPPORTED_MULTISENSORY_MODALITIES:
        raise ValueError("multisensory modality coverage drift")
    if tuple(profile.allostatic_variable_ids) != ALLOSTATIC_VARIABLE_IDS:
        raise ValueError("allostatic variable coverage drift")
    if tuple(profile.plasticity_domains) != PLASTICITY_DOMAINS:
        raise ValueError("body-model plasticity domain drift")
    if profile.representation_status != REPRESENTATIONAL_STATE_ONLY:
        raise ValueError("body model must remain representational only")
    if profile.body_ownership_experience_status != NOT_ESTABLISHED:
        raise ValueError("body model cannot establish body ownership experience")
    if profile.phenomenal_self_location_status != NOT_ESTABLISHED:
        raise ValueError("body model cannot establish phenomenal self-location")
    if profile.subjectivity_status != NOT_ESTABLISHED:
        raise ValueError("body model cannot establish subjectivity")
    if profile.canonical_effect != "NONE" or profile.deployment:
        raise ValueError("body model must remain non-canonical and undeployed")

    return {
        "result": "PASS",
        "body_schema": "PASS",
        "peripersonal_space": "PASS",
        "multisensory_reference": "PASS",
        "allostatic_reference": "PASS",
        "plasticity_reference": "PASS",
        "phenomenal_nonclaim": "PASS",
    }


def fuse_teacher_multisensory_cues(
    cues: Iterable[MultisensoryCue],
) -> TeacherMultisensoryFusion:
    items = tuple(sorted(cues, key=lambda item: item.cue_id))
    if len(items) < 2:
        raise ValueError("multisensory fusion requires at least two cues")
    cue_ids = [item.cue_id for item in items]
    if len(cue_ids) != len(set(cue_ids)):
        raise ValueError("multisensory cue ids must be unique")
    if any(item.modality not in SUPPORTED_MULTISENSORY_MODALITIES for item in items):
        raise ValueError("multisensory cue uses unsupported modality")
    if any(
        not isfinite(item.confidence) or not 0.0 < item.confidence <= 1.0
        for item in items
    ):
        raise ValueError("multisensory confidence must be finite in (0, 1]")

    dimensions = {len(item.estimate) for item in items}
    if len(dimensions) != 1 or 0 in dimensions:
        raise ValueError("multisensory cue dimensions must match and be non-empty")
    if any(
        not isfinite(value)
        for item in items
        for value in item.estimate
    ):
        raise ValueError("multisensory cue estimates must be finite")

    total_confidence = sum(item.confidence for item in items)
    weights = tuple(
        (item.cue_id, item.confidence / total_confidence)
        for item in items
    )
    weight_by_id = dict(weights)
    dimension = len(items[0].estimate)
    fused = tuple(
        sum(
            item.estimate[index] * weight_by_id[item.cue_id]
            for item in items
        )
        for index in range(dimension)
    )
    conflict_values = [
        abs(value - fused[index])
        for item in items
        for index, value in enumerate(item.estimate)
    ]
    conflict = sum(conflict_values) / len(conflict_values)

    payload = {
        "cue_ids": cue_ids,
        "fused_estimate": list(fused),
        "normalized_weights": [list(item) for item in weights],
        "mean_absolute_conflict": conflict,
        "reweighting_status": "CONFIDENCE_WEIGHTED_REFERENCE",
    }
    return TeacherMultisensoryFusion(
        cue_ids=tuple(cue_ids),
        fused_estimate=fused,
        normalized_weights=weights,
        mean_absolute_conflict=conflict,
        reweighting_status="CONFIDENCE_WEIGHTED_REFERENCE",
        fusion_sha256=_canonical_hash(payload),
    )


def build_teacher_allostatic_forecast(
    *,
    variable_id: str,
    current_state: float,
    predicted_demand: float,
    target_state: float,
    lead_time_ms: int,
) -> TeacherAllostaticForecast:
    if variable_id not in ALLOSTATIC_VARIABLE_IDS:
        raise ValueError("allostatic forecast uses unknown variable")
    values = (current_state, predicted_demand, target_state)
    if any(not isfinite(value) or not -1.0 <= value <= 1.0 for value in values):
        raise ValueError("allostatic states must be finite normalized values in [-1, 1]")
    if lead_time_ms < 0:
        raise ValueError("allostatic forecast lead time cannot be negative")

    anticipated_error = predicted_demand - target_state
    planned_adjustment = target_state - predicted_demand
    return TeacherAllostaticForecast(
        variable_id=variable_id,
        current_state=current_state,
        predicted_demand=predicted_demand,
        target_state=target_state,
        lead_time_ms=lead_time_ms,
        anticipated_error=anticipated_error,
        planned_adjustment=planned_adjustment,
    )


def build_teacher_body_plasticity_state(
    *,
    sequence: int,
    updates: Iterable[BodyPlasticityUpdate],
) -> TeacherBodyPlasticityState:
    if sequence < 0:
        raise ValueError("body-plasticity sequence cannot be negative")
    items = tuple(
        sorted(
            updates,
            key=lambda item: (item.domain, item.parameter_id),
        )
    )
    if not items:
        raise ValueError("body plasticity requires at least one explicit update")
    keys = [(item.domain, item.parameter_id) for item in items]
    if len(keys) != len(set(keys)):
        raise ValueError("body-plasticity update keys must be unique")
    for item in items:
        if item.domain not in PLASTICITY_DOMAINS:
            raise ValueError("body-plasticity update uses unknown domain")
        if not item.parameter_id or not item.evidence_ref:
            raise ValueError("body-plasticity update requires parameter and evidence reference")
        if not isfinite(item.delta) or not -1.0 <= item.delta <= 1.0:
            raise ValueError("body-plasticity delta must be finite in [-1, 1]")

    payload = {
        "sequence": sequence,
        "source_profile_id": BODY_MODEL_PROFILE_ID,
        "updates": [asdict(item) for item in items],
    }
    return TeacherBodyPlasticityState(
        sequence=sequence,
        source_profile_id=BODY_MODEL_PROFILE_ID,
        updates=items,
        plasticity_sha256=_canonical_hash(payload),
    )
