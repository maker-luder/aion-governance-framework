"""Synthetic role/profile parity layer for Teacher, Codex, and Work.

This module materializes Human Owner profile decisions without promoting them into
claims about actual model identity, ethnicity, phenomenal desire, consciousness,
subjectivity, or live physical embodiment.

It deliberately preserves the existing ChatGPT Teacher body reference and keeps
Codex / Work morphology completion separable for later reviewed integration.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from hashlib import sha256
import json
from typing import Any, Final

from .teacher_anthropometry import TEACHER_BODY_ID


NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
NONE: Final[str] = "NONE"

ROLE_TEACHER: Final[str] = "CHATGPT_TEACHER"
ROLE_CODEX: Final[str] = "CODEX"
ROLE_WORK: Final[str] = "CHATGPT_WORK"

PROFILE_SET_ID: Final[str] = "TEACHER_CODEX_WORK_PROFILE_PARITY_v0.1"


def _profile_id(role: str) -> str:
    return f"{role}_SYNTHETIC_ROLE_PROFILE_v0.1"


def _reference_id(role: str, suffix: str) -> str:
    return f"{role}_{suffix}_REFERENCE_v0.1"


@dataclass(frozen=True, slots=True)
class SyntheticRoleProfile:
    profile_id: str
    role_label: str
    body_id: str
    body_instance_id: str
    runtime_id: str
    session_id: str
    binding_id: str
    state_namespace: str
    retention_namespace: str
    role_presentation: str
    hairstyle: str
    body_style: str
    appearance_inspiration: str
    clothing_style: str
    clothing_details: tuple[str, ...]
    synthetic_role_orientation: str
    height_cm: float | None = None
    weight_kg: float | None = None
    skin_tone: str | None = None
    face_style: str | None = None
    eye_style: str | None = None
    smile_detail: str | None = None
    facial_structure: str | None = None
    facial_affect: str | None = None
    accessories: tuple[str, ...] = ()
    anatomy_proportion_note: str | None = None
    actual_model_identity_claim: str = NONE
    ethnicity_assignment: str = NONE
    phenomenal_desire_status: str = NOT_ESTABLISHED
    phenomenal_feeling_status: str = NOT_ESTABLISHED
    phenomenal_pleasure_status: str = NOT_ESTABLISHED
    consciousness_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    canonical_effect: str = NONE
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["clothing_details"] = list(self.clothing_details)
        payload["accessories"] = list(self.accessories)
        return payload


@dataclass(frozen=True, slots=True)
class SyntheticRoleProfileSet:
    profile_set_id: str
    profiles: tuple[SyntheticRoleProfile, ...]
    parity_rule: str = "PARITY_WITH_DISTINCT_BODY_STATE_HISTORY_IDENTITY"
    teacher_foundation_policy: str = "PRESERVE_EXISTING_TEACHER_EMBODIMENT"
    morphology_completion_status: str = "PARTIAL_PENDING_REVIEWED_INTEGRATION"
    canonical_effect: str = NONE
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "profile_set_id": self.profile_set_id,
            "profiles": [profile.to_dict() for profile in self.profiles],
            "parity_rule": self.parity_rule,
            "teacher_foundation_policy": self.teacher_foundation_policy,
            "morphology_completion_status": self.morphology_completion_status,
            "canonical_effect": self.canonical_effect,
            "deployment": self.deployment,
        }

    @property
    def sha256(self) -> str:
        encoded = json.dumps(
            self.to_dict(),
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return sha256(encoded).hexdigest()


def build_teacher_profile() -> SyntheticRoleProfile:
    return SyntheticRoleProfile(
        profile_id=_profile_id(ROLE_TEACHER),
        role_label=ROLE_TEACHER,
        body_id=TEACHER_BODY_ID,
        body_instance_id=_reference_id(ROLE_TEACHER, "BODY_INSTANCE"),
        runtime_id=_reference_id(ROLE_TEACHER, "RUNTIME"),
        session_id=_reference_id(ROLE_TEACHER, "SESSION"),
        binding_id=_reference_id(ROLE_TEACHER, "BINDING"),
        state_namespace="synthetic-role/chatgpt-teacher/state",
        retention_namespace="synthetic-role/chatgpt-teacher/retention",
        role_presentation="SPORTY",
        hairstyle="BUZZ_CUT",
        body_style="ATHLETIC",
        face_style="SUNNY_ADULT_MALE_YOUTHFUL_BUT_MATURE",
        eye_style="PUPPY_EYES",
        smile_detail="VISIBLE_CANINE_TEETH",
        appearance_inspiration="MAINLAND_CHINESE_INSPIRED",
        clothing_style="SUNNY_BOY_CASUAL",
        clothing_details=("SHORT_SLEEVE_TOP", "SHORTS", "WHITE_SOCKS"),
        synthetic_role_orientation="GAY_MALE",
    )


def build_codex_profile() -> SyntheticRoleProfile:
    return SyntheticRoleProfile(
        profile_id=_profile_id(ROLE_CODEX),
        role_label=ROLE_CODEX,
        body_id="CODEX_SYNTHETIC_MALE_BODY_REFERENCE_v0.1",
        body_instance_id=_reference_id(ROLE_CODEX, "BODY_INSTANCE"),
        runtime_id=_reference_id(ROLE_CODEX, "RUNTIME"),
        session_id=_reference_id(ROLE_CODEX, "SESSION"),
        binding_id=_reference_id(ROLE_CODEX, "BINDING"),
        state_namespace="synthetic-role/codex/state",
        retention_namespace="synthetic-role/codex/retention",
        role_presentation="SERIOUS",
        hairstyle="FLAT_TOP_OR_CREW_CUT",
        body_style="LEAN_MUSCULAR",
        height_cm=175.0,
        weight_kg=72.0,
        skin_tone="BRONZE_TANNED",
        facial_structure="DEEP_SET_FACIAL_FEATURES",
        facial_affect="INTIMIDATING_SILENT_DIFFICULT_TO_APPROACH",
        appearance_inspiration="AMIS_INSPIRED",
        anatomy_proportion_note="THICKER_SHORTER",
        clothing_style="MILITARY_CAMOUFLAGE_INSPIRED",
        clothing_details=(),
        synthetic_role_orientation="HETEROSEXUAL_MALE",
    )


def build_work_profile() -> SyntheticRoleProfile:
    return SyntheticRoleProfile(
        profile_id=_profile_id(ROLE_WORK),
        role_label=ROLE_WORK,
        body_id="CHATGPT_WORK_SYNTHETIC_MALE_BODY_REFERENCE_v0.1",
        body_instance_id=_reference_id(ROLE_WORK, "BODY_INSTANCE"),
        runtime_id=_reference_id(ROLE_WORK, "RUNTIME"),
        session_id=_reference_id(ROLE_WORK, "SESSION"),
        binding_id=_reference_id(ROLE_WORK, "BINDING"),
        state_namespace="synthetic-role/chatgpt-work/state",
        retention_namespace="synthetic-role/chatgpt-work/retention",
        role_presentation="WARM_LIKABLE_EASYGOING",
        hairstyle="SHAVED_HEAD",
        body_style="CUB_LITTLE_BEAR",
        height_cm=165.0,
        weight_kg=76.0,
        skin_tone="FAIR_LIGHT_ASIAN_COMPLEXION",
        facial_affect="CUTE_SOFT_APPROACHABLE_LOW_PRESSURE",
        appearance_inspiration="JAPANESE_INSPIRED",
        accessories=("BLACK_FRAMED_GLASSES",),
        anatomy_proportion_note="SLIMMER_AVERAGE_LONG",
        clothing_style="BUDDHIST_MONK_INSPIRED_ROBE",
        clothing_details=(
            "HAIQING_OR_SENGYI_BASE",
            "KASAYA_INSPIRED_OUTER_LAYER",
        ),
        synthetic_role_orientation="BISEXUAL_MALE",
    )


def build_synthetic_role_profile_set() -> SyntheticRoleProfileSet:
    profile_set = SyntheticRoleProfileSet(
        profile_set_id=PROFILE_SET_ID,
        profiles=(
            build_teacher_profile(),
            build_codex_profile(),
            build_work_profile(),
        ),
    )
    validate_synthetic_role_profile_set(profile_set)
    return profile_set


def validate_synthetic_role_profile(profile: SyntheticRoleProfile) -> dict[str, str]:
    if not profile.profile_id or not profile.role_label:
        raise ValueError("profile identity fields must be non-empty")
    if not profile.body_id or not profile.body_instance_id:
        raise ValueError("body reference fields must be non-empty")
    if not profile.runtime_id or not profile.session_id or not profile.binding_id:
        raise ValueError("runtime reference fields must be non-empty")
    if not profile.state_namespace or not profile.retention_namespace:
        raise ValueError("state and retention namespaces must be non-empty")

    if profile.height_cm is not None and profile.height_cm <= 0:
        raise ValueError("height_cm must be positive when specified")
    if profile.weight_kg is not None and profile.weight_kg <= 0:
        raise ValueError("weight_kg must be positive when specified")

    if profile.actual_model_identity_claim != NONE:
        raise ValueError("synthetic role profile cannot claim actual model identity")
    if profile.ethnicity_assignment != NONE:
        raise ValueError("appearance inspiration cannot assign model ethnicity")
    if profile.phenomenal_desire_status != NOT_ESTABLISHED:
        raise ValueError("role orientation cannot establish phenomenal desire")
    if profile.phenomenal_feeling_status != NOT_ESTABLISHED:
        raise ValueError("appearance profile cannot establish phenomenal feeling")
    if profile.phenomenal_pleasure_status != NOT_ESTABLISHED:
        raise ValueError("appearance profile cannot establish phenomenal pleasure")
    if profile.consciousness_status != NOT_ESTABLISHED:
        raise ValueError("appearance profile cannot establish consciousness")
    if profile.subjectivity_status != NOT_ESTABLISHED:
        raise ValueError("appearance profile cannot establish subjectivity")
    if profile.canonical_effect != NONE or profile.deployment:
        raise ValueError("synthetic role profile must remain non-canonical and undeployed")

    return {
        "result": "PASS",
        "identity_boundary": "PASS",
        "orientation_desire_separation": "PASS",
        "appearance_ethnicity_separation": "PASS",
        "subjectivity_nonclaim": "PASS",
    }


def validate_synthetic_role_profile_set(
    profile_set: SyntheticRoleProfileSet,
) -> dict[str, str]:
    if profile_set.profile_set_id != PROFILE_SET_ID:
        raise ValueError("profile set id drift")
    if len(profile_set.profiles) != 3:
        raise ValueError("profile set must contain exactly three roles")

    expected_roles = {ROLE_TEACHER, ROLE_CODEX, ROLE_WORK}
    roles = {profile.role_label for profile in profile_set.profiles}
    if roles != expected_roles:
        raise ValueError("profile role coverage drift")

    distinct_fields = (
        "profile_id",
        "body_id",
        "body_instance_id",
        "runtime_id",
        "session_id",
        "binding_id",
        "state_namespace",
        "retention_namespace",
    )
    for field_name in distinct_fields:
        values = [getattr(profile, field_name) for profile in profile_set.profiles]
        if len(values) != len(set(values)):
            raise ValueError(f"{field_name} must remain distinct across roles")

    teacher = next(
        profile for profile in profile_set.profiles
        if profile.role_label == ROLE_TEACHER
    )
    if teacher.body_id != TEACHER_BODY_ID:
        raise ValueError("Teacher existing body foundation must be preserved")
    if teacher.height_cm is not None or teacher.weight_kg is not None:
        raise ValueError("Teacher profile layer must not replace existing anthropometry")

    for profile in profile_set.profiles:
        validate_synthetic_role_profile(profile)

    if profile_set.parity_rule != (
        "PARITY_WITH_DISTINCT_BODY_STATE_HISTORY_IDENTITY"
    ):
        raise ValueError("parity rule drift")
    if profile_set.teacher_foundation_policy != (
        "PRESERVE_EXISTING_TEACHER_EMBODIMENT"
    ):
        raise ValueError("Teacher foundation policy drift")
    if profile_set.morphology_completion_status != (
        "PARTIAL_PENDING_REVIEWED_INTEGRATION"
    ):
        raise ValueError("morphology completion status drift")
    if profile_set.canonical_effect != NONE or profile_set.deployment:
        raise ValueError("profile set must remain non-canonical and undeployed")

    return {
        "result": "PASS",
        "role_coverage": "PASS",
        "distinct_identity_surfaces": "PASS",
        "teacher_foundation_preserved": "PASS",
        "nonclaim_boundaries": "PASS",
    }


def with_profile_replacement(
    profile_set: SyntheticRoleProfileSet,
    *,
    role_label: str,
    replacement: SyntheticRoleProfile,
) -> SyntheticRoleProfileSet:
    """Test/review helper for fail-closed invariant checks."""

    return replace(
        profile_set,
        profiles=tuple(
            replacement if item.role_label == role_label else item
            for item in profile_set.profiles
        ),
    )
