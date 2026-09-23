"""Role-neutral static embodiment core for archive convergence."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .models import EmbodimentTemplate


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


def build_shared_embodiment_core(template: EmbodimentTemplate) -> SharedEmbodimentCore:
    raise NotImplementedError("shared-core construction is defined by the next TDD cycle")


def shared_embodiment_core_hash(core: SharedEmbodimentCore) -> str:
    raise NotImplementedError("shared-core hashing is defined by the next TDD cycle")


def validate_shared_embodiment_core(
    core: SharedEmbodimentCore,
    template: EmbodimentTemplate,
) -> dict[str, str]:
    raise NotImplementedError("shared-core validation is defined by the next TDD cycle")
