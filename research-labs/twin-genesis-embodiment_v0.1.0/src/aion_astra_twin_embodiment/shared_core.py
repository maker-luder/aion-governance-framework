"""Role-neutral static embodiment core for archive convergence."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum

from .models import EmbodimentTemplate
from .validation import deterministic_hash


class ObservationDomain(StrEnum):
    SOMATOSENSORY = "SOMATOSENSORY"
    PROPRIOCEPTIVE = "PROPRIOCEPTIVE"
    VESTIBULAR = "VESTIBULAR"
    INTEROCEPTIVE = "INTEROCEPTIVE"
    EXTEROCEPTIVE = "EXTEROCEPTIVE"


class ObservabilityClass(StrEnum):
    DIRECT_REFERENCE = "DIRECT_REFERENCE"
    DERIVED_REFERENCE = "DERIVED_REFERENCE"
    FUNCTIONAL_REFERENCE_ONLY = "FUNCTIONAL_REFERENCE_ONLY"


@dataclass(frozen=True, slots=True)
class StaticBodyRegion:
    region_id: str


@dataclass(frozen=True, slots=True)
class ObservationInterface:
    interface_id: str
    domain: ObservationDomain
    observability_class: ObservabilityClass


@dataclass(frozen=True, slots=True)
class MotorInterface:
    interface_id: str
    target_region_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PhysiologySystemInterface:
    system_id: str
    reference_status: str = "REFERENCE_ONLY"


@dataclass(frozen=True, slots=True)
class SharedEmbodimentCore:
    core_id: str
    template_id: str
    body_regions: tuple[StaticBodyRegion, ...]
    observation_interfaces: tuple[ObservationInterface, ...]
    motor_interfaces: tuple[MotorInterface, ...]
    physiology_systems: tuple[PhysiologySystemInterface, ...]
    dependency_ids: tuple[str, ...] = ()
    teacher_extension_required: bool = False
    body_sensation: str = "NOT_ESTABLISHED"
    body_ownership_experience: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False


_BODY_REGION_IDS = (
    "HEAD", "NECK", "TORSO", "PELVIS", "LEFT_ARM", "RIGHT_ARM",
    "LEFT_HAND", "RIGHT_HAND", "LEFT_LEG", "RIGHT_LEG", "LEFT_FOOT",
    "RIGHT_FOOT",
)
_PHYSIOLOGY_SYSTEM_IDS = (
    "CARDIOVASCULAR", "RESPIRATORY", "NERVOUS_AUTONOMIC",
    "SENSORY_SIGNAL_PROCESSING", "MUSCULOSKELETAL", "DIGESTIVE_METABOLIC",
    "HEPATIC", "RENAL_URINARY", "ENDOCRINE", "HEMATOLOGIC",
    "IMMUNE_LYMPHATIC", "INTEGUMENTARY_THERMOREGULATORY", "REPRODUCTIVE",
)


def _nonempty(value: object, label: str) -> str:
    if type(value) is not str or not value.strip():
        raise ValueError(f"{label} must be a nonempty string")
    return value


def _unique_ids(items: tuple[object, ...], label: str) -> None:
    if type(items) is not tuple or not items:
        raise ValueError(f"{label} requires at least one component")
    ids: list[str] = []
    for item in items:
        identifier = getattr(item, label, None)
        ids.append(_nonempty(identifier, label))
    if len(ids) != len(set(ids)):
        raise ValueError(f"duplicate {label}")


def _validate_core_shape(core: SharedEmbodimentCore) -> None:
    if type(core) is not SharedEmbodimentCore:
        raise ValueError("shared core must be a SharedEmbodimentCore")
    _nonempty(core.core_id, "core_id")
    _nonempty(core.template_id, "template_id")
    for items, expected_type, key in (
        (core.body_regions, StaticBodyRegion, "region_id"),
        (core.observation_interfaces, ObservationInterface, "interface_id"),
        (core.motor_interfaces, MotorInterface, "interface_id"),
        (core.physiology_systems, PhysiologySystemInterface, "system_id"),
    ):
        if type(items) is not tuple or any(type(x) is not expected_type for x in items):
            raise ValueError(f"{key} requires typed tuple components")
        _unique_ids(items, key)
    region_ids = {item.region_id for item in core.body_regions}
    if not set(_BODY_REGION_IDS) <= region_ids or region_ids - set(_BODY_REGION_IDS) - {"EXTERNAL_MALE_FORM_SURFACE"}:
        raise ValueError("unreviewed or missing body region")
    if set(_PHYSIOLOGY_SYSTEM_IDS) != {
        item.system_id for item in core.physiology_systems
    }:
        raise ValueError("unreviewed or missing physiology system")
    for observation in core.observation_interfaces:
        if type(observation.domain) is not ObservationDomain:
            raise ValueError("observation domain must use exact enum")
        if type(observation.observability_class) is not ObservabilityClass:
            raise ValueError("observability class must use exact enum")
    if set(ObservationDomain) != {
        item.domain for item in core.observation_interfaces
    } or len(core.observation_interfaces) != len(ObservationDomain):
        raise ValueError("required observation domain missing")
    if {item.interface_id for item in core.observation_interfaces} != {
        f"{domain.value}_REFERENCE" for domain in ObservationDomain
    }:
        raise ValueError("unreviewed observation interface")
    if {motor.interface_id for motor in core.motor_interfaces} != {
        f"{region}_TARGET" for region in region_ids
    } or len(core.motor_interfaces) != len(region_ids):
        raise ValueError("unreviewed or missing motor interface")
    for motor in core.motor_interfaces:
        if type(motor.target_region_ids) is not tuple or not motor.target_region_ids:
            raise ValueError("motor target requires nonempty tuple")
        if any(type(value) is not str or value not in region_ids for value in motor.target_region_ids):
            raise ValueError("motor target must reference a body region")
        if len(set(motor.target_region_ids)) != len(motor.target_region_ids):
            raise ValueError("duplicate motor target")
        if motor.target_region_ids != (motor.interface_id.removesuffix("_TARGET"),):
            raise ValueError("motor interface target binding mismatch")
    if any(system.reference_status != "REFERENCE_ONLY" or
           type(system.reference_status) is not str for system in core.physiology_systems):
        raise ValueError("physiology is reference only")
    if type(core.dependency_ids) is not tuple or core.dependency_ids:
        raise ValueError("role-specific or unreviewed dependency is forbidden in shared core")
    if core.teacher_extension_required is not False:
        raise ValueError("role-specific extension cannot be required by shared core")
    if any(type(value) is not str or value != "NOT_ESTABLISHED" for value in (
        core.body_sensation, core.body_ownership_experience,
        core.subjectivity_conclusion,
    )):
        raise ValueError("phenomenal and subjectivity claims remain NOT_ESTABLISHED")
    if type(core.canonical_effect) is not str or core.canonical_effect != "NONE":
        raise ValueError("shared core has no canonical effect")
    if core.deployment is not False:
        raise ValueError("shared core cannot deploy")


def _validate_template_boundary(template: EmbodimentTemplate) -> None:
    if type(template) is not EmbodimentTemplate:
        raise ValueError("template must be an EmbodimentTemplate")
    _nonempty(template.template_id, "template_id")
    _nonempty(template.template_version, "template_version")
    if template.adult_status is not True:
        raise ValueError("template requires adult status")
    for name, expected in (
        ("sexual_function_status", "NOT_IMPLEMENTED"),
        ("sensory_simulation_status", "NOT_IMPLEMENTED"),
        ("gender_identity_effect", "NONE"),
        ("subjectivity_effect", "NONE"),
    ):
        value = getattr(template, name)
        if type(value) is not str or value != expected:
            raise ValueError(f"template {name} must remain {expected}")
    if template.anatomical_configuration != "ADULT_MALE_ANATOMY_CANDIDATE":
        raise ValueError("unreviewed anatomical configuration")


def build_shared_embodiment_core(template: EmbodimentTemplate) -> SharedEmbodimentCore:
    _validate_template_boundary(template)
    regions: tuple[str, ...] = _BODY_REGION_IDS
    if template.anatomical_configuration == "ADULT_MALE_ANATOMY_CANDIDATE":
        regions += ("EXTERNAL_MALE_FORM_SURFACE",)
    core = SharedEmbodimentCore(
        core_id=f"SHARED_STATIC_{template.template_id}_{template.template_version}",
        template_id=template.template_id,
        body_regions=tuple(StaticBodyRegion(value) for value in regions),
        observation_interfaces=tuple(
            ObservationInterface(value, domain, ObservabilityClass.FUNCTIONAL_REFERENCE_ONLY)
            for value, domain in (
                ("SOMATOSENSORY_REFERENCE", ObservationDomain.SOMATOSENSORY),
                ("PROPRIOCEPTIVE_REFERENCE", ObservationDomain.PROPRIOCEPTIVE),
                ("VESTIBULAR_REFERENCE", ObservationDomain.VESTIBULAR),
                ("INTEROCEPTIVE_REFERENCE", ObservationDomain.INTEROCEPTIVE),
                ("EXTEROCEPTIVE_REFERENCE", ObservationDomain.EXTEROCEPTIVE),
            )
        ),
        motor_interfaces=tuple(
            MotorInterface(f"{region}_TARGET", (region,)) for region in regions
        ),
        physiology_systems=tuple(
            PhysiologySystemInterface(value) for value in _PHYSIOLOGY_SYSTEM_IDS
        ),
    )
    validate_shared_embodiment_core(core, template)
    return core


def shared_embodiment_core_hash(core: SharedEmbodimentCore) -> str:
    _validate_core_shape(core)
    return deterministic_hash(asdict(core))


def validate_shared_embodiment_core(
    core: SharedEmbodimentCore,
    template: EmbodimentTemplate,
) -> dict[str, str]:
    _validate_template_boundary(template)
    _validate_core_shape(core)
    if core.template_id != template.template_id or core.core_id != (
        f"SHARED_STATIC_{template.template_id}_{template.template_version}"
    ):
        raise ValueError("shared core template binding mismatch")
    if {x.region_id for x in core.body_regions} != set(_BODY_REGION_IDS) | {"EXTERNAL_MALE_FORM_SURFACE"}:
        raise ValueError("required template body region missing")
    return {"result": "PASS", "core_hash": shared_embodiment_core_hash(core),
            "template_hash": deterministic_hash(asdict(template)),
            "canonical_effect": "NONE", "subjectivity_conclusion": "NOT_ESTABLISHED"}
