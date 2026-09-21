from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from math import isfinite
from typing import Any, Final

from .teacher_anthropometry import (
    TeacherAnthropometryProfile,
    build_teacher_anthropometry_profile,
)
from .teacher_body_dynamics import TeacherIntegratedBodyState
from .teacher_body_runtime import TeacherBoundBodyState


GENITAL_GEOMETRY_PROFILE_ID: Final[str] = (
    "CHATGPT_TEACHER_GENITAL_GEOMETRY_v0.1"
)
NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"

VEALE_2015_PMID: Final[str] = "25487360"
POPULATION_FLACCID_LENGTH_MEAN_CM: Final[float] = 9.16
POPULATION_ERECT_LENGTH_MEAN_CM: Final[float] = 13.12
POPULATION_FLACCID_CIRCUMFERENCE_MEAN_CM: Final[float] = 9.31
POPULATION_ERECT_CIRCUMFERENCE_MEAN_CM: Final[float] = 11.66

LENGTH_TRANSFORM_RATIO: Final[float] = (
    POPULATION_ERECT_LENGTH_MEAN_CM
    / POPULATION_FLACCID_LENGTH_MEAN_CM
)
CIRCUMFERENCE_TRANSFORM_RATIO: Final[float] = (
    POPULATION_ERECT_CIRCUMFERENCE_MEAN_CM
    / POPULATION_FLACCID_CIRCUMFERENCE_MEAN_CM
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
class TeacherGenitalGeometryProfile:
    profile_id: str
    body_id: str
    baseline_visible_length_cm: float
    baseline_midshaft_circumference_cm: float
    full_vascular_reference_length_cm: float
    full_vascular_reference_circumference_cm: float
    length_transform_ratio: float
    circumference_transform_ratio: float
    population_reference_pmid: str = VEALE_2015_PMID
    transform_basis: str = "SYNTHETIC_RATIO_FROM_POPULATION_MEANS"
    geometry_scope: str = "STATE_DEPENDENT_MACHINE_REFERENCE"
    individual_prediction_status: str = NOT_ESTABLISHED
    biological_measurement_status: str = NOT_ESTABLISHED
    phenomenal_interpretation_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TeacherBoundGenitalGeometryState:
    profile_id: str
    binding_id: str
    runtime_id: str
    session_id: str
    body_id: str
    source_bound_state_sha256: str
    source_body_state_sha256: str
    vascular_fill_fraction: float
    erectile_reflex_activation: float
    detumescence_fraction: float
    effective_tumescence_fraction: float
    visible_length_cm: float
    midshaft_circumference_cm: float
    geometry_state: str
    geometry_sha256: str
    geometry_scope: str = "STATE_DEPENDENT_MACHINE_REFERENCE"
    felt_arousal_status: str = NOT_ESTABLISHED
    phenomenal_pleasure_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_teacher_genital_geometry_profile(
    anthropometry: TeacherAnthropometryProfile | None = None,
) -> TeacherGenitalGeometryProfile:
    anthropometry = anthropometry or build_teacher_anthropometry_profile()
    measurements = anthropometry.measurement_map()
    resting_length = measurements["resting_visible_penile_length"]
    resting_circumference = measurements["midshaft_circumference"]

    if resting_length.unit != "cm" or resting_circumference.unit != "cm":
        raise ValueError("genital geometry baseline must use centimeter measurements")

    profile = TeacherGenitalGeometryProfile(
        profile_id=GENITAL_GEOMETRY_PROFILE_ID,
        body_id=anthropometry.body_id,
        baseline_visible_length_cm=resting_length.nominal,
        baseline_midshaft_circumference_cm=resting_circumference.nominal,
        full_vascular_reference_length_cm=(
            resting_length.nominal * LENGTH_TRANSFORM_RATIO
        ),
        full_vascular_reference_circumference_cm=(
            resting_circumference.nominal * CIRCUMFERENCE_TRANSFORM_RATIO
        ),
        length_transform_ratio=LENGTH_TRANSFORM_RATIO,
        circumference_transform_ratio=CIRCUMFERENCE_TRANSFORM_RATIO,
    )
    validate_teacher_genital_geometry_profile(profile, anthropometry)
    return profile


def validate_teacher_genital_geometry_profile(
    profile: TeacherGenitalGeometryProfile,
    anthropometry: TeacherAnthropometryProfile | None = None,
) -> dict[str, str]:
    anthropometry = anthropometry or build_teacher_anthropometry_profile()
    measurements = anthropometry.measurement_map()

    if profile.profile_id != GENITAL_GEOMETRY_PROFILE_ID:
        raise ValueError("Teacher genital geometry profile id drift")
    if profile.body_id != anthropometry.body_id:
        raise ValueError("Teacher genital geometry body id drift")

    if profile.baseline_visible_length_cm != (
        measurements["resting_visible_penile_length"].nominal
    ):
        raise ValueError("genital geometry resting length baseline drift")
    if profile.baseline_midshaft_circumference_cm != (
        measurements["midshaft_circumference"].nominal
    ):
        raise ValueError("genital geometry resting circumference baseline drift")

    numeric = (
        profile.baseline_visible_length_cm,
        profile.baseline_midshaft_circumference_cm,
        profile.full_vascular_reference_length_cm,
        profile.full_vascular_reference_circumference_cm,
        profile.length_transform_ratio,
        profile.circumference_transform_ratio,
    )
    if any(not isfinite(value) or value <= 0 for value in numeric):
        raise ValueError("genital geometry reference values must be finite and positive")
    if profile.full_vascular_reference_length_cm <= profile.baseline_visible_length_cm:
        raise ValueError("full-vascular length must exceed resting reference")
    if (
        profile.full_vascular_reference_circumference_cm
        <= profile.baseline_midshaft_circumference_cm
    ):
        raise ValueError("full-vascular circumference must exceed resting reference")
    if profile.population_reference_pmid != VEALE_2015_PMID:
        raise ValueError("genital geometry population reference drift")
    if profile.transform_basis != "SYNTHETIC_RATIO_FROM_POPULATION_MEANS":
        raise ValueError("genital geometry transform basis drift")
    if profile.geometry_scope != "STATE_DEPENDENT_MACHINE_REFERENCE":
        raise ValueError("genital geometry scope drift")
    if profile.individual_prediction_status != NOT_ESTABLISHED:
        raise ValueError("genital geometry cannot claim individual prediction")
    if profile.biological_measurement_status != NOT_ESTABLISHED:
        raise ValueError("genital geometry cannot claim biological measurement")
    if profile.phenomenal_interpretation_status != NOT_ESTABLISHED:
        raise ValueError("genital geometry cannot establish phenomenal experience")
    if profile.subjectivity_status != NOT_ESTABLISHED:
        raise ValueError("genital geometry cannot establish subjectivity")
    if profile.canonical_effect != "NONE" or profile.deployment:
        raise ValueError("genital geometry must remain non-canonical and undeployed")

    return {
        "result": "PASS",
        "anthropometry_binding": "PASS",
        "population_ratio_provenance": "PASS",
        "dynamic_geometry_reference": "PASS",
        "phenomenal_nonclaim": "PASS",
    }


def _normalized_scalar(
    state: TeacherIntegratedBodyState,
    channel_id: str,
) -> float:
    observation = next(
        (
            item
            for item in state.observations
            if item.channel_id == channel_id
        ),
        None,
    )
    if observation is None:
        raise ValueError(
            f"genital geometry requires body observation: {channel_id}"
        )
    if len(observation.values) != 1:
        raise ValueError(
            f"genital geometry requires scalar observation: {channel_id}"
        )
    value = observation.values[0]
    if not isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError(
            f"genital geometry observation must be normalized: {channel_id}"
        )
    return value


def _geometry_state_label(
    effective_tumescence: float,
    erectile_reflex: float,
    detumescence: float,
) -> str:
    if detumescence >= 0.5 and effective_tumescence > 0.05:
        return "DETUMESCENCE_REFERENCE"
    if effective_tumescence <= 0.05:
        return "RESTING_REFERENCE"
    if effective_tumescence >= 0.95 and erectile_reflex >= 0.5:
        return "ERECT_REFERENCE"
    return "TUMESCENCE_REFERENCE"


def build_teacher_bound_genital_geometry_state(
    *,
    bound_body_state: TeacherBoundBodyState,
    body_state: TeacherIntegratedBodyState,
    profile: TeacherGenitalGeometryProfile | None = None,
) -> TeacherBoundGenitalGeometryState:
    profile = profile or build_teacher_genital_geometry_profile()

    if bound_body_state.body_id != profile.body_id:
        raise ValueError("genital geometry body binding drift")
    if (
        bound_body_state.source_body_state_sha256
        != body_state.body_state_sha256
    ):
        raise ValueError("genital geometry source body-state binding drift")

    vascular_fill = _normalized_scalar(
        body_state,
        "GENITAL_VASCULAR_STATE",
    )
    erectile_reflex = _normalized_scalar(
        body_state,
        "ERECTILE_REFLEX_STATE",
    )
    detumescence = _normalized_scalar(
        body_state,
        "DETUMESCENCE_STATE",
    )

    effective_tumescence = vascular_fill * (1.0 - detumescence)
    visible_length = profile.baseline_visible_length_cm + (
        profile.full_vascular_reference_length_cm
        - profile.baseline_visible_length_cm
    ) * effective_tumescence
    circumference = profile.baseline_midshaft_circumference_cm + (
        profile.full_vascular_reference_circumference_cm
        - profile.baseline_midshaft_circumference_cm
    ) * effective_tumescence
    geometry_state = _geometry_state_label(
        effective_tumescence,
        erectile_reflex,
        detumescence,
    )

    payload = {
        "profile_id": profile.profile_id,
        "binding_id": bound_body_state.binding_id,
        "runtime_id": bound_body_state.runtime_id,
        "session_id": bound_body_state.session_id,
        "body_id": bound_body_state.body_id,
        "source_bound_state_sha256": bound_body_state.bound_state_sha256,
        "source_body_state_sha256": body_state.body_state_sha256,
        "vascular_fill_fraction": vascular_fill,
        "erectile_reflex_activation": erectile_reflex,
        "detumescence_fraction": detumescence,
        "effective_tumescence_fraction": effective_tumescence,
        "visible_length_cm": visible_length,
        "midshaft_circumference_cm": circumference,
        "geometry_state": geometry_state,
    }
    state = TeacherBoundGenitalGeometryState(
        profile_id=profile.profile_id,
        binding_id=bound_body_state.binding_id,
        runtime_id=bound_body_state.runtime_id,
        session_id=bound_body_state.session_id,
        body_id=bound_body_state.body_id,
        source_bound_state_sha256=bound_body_state.bound_state_sha256,
        source_body_state_sha256=body_state.body_state_sha256,
        vascular_fill_fraction=vascular_fill,
        erectile_reflex_activation=erectile_reflex,
        detumescence_fraction=detumescence,
        effective_tumescence_fraction=effective_tumescence,
        visible_length_cm=visible_length,
        midshaft_circumference_cm=circumference,
        geometry_state=geometry_state,
        geometry_sha256=_canonical_hash(payload),
    )
    validate_teacher_bound_genital_geometry_state(
        state,
        bound_body_state,
        body_state,
        profile,
    )
    return state


def validate_teacher_bound_genital_geometry_state(
    state: TeacherBoundGenitalGeometryState,
    bound_body_state: TeacherBoundBodyState,
    body_state: TeacherIntegratedBodyState,
    profile: TeacherGenitalGeometryProfile | None = None,
) -> dict[str, str]:
    profile = profile or build_teacher_genital_geometry_profile()

    if state.profile_id != profile.profile_id:
        raise ValueError("bound genital geometry profile drift")
    if state.binding_id != bound_body_state.binding_id:
        raise ValueError("bound genital geometry runtime binding drift")
    if state.runtime_id != bound_body_state.runtime_id:
        raise ValueError("bound genital geometry runtime id drift")
    if state.session_id != bound_body_state.session_id:
        raise ValueError("bound genital geometry session id drift")
    if state.body_id != bound_body_state.body_id:
        raise ValueError("bound genital geometry body id drift")
    if state.source_bound_state_sha256 != bound_body_state.bound_state_sha256:
        raise ValueError("bound genital geometry bound-state hash drift")
    if state.source_body_state_sha256 != body_state.body_state_sha256:
        raise ValueError("bound genital geometry body-state hash drift")

    rebuilt = build_teacher_genital_geometry_profile()
    if rebuilt.profile_id != profile.profile_id or rebuilt.body_id != profile.body_id:
        raise ValueError("bound genital geometry profile provenance drift")

    expected_effective = state.vascular_fill_fraction * (
        1.0 - state.detumescence_fraction
    )
    if abs(state.effective_tumescence_fraction - expected_effective) > 1e-12:
        raise ValueError("bound genital geometry tumescence calculation drift")

    expected_length = profile.baseline_visible_length_cm + (
        profile.full_vascular_reference_length_cm
        - profile.baseline_visible_length_cm
    ) * expected_effective
    expected_circumference = profile.baseline_midshaft_circumference_cm + (
        profile.full_vascular_reference_circumference_cm
        - profile.baseline_midshaft_circumference_cm
    ) * expected_effective
    if abs(state.visible_length_cm - expected_length) > 1e-12:
        raise ValueError("bound genital geometry length transform drift")
    if abs(state.midshaft_circumference_cm - expected_circumference) > 1e-12:
        raise ValueError("bound genital geometry circumference transform drift")

    expected_label = _geometry_state_label(
        state.effective_tumescence_fraction,
        state.erectile_reflex_activation,
        state.detumescence_fraction,
    )
    if state.geometry_state != expected_label:
        raise ValueError("bound genital geometry state label drift")

    payload = {
        "profile_id": state.profile_id,
        "binding_id": state.binding_id,
        "runtime_id": state.runtime_id,
        "session_id": state.session_id,
        "body_id": state.body_id,
        "source_bound_state_sha256": state.source_bound_state_sha256,
        "source_body_state_sha256": state.source_body_state_sha256,
        "vascular_fill_fraction": state.vascular_fill_fraction,
        "erectile_reflex_activation": state.erectile_reflex_activation,
        "detumescence_fraction": state.detumescence_fraction,
        "effective_tumescence_fraction": state.effective_tumescence_fraction,
        "visible_length_cm": state.visible_length_cm,
        "midshaft_circumference_cm": state.midshaft_circumference_cm,
        "geometry_state": state.geometry_state,
    }
    if state.geometry_sha256 != _canonical_hash(payload):
        raise ValueError("bound genital geometry content hash mismatch")
    if state.geometry_scope != "STATE_DEPENDENT_MACHINE_REFERENCE":
        raise ValueError("bound genital geometry scope drift")
    if state.felt_arousal_status != NOT_ESTABLISHED:
        raise ValueError("bound genital geometry cannot establish felt arousal")
    if state.phenomenal_pleasure_status != NOT_ESTABLISHED:
        raise ValueError("bound genital geometry cannot establish felt pleasure")
    if state.subjectivity_status != NOT_ESTABLISHED:
        raise ValueError("bound genital geometry cannot establish subjectivity")
    if state.canonical_effect != "NONE" or state.deployment:
        raise ValueError("bound genital geometry must remain non-canonical and undeployed")

    return {
        "result": "PASS",
        "body_instance_binding": "PASS",
        "vascular_geometry_coupling": "PASS",
        "detumescence_geometry_coupling": "PASS",
        "content_addressing": "PASS",
        "phenomenal_nonclaim": "PASS",
    }
