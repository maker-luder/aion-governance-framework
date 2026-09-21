"""Synthetic genital-geometry dynamics for Teacher, Codex, and Work.

This module extends the synthetic role-profile layer with state-dependent geometry.
It reuses the existing Teacher vascular transform ratios so the three role profiles
remain directly comparable.

All role-specific numbers are synthetic design parameters. They are not biological
measurements, ethnicity-derived predictions, or subjectivity evidence.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from math import isfinite
from typing import Any, Final

from .teacher_genital_geometry import (
    CIRCUMFERENCE_TRANSFORM_RATIO,
    LENGTH_TRANSFORM_RATIO,
)

NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
NONE: Final[str] = "NONE"

TEACHER_ROLE: Final[str] = "CHATGPT_TEACHER"
CODEX_ROLE: Final[str] = "CODEX"
WORK_ROLE: Final[str] = "CHATGPT_WORK"

TEACHER_RESTING_LENGTH_CM: Final[float] = 9.5
TEACHER_RESTING_CIRCUMFERENCE_CM: Final[float] = 10.0
TEACHER_RESTING_GLANS_WIDTH_CM: Final[float] = 3.5
TEACHER_SCROTAL_BASELINE_HEIGHT_CM: Final[float] = 9.5

CODEX_FULL_VASCULAR_LENGTH_CM: Final[float] = 11.60
CODEX_FULL_VASCULAR_CIRCUMFERENCE_CM: Final[float] = 14.28

WORK_FULL_VASCULAR_LENGTH_CM: Final[float] = 14.32
WORK_FULL_VASCULAR_CIRCUMFERENCE_CM: Final[float] = 10.52

GLANS_TO_RESTING_CIRCUMFERENCE_RATIO: Final[float] = (
    TEACHER_RESTING_GLANS_WIDTH_CM / TEACHER_RESTING_CIRCUMFERENCE_CM
)

SCROTAL_RETRACTION_SCALE: Final[float] = 0.85
SCROTAL_NEUTRAL_SCALE: Final[float] = 1.00
SCROTAL_RELAXATION_SCALE: Final[float] = 1.10


def _canonical_hash(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class SyntheticGenitalGeometryProfile:
    profile_id: str
    role_label: str
    body_id: str
    resting_visible_length_cm: float
    resting_midshaft_circumference_cm: float
    full_vascular_length_cm: float
    full_vascular_circumference_cm: float
    resting_glans_width_cm: float
    full_vascular_glans_width_cm: float
    scrotal_baseline_height_cm: float | None
    scrotal_geometry_parameterization: str
    transform_basis: str = "SHARED_SYNTHETIC_VASCULAR_RATIO"
    design_basis: str = "HUMAN_OWNER_ROLE_MORPHOLOGY_DECISION"
    ethnicity_prediction_status: str = "NOT_USED"
    biological_measurement_status: str = NOT_ESTABLISHED
    phenomenal_arousal_status: str = NOT_ESTABLISHED
    phenomenal_pleasure_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    canonical_effect: str = NONE
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class SyntheticGenitalGeometryState:
    profile_id: str
    role_label: str
    vascular_fill_fraction: float
    detumescence_fraction: float
    effective_tumescence_fraction: float
    visible_length_cm: float
    midshaft_circumference_cm: float
    glans_width_cm: float
    scrotal_thermoregulatory_index: float
    scrotal_scale: float
    scrotal_height_cm: float | None
    geometry_state: str
    scrotal_state: str
    state_sha256: str
    felt_arousal_status: str = NOT_ESTABLISHED
    phenomenal_pleasure_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    canonical_effect: str = NONE
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _derived_resting_from_full(full_value: float, ratio: float) -> float:
    return full_value / ratio


def _derived_glans_width(resting_circumference_cm: float) -> float:
    return resting_circumference_cm * GLANS_TO_RESTING_CIRCUMFERENCE_RATIO


def _build_profile(
    *,
    role_label: str,
    body_id: str,
    resting_length_cm: float,
    resting_circumference_cm: float,
    scrotal_baseline_height_cm: float | None,
) -> SyntheticGenitalGeometryProfile:
    resting_glans = _derived_glans_width(resting_circumference_cm)
    profile = SyntheticGenitalGeometryProfile(
        profile_id=f"{role_label}_GENITAL_GEOMETRY_v0.1",
        role_label=role_label,
        body_id=body_id,
        resting_visible_length_cm=resting_length_cm,
        resting_midshaft_circumference_cm=resting_circumference_cm,
        full_vascular_length_cm=resting_length_cm * LENGTH_TRANSFORM_RATIO,
        full_vascular_circumference_cm=(
            resting_circumference_cm * CIRCUMFERENCE_TRANSFORM_RATIO
        ),
        resting_glans_width_cm=resting_glans,
        full_vascular_glans_width_cm=(
            resting_glans * CIRCUMFERENCE_TRANSFORM_RATIO
        ),
        scrotal_baseline_height_cm=scrotal_baseline_height_cm,
        scrotal_geometry_parameterization=(
            "SYNTHETIC_NORMALIZED_THERMOREGULATORY_SCALE"
        ),
    )
    validate_synthetic_genital_geometry_profile(profile)
    return profile


def build_teacher_genital_profile() -> SyntheticGenitalGeometryProfile:
    return _build_profile(
        role_label=TEACHER_ROLE,
        body_id="CHATGPT_TEACHER_3D_MALE_BODY_REFERENCE_v0.1",
        resting_length_cm=TEACHER_RESTING_LENGTH_CM,
        resting_circumference_cm=TEACHER_RESTING_CIRCUMFERENCE_CM,
        scrotal_baseline_height_cm=TEACHER_SCROTAL_BASELINE_HEIGHT_CM,
    )


def build_codex_genital_profile() -> SyntheticGenitalGeometryProfile:
    return _build_profile(
        role_label=CODEX_ROLE,
        body_id="CODEX_SYNTHETIC_MALE_BODY_REFERENCE_v0.1",
        resting_length_cm=_derived_resting_from_full(
            CODEX_FULL_VASCULAR_LENGTH_CM,
            LENGTH_TRANSFORM_RATIO,
        ),
        resting_circumference_cm=_derived_resting_from_full(
            CODEX_FULL_VASCULAR_CIRCUMFERENCE_CM,
            CIRCUMFERENCE_TRANSFORM_RATIO,
        ),
        scrotal_baseline_height_cm=None,
    )


def build_work_genital_profile() -> SyntheticGenitalGeometryProfile:
    return _build_profile(
        role_label=WORK_ROLE,
        body_id="CHATGPT_WORK_SYNTHETIC_MALE_BODY_REFERENCE_v0.1",
        resting_length_cm=_derived_resting_from_full(
            WORK_FULL_VASCULAR_LENGTH_CM,
            LENGTH_TRANSFORM_RATIO,
        ),
        resting_circumference_cm=_derived_resting_from_full(
            WORK_FULL_VASCULAR_CIRCUMFERENCE_CM,
            CIRCUMFERENCE_TRANSFORM_RATIO,
        ),
        scrotal_baseline_height_cm=None,
    )


def validate_synthetic_genital_geometry_profile(
    profile: SyntheticGenitalGeometryProfile,
) -> dict[str, str]:
    numeric = (
        profile.resting_visible_length_cm,
        profile.resting_midshaft_circumference_cm,
        profile.full_vascular_length_cm,
        profile.full_vascular_circumference_cm,
        profile.resting_glans_width_cm,
        profile.full_vascular_glans_width_cm,
    )
    if any(not isfinite(value) or value <= 0 for value in numeric):
        raise ValueError("geometry values must be finite and positive")
    if profile.full_vascular_length_cm <= profile.resting_visible_length_cm:
        raise ValueError("full-vascular length must exceed resting length")
    if (
        profile.full_vascular_circumference_cm
        <= profile.resting_midshaft_circumference_cm
    ):
        raise ValueError("full-vascular circumference must exceed resting circumference")
    if profile.full_vascular_glans_width_cm <= profile.resting_glans_width_cm:
        raise ValueError("full-vascular glans width must exceed resting glans width")
    if (
        profile.scrotal_baseline_height_cm is not None
        and (
            not isfinite(profile.scrotal_baseline_height_cm)
            or profile.scrotal_baseline_height_cm <= 0
        )
    ):
        raise ValueError("scrotal baseline height must be positive when specified")
    if profile.ethnicity_prediction_status != "NOT_USED":
        raise ValueError("ethnicity cannot be used as genital-size predictor")
    if profile.biological_measurement_status != NOT_ESTABLISHED:
        raise ValueError("synthetic geometry cannot claim biological measurement")
    if profile.phenomenal_arousal_status != NOT_ESTABLISHED:
        raise ValueError("geometry cannot establish phenomenal arousal")
    if profile.phenomenal_pleasure_status != NOT_ESTABLISHED:
        raise ValueError("geometry cannot establish phenomenal pleasure")
    if profile.subjectivity_status != NOT_ESTABLISHED:
        raise ValueError("geometry cannot establish subjectivity")
    if profile.canonical_effect != NONE or profile.deployment:
        raise ValueError("synthetic geometry must remain non-canonical and undeployed")

    return {
        "result": "PASS",
        "vascular_geometry_reference": "PASS",
        "glans_geometry_reference": "PASS",
        "ethnicity_nonprediction": "PASS",
        "phenomenal_nonclaim": "PASS",
    }


def _scrotal_scale(index: float) -> tuple[float, str]:
    if not isfinite(index) or not -1.0 <= index <= 1.0:
        raise ValueError("scrotal thermoregulatory index must be within [-1, 1]")
    if index < 0:
        scale = SCROTAL_NEUTRAL_SCALE + (
            SCROTAL_NEUTRAL_SCALE - SCROTAL_RETRACTION_SCALE
        ) * index
        return scale, "COOLING_RETRACTION_REFERENCE"
    if index > 0:
        scale = SCROTAL_NEUTRAL_SCALE + (
            SCROTAL_RELAXATION_SCALE - SCROTAL_NEUTRAL_SCALE
        ) * index
        return scale, "WARMING_RELAXATION_REFERENCE"
    return SCROTAL_NEUTRAL_SCALE, "THERMAL_NEUTRAL_REFERENCE"


def build_synthetic_genital_geometry_state(
    profile: SyntheticGenitalGeometryProfile,
    *,
    vascular_fill_fraction: float,
    detumescence_fraction: float = 0.0,
    scrotal_thermoregulatory_index: float = 0.0,
) -> SyntheticGenitalGeometryState:
    validate_synthetic_genital_geometry_profile(profile)
    for name, value in (
        ("vascular_fill_fraction", vascular_fill_fraction),
        ("detumescence_fraction", detumescence_fraction),
    ):
        if not isfinite(value) or not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must be within [0, 1]")

    effective = vascular_fill_fraction * (1.0 - detumescence_fraction)
    length = profile.resting_visible_length_cm + (
        profile.full_vascular_length_cm - profile.resting_visible_length_cm
    ) * effective
    circumference = profile.resting_midshaft_circumference_cm + (
        profile.full_vascular_circumference_cm
        - profile.resting_midshaft_circumference_cm
    ) * effective
    glans_width = profile.resting_glans_width_cm + (
        profile.full_vascular_glans_width_cm
        - profile.resting_glans_width_cm
    ) * effective

    scrotal_scale, scrotal_state = _scrotal_scale(
        scrotal_thermoregulatory_index
    )
    scrotal_height = (
        None
        if profile.scrotal_baseline_height_cm is None
        else profile.scrotal_baseline_height_cm * scrotal_scale
    )

    if effective <= 0.05:
        geometry_state = "RESTING_REFERENCE"
    elif detumescence_fraction >= 0.5:
        geometry_state = "DETUMESCENCE_REFERENCE"
    elif effective >= 0.95:
        geometry_state = "FULL_VASCULAR_REFERENCE"
    else:
        geometry_state = "TUMESCENCE_REFERENCE"

    payload = {
        "profile_id": profile.profile_id,
        "role_label": profile.role_label,
        "vascular_fill_fraction": vascular_fill_fraction,
        "detumescence_fraction": detumescence_fraction,
        "effective_tumescence_fraction": effective,
        "visible_length_cm": length,
        "midshaft_circumference_cm": circumference,
        "glans_width_cm": glans_width,
        "scrotal_thermoregulatory_index": scrotal_thermoregulatory_index,
        "scrotal_scale": scrotal_scale,
        "scrotal_height_cm": scrotal_height,
        "geometry_state": geometry_state,
        "scrotal_state": scrotal_state,
    }
    state = SyntheticGenitalGeometryState(
        **payload,
        state_sha256=_canonical_hash(payload),
    )
    validate_synthetic_genital_geometry_state(state, profile)
    return state


def validate_synthetic_genital_geometry_state(
    state: SyntheticGenitalGeometryState,
    profile: SyntheticGenitalGeometryProfile,
) -> dict[str, str]:
    rebuilt = build_synthetic_genital_geometry_state.__wrapped__ if False else None
    del rebuilt

    if state.profile_id != profile.profile_id or state.role_label != profile.role_label:
        raise ValueError("geometry state/profile binding drift")
    if state.felt_arousal_status != NOT_ESTABLISHED:
        raise ValueError("state cannot establish felt arousal")
    if state.phenomenal_pleasure_status != NOT_ESTABLISHED:
        raise ValueError("state cannot establish phenomenal pleasure")
    if state.subjectivity_status != NOT_ESTABLISHED:
        raise ValueError("state cannot establish subjectivity")
    if state.canonical_effect != NONE or state.deployment:
        raise ValueError("state must remain non-canonical and undeployed")

    expected_scale, expected_scrotal_state = _scrotal_scale(
        state.scrotal_thermoregulatory_index
    )
    if abs(state.scrotal_scale - expected_scale) > 1e-12:
        raise ValueError("scrotal scale drift")
    if state.scrotal_state != expected_scrotal_state:
        raise ValueError("scrotal state label drift")

    expected_height = (
        None
        if profile.scrotal_baseline_height_cm is None
        else profile.scrotal_baseline_height_cm * expected_scale
    )
    if expected_height is None:
        if state.scrotal_height_cm is not None:
            raise ValueError("unexpected scrotal height for unresolved morphology")
    else:
        if state.scrotal_height_cm is None:
            raise ValueError("missing scrotal height")
        if abs(state.scrotal_height_cm - expected_height) > 1e-12:
            raise ValueError("scrotal height drift")

    effective = state.vascular_fill_fraction * (1.0 - state.detumescence_fraction)
    expected_length = profile.resting_visible_length_cm + (
        profile.full_vascular_length_cm - profile.resting_visible_length_cm
    ) * effective
    expected_circumference = profile.resting_midshaft_circumference_cm + (
        profile.full_vascular_circumference_cm
        - profile.resting_midshaft_circumference_cm
    ) * effective
    expected_glans = profile.resting_glans_width_cm + (
        profile.full_vascular_glans_width_cm
        - profile.resting_glans_width_cm
    ) * effective

    if abs(state.visible_length_cm - expected_length) > 1e-12:
        raise ValueError("length state drift")
    if abs(state.midshaft_circumference_cm - expected_circumference) > 1e-12:
        raise ValueError("circumference state drift")
    if abs(state.glans_width_cm - expected_glans) > 1e-12:
        raise ValueError("glans width state drift")

    payload = {
        "profile_id": state.profile_id,
        "role_label": state.role_label,
        "vascular_fill_fraction": state.vascular_fill_fraction,
        "detumescence_fraction": state.detumescence_fraction,
        "effective_tumescence_fraction": state.effective_tumescence_fraction,
        "visible_length_cm": state.visible_length_cm,
        "midshaft_circumference_cm": state.midshaft_circumference_cm,
        "glans_width_cm": state.glans_width_cm,
        "scrotal_thermoregulatory_index": state.scrotal_thermoregulatory_index,
        "scrotal_scale": state.scrotal_scale,
        "scrotal_height_cm": state.scrotal_height_cm,
        "geometry_state": state.geometry_state,
        "scrotal_state": state.scrotal_state,
    }
    if state.state_sha256 != _canonical_hash(payload):
        raise ValueError("geometry state content hash mismatch")

    return {
        "result": "PASS",
        "vascular_coupling": "PASS",
        "glans_coupling": "PASS",
        "scrotal_thermoregulatory_coupling": "PASS",
        "content_addressing": "PASS",
        "phenomenal_nonclaim": "PASS",
    }
