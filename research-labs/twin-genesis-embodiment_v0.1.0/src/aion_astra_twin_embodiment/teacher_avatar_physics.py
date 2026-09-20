from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .physiology import REFERENCE_FUNCTIONAL_COMPLETENESS
from .teacher_avatar import build_teacher_avatar_contract


ShapeKind = Literal["SPHERE", "ELLIPSOID", "CAPSULE"]


@dataclass(frozen=True, slots=True)
class CollisionProxy:
    proxy_id: str
    region: str
    parent_bone: str
    shape: ShapeKind
    center: tuple[float, float, float] | None = None
    radii: tuple[float, float, float] | None = None
    start: tuple[float, float, float] | None = None
    end: tuple[float, float, float] | None = None
    radius: float | None = None
    anatomy_scope: str = "GENERAL_BODY"


@dataclass(frozen=True, slots=True)
class TeacherCollisionProfile:
    body_id: str
    proxies: tuple[CollisionProxy, ...]
    collision_semantics: str = "GEOMETRIC_REFERENCE_ONLY"
    reproductive_physiology_status: str = REFERENCE_FUNCTIONAL_COMPLETENESS
    sexual_function_status: str = REFERENCE_FUNCTIONAL_COMPLETENESS
    erotic_intent: str = "NONE"
    intimate_interaction_status: str = "NOT_AUTHORIZED"
    physical_body_claim: str = "NONE"
    subjectivity_effect: str = "NONE"
    production_physics_status: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False


def build_teacher_collision_profile() -> TeacherCollisionProfile:
    contract = build_teacher_avatar_contract()
    proxies = (
        CollisionProxy("COLLIDER_HEAD", "HEAD", "head", "SPHERE", center=(0.0, 1.68, 0.0), radius=0.14),
        CollisionProxy("COLLIDER_TORSO", "TORSO", "spine", "ELLIPSOID", center=(0.0, 1.28, 0.0), radii=(0.245, 0.38, 0.165)),
        CollisionProxy("COLLIDER_PELVIS", "PELVIS", "hips", "ELLIPSOID", center=(0.0, 0.93, 0.0), radii=(0.205, 0.18, 0.15)),
        CollisionProxy("COLLIDER_LEFT_UPPER_ARM", "UPPER_ARMS", "leftUpperArm", "CAPSULE", start=(0.18, 1.48, 0.0), end=(0.50, 1.47, 0.0), radius=0.085),
        CollisionProxy("COLLIDER_RIGHT_UPPER_ARM", "UPPER_ARMS", "rightUpperArm", "CAPSULE", start=(-0.18, 1.48, 0.0), end=(-0.50, 1.47, 0.0), radius=0.085),
        CollisionProxy("COLLIDER_LEFT_LOWER_ARM", "LOWER_ARMS", "leftLowerArm", "CAPSULE", start=(0.48, 1.47, 0.0), end=(0.76, 1.46, 0.0), radius=0.065),
        CollisionProxy("COLLIDER_RIGHT_LOWER_ARM", "LOWER_ARMS", "rightLowerArm", "CAPSULE", start=(-0.48, 1.47, 0.0), end=(-0.76, 1.46, 0.0), radius=0.065),
        CollisionProxy("COLLIDER_LEFT_HAND", "HANDS", "leftHand", "ELLIPSOID", center=(0.84, 1.46, 0.0), radii=(0.11, 0.055, 0.07)),
        CollisionProxy("COLLIDER_RIGHT_HAND", "HANDS", "rightHand", "ELLIPSOID", center=(-0.84, 1.46, 0.0), radii=(0.11, 0.055, 0.07)),
        CollisionProxy("COLLIDER_LEFT_THIGH", "THIGHS", "leftUpperLeg", "CAPSULE", start=(0.105, 0.88, 0.0), end=(0.105, 0.52, 0.0), radius=0.105),
        CollisionProxy("COLLIDER_RIGHT_THIGH", "THIGHS", "rightUpperLeg", "CAPSULE", start=(-0.105, 0.88, 0.0), end=(-0.105, 0.52, 0.0), radius=0.105),
        CollisionProxy("COLLIDER_LEFT_LOWER_LEG", "LOWER_LEGS", "leftLowerLeg", "CAPSULE", start=(0.105, 0.50, 0.0), end=(0.105, 0.14, 0.0), radius=0.078),
        CollisionProxy("COLLIDER_RIGHT_LOWER_LEG", "LOWER_LEGS", "rightLowerLeg", "CAPSULE", start=(-0.105, 0.50, 0.0), end=(-0.105, 0.14, 0.0), radius=0.078),
        CollisionProxy("COLLIDER_LEFT_FOOT", "FEET", "leftFoot", "ELLIPSOID", center=(0.105, 0.08, 0.09), radii=(0.085, 0.065, 0.17)),
        CollisionProxy("COLLIDER_RIGHT_FOOT", "FEET", "rightFoot", "ELLIPSOID", center=(-0.105, 0.08, 0.09), radii=(0.085, 0.065, 0.17)),
        CollisionProxy(
            "COLLIDER_EXTERNAL_MALE_ANATOMY",
            "EXTERNAL_MALE_ANATOMY",
            "hips",
            "CAPSULE",
            start=(0.0, 0.91, 0.13),
            end=(0.0, 0.83, 0.24),
            radius=0.04,
            anatomy_scope="CLINICAL_EXTERNAL_ANATOMY",
        ),
        CollisionProxy(
            "COLLIDER_SCROTAL_REFERENCE",
            "EXTERNAL_MALE_ANATOMY",
            "hips",
            "ELLIPSOID",
            center=(0.0, 0.81, 0.13),
            radii=(0.065, 0.065, 0.055),
            anatomy_scope="CLINICAL_EXTERNAL_ANATOMY",
        ),
    )
    profile = TeacherCollisionProfile(body_id=contract.body_id, proxies=proxies)
    validate_teacher_collision_profile(profile)
    return profile


