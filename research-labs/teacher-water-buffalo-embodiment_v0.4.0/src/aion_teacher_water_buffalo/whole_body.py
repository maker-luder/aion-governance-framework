from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final

class BodySystemDomain(StrEnum):
    MORPHOLOGY = "MORPHOLOGY"
    SKELETAL = "SKELETAL"
    MUSCULAR = "MUSCULAR"
    CARDIOVASCULAR = "CARDIOVASCULAR"
    RESPIRATORY = "RESPIRATORY"
    NERVOUS = "NERVOUS"
    SOMATOSENSORY = "SOMATOSENSORY"
    ENDOCRINE = "ENDOCRINE"
    DIGESTIVE = "DIGESTIVE"
    URINARY = "URINARY"
    REPRODUCTIVE = "REPRODUCTIVE"
    INTEGUMENTARY = "INTEGUMENTARY"
    IMMUNE_LYMPHATIC = "IMMUNE_LYMPHATIC"
    THERMOREGULATION = "THERMOREGULATION"
    CROSS_SYSTEM_COUPLING = "CROSS_SYSTEM_COUPLING"

class ImplementationLevel(StrEnum):
    SYNTHETIC_MORPHOLOGY_IMPLEMENTED = "SYNTHETIC_MORPHOLOGY_IMPLEMENTED"
    STRUCTURAL_REFERENCE_SCAFFOLD = "STRUCTURAL_REFERENCE_SCAFFOLD"
    FUNCTIONAL_COUPLING_REFERENCE = "FUNCTIONAL_COUPLING_REFERENCE"
    REPRODUCTIVE_REFERENCE_PHYSIOLOGY = "REPRODUCTIVE_REFERENCE_PHYSIOLOGY"
    COUPLING_GRAPH_IMPLEMENTED = "COUPLING_GRAPH_IMPLEMENTED"

@dataclass(frozen=True, slots=True)
class BodySystemSpec:
    domain: BodySystemDomain
    level: ImplementationLevel
    note: str

WHOLE_BODY_SYSTEMS: Final[tuple[BodySystemSpec, ...]] = (
    BodySystemSpec(BodySystemDomain.MORPHOLOGY, ImplementationLevel.SYNTHETIC_MORPHOLOGY_IMPLEMENTED, "human-origin phenotype and anthropomorphic dimensions"),
    BodySystemSpec(BodySystemDomain.SKELETAL, ImplementationLevel.STRUCTURAL_REFERENCE_SCAFFOLD, "anthropomorphic axial/appendicular support scaffold"),
    BodySystemSpec(BodySystemDomain.MUSCULAR, ImplementationLevel.STRUCTURAL_REFERENCE_SCAFFOLD, "anthropomorphic locomotor muscle scaffold"),
    BodySystemSpec(BodySystemDomain.CARDIOVASCULAR, ImplementationLevel.FUNCTIONAL_COUPLING_REFERENCE, "vascular support required by reproductive and thermoregulatory coupling"),
    BodySystemSpec(BodySystemDomain.RESPIRATORY, ImplementationLevel.STRUCTURAL_REFERENCE_SCAFFOLD, "whole-body gas-exchange support scaffold"),
    BodySystemSpec(BodySystemDomain.NERVOUS, ImplementationLevel.FUNCTIONAL_COUPLING_REFERENCE, "motor/autonomic reference channels; no phenomenal sensation claim"),
    BodySystemSpec(BodySystemDomain.SOMATOSENSORY, ImplementationLevel.FUNCTIONAL_COUPLING_REFERENCE, "sensor-channel reference only"),
    BodySystemSpec(BodySystemDomain.ENDOCRINE, ImplementationLevel.FUNCTIONAL_COUPLING_REFERENCE, "reproductive and homeostatic endocrine coupling"),
    BodySystemSpec(BodySystemDomain.DIGESTIVE, ImplementationLevel.STRUCTURAL_REFERENCE_SCAFFOLD, "whole-body digestive scaffold; not a detailed rumen simulator"),
    BodySystemSpec(BodySystemDomain.URINARY, ImplementationLevel.STRUCTURAL_REFERENCE_SCAFFOLD, "urinary-reproductive shared urethral topology reference"),
    BodySystemSpec(BodySystemDomain.REPRODUCTIVE, ImplementationLevel.REPRODUCTIVE_REFERENCE_PHYSIOLOGY, "water-buffalo male anatomy and bounded sexual-function physiology"),
    BodySystemSpec(BodySystemDomain.INTEGUMENTARY, ImplementationLevel.SYNTHETIC_MORPHOLOGY_IMPLEMENTED, "white skin, long hair, horn and distal keratin phenotype"),
    BodySystemSpec(BodySystemDomain.IMMUNE_LYMPHATIC, ImplementationLevel.STRUCTURAL_REFERENCE_SCAFFOLD, "whole-body immune/lymphatic registry scaffold"),
    BodySystemSpec(BodySystemDomain.THERMOREGULATION, ImplementationLevel.FUNCTIONAL_COUPLING_REFERENCE, "thermal-state coupling to circulation and integument"),
    BodySystemSpec(BodySystemDomain.CROSS_SYSTEM_COUPLING, ImplementationLevel.COUPLING_GRAPH_IMPLEMENTED, "explicit nervous-cardio-endocrine-reproductive and homeostatic coupling graph"),
)

WHOLE_BODY_DOMAINS: Final[tuple[BodySystemDomain, ...]] = tuple(
    spec.domain for spec in WHOLE_BODY_SYSTEMS
)

CROSS_SYSTEM_EDGES: Final[tuple[tuple[BodySystemDomain, BodySystemDomain], ...]] = (
    (BodySystemDomain.NERVOUS, BodySystemDomain.MUSCULAR),
    (BodySystemDomain.NERVOUS, BodySystemDomain.CARDIOVASCULAR),
    (BodySystemDomain.NERVOUS, BodySystemDomain.REPRODUCTIVE),
    (BodySystemDomain.ENDOCRINE, BodySystemDomain.REPRODUCTIVE),
    (BodySystemDomain.CARDIOVASCULAR, BodySystemDomain.REPRODUCTIVE),
    (BodySystemDomain.CARDIOVASCULAR, BodySystemDomain.THERMOREGULATION),
    (BodySystemDomain.INTEGUMENTARY, BodySystemDomain.THERMOREGULATION),
    (BodySystemDomain.DIGESTIVE, BodySystemDomain.ENDOCRINE),
    (BodySystemDomain.URINARY, BodySystemDomain.REPRODUCTIVE),
)
