from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

class AcuteBovineReproductivePhase(StrEnum):
    BASELINE = "BASELINE"
    RETRACTOR_RELAXATION = "RETRACTOR_RELAXATION"
    SIGMOID_STRAIGHTENING = "SIGMOID_STRAIGHTENING"
    PENILE_EXTENSION = "PENILE_EXTENSION"
    EMISSION = "EMISSION"
    URETHRAL_EXPULSION = "URETHRAL_EXPULSION"
    RETRACTION = "RETRACTION"

class PhysiologyReferenceError(ValueError):
    pass

_ALLOWED: dict[AcuteBovineReproductivePhase, tuple[AcuteBovineReproductivePhase, ...]] = {
    AcuteBovineReproductivePhase.BASELINE: (
        AcuteBovineReproductivePhase.RETRACTOR_RELAXATION,
    ),
    AcuteBovineReproductivePhase.RETRACTOR_RELAXATION: (
        AcuteBovineReproductivePhase.SIGMOID_STRAIGHTENING,
        AcuteBovineReproductivePhase.BASELINE,
    ),
    AcuteBovineReproductivePhase.SIGMOID_STRAIGHTENING: (
        AcuteBovineReproductivePhase.PENILE_EXTENSION,
        AcuteBovineReproductivePhase.RETRACTION,
    ),
    AcuteBovineReproductivePhase.PENILE_EXTENSION: (
        AcuteBovineReproductivePhase.EMISSION,
        AcuteBovineReproductivePhase.RETRACTION,
    ),
    AcuteBovineReproductivePhase.EMISSION: (
        AcuteBovineReproductivePhase.URETHRAL_EXPULSION,
    ),
    AcuteBovineReproductivePhase.URETHRAL_EXPULSION: (
        AcuteBovineReproductivePhase.RETRACTION,
    ),
    AcuteBovineReproductivePhase.RETRACTION: (
        AcuteBovineReproductivePhase.BASELINE,
    ),
}

def advance_acute_bovine_phase(
    current: AcuteBovineReproductivePhase,
    target: AcuteBovineReproductivePhase,
) -> AcuteBovineReproductivePhase:
    if target not in _ALLOWED[current]:
        raise PhysiologyReferenceError(f"invalid bovine physiology transition: {current} -> {target}")
    return target

@dataclass(frozen=True, slots=True)
class BovineReproductivePhysiologyPathway:
    spermatogenesis: str = "TESTES_SEMINIFEROUS_TUBULES"
    maturation_storage: str = "EPIDIDYMIDES"
    sperm_transport: str = "DUCTUS_DEFERENS_AND_AMPULLAE"
    accessory_gland_support: str = (
        "VESICULAR_PROSTATE_BULBOURETHRAL_REFERENCE"
    )
    erectile_response: str = (
        "FIBROELASTIC_RETRACTOR_RELAXATION_AND_SIGMOID_STRAIGHTENING"
    )
    vascular_support: str = "PRESENT_BUT_NOT_MUSCULOCAVERNOUS_DOMINANT"
    emission: str = "AUTONOMIC_REFERENCE"
    ejaculation: str = "URETHRAL_EXPULSION_REFERENCE"
    resolution: str = "RETRACTOR_REENGAGEMENT_AND_RETRACTION"