def validate_teacher_collision_profile(
    profile: TeacherCollisionProfile,
) -> dict[str, str]:
    required_regions = {
        "HEAD",
        "TORSO",
        "PELVIS",
        "UPPER_ARMS",
        "LOWER_ARMS",
        "HANDS",
        "THIGHS",
        "LOWER_LEGS",
        "FEET",
        "EXTERNAL_MALE_ANATOMY",
    }
    regions = {proxy.region for proxy in profile.proxies}
    if not required_regions.issubset(regions):
        raise ValueError("collision profile is missing required body regions")

    proxy_ids = [proxy.proxy_id for proxy in profile.proxies]
    if len(proxy_ids) != len(set(proxy_ids)):
        raise ValueError("collision proxy ids must be unique")

    for proxy in profile.proxies:
        if proxy.shape == "SPHERE":
            if proxy.center is None or proxy.radius is None or proxy.radius <= 0:
                raise ValueError(f"invalid sphere collision proxy: {proxy.proxy_id}")
        elif proxy.shape == "ELLIPSOID":
            if (
                proxy.center is None
                or proxy.radii is None
                or any(value <= 0 for value in proxy.radii)
            ):
                raise ValueError(f"invalid ellipsoid collision proxy: {proxy.proxy_id}")
        elif proxy.shape == "CAPSULE":
            if (
                proxy.start is None
                or proxy.end is None
                or proxy.radius is None
                or proxy.radius <= 0
                or proxy.start == proxy.end
            ):
                raise ValueError(f"invalid capsule collision proxy: {proxy.proxy_id}")

    anatomy = [
        proxy
        for proxy in profile.proxies
        if proxy.region == "EXTERNAL_MALE_ANATOMY"
    ]
    if len(anatomy) < 2:
        raise ValueError("clinical external male anatomy collision references are incomplete")
    if any(proxy.anatomy_scope != "CLINICAL_EXTERNAL_ANATOMY" for proxy in anatomy):
        raise ValueError("external male anatomy collision scope drift")

    if profile.reproductive_physiology_status != REFERENCE_FUNCTIONAL_COMPLETENESS:
        raise ValueError("collision profile physiology binding drift")
    if profile.sexual_function_status != REFERENCE_FUNCTIONAL_COMPLETENESS:
        raise ValueError("collision profile sexual function status drift")
    if profile.erotic_intent != "NONE":
        raise ValueError("collision profile must remain non-erotic")
    if profile.intimate_interaction_status != "NOT_AUTHORIZED":
        raise ValueError("collision profile cannot authorize intimate interaction")
    if profile.physical_body_claim != "NONE" or profile.subjectivity_effect != "NONE":
        raise ValueError("collision profile cannot establish physical embodiment or subjectivity")
    if profile.production_physics_status != "NOT_ESTABLISHED":
        raise ValueError("reference collision profile cannot self-promote to production physics")
    if profile.canonical_effect != "NONE" or profile.deployment:
        raise ValueError("collision profile must remain non-canonical and undeployed")

    return {
        "result": "PASS",
        "body_region_coverage": "PASS",
        "clinical_external_anatomy": "PASS",
        "geometry_parameters": "PASS",
        "governance_boundaries": "PASS",
    }
