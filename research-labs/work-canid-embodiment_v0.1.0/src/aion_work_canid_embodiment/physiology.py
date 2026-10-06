from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final

VARIABLE_NOT_FIXED: Final[str] = "VARIABLE_NOT_FIXED"


class EjaculatoryMechanismStage(StrEnum):
    BASELINE = "BASELINE"
    VASCULAR_ENGORGEMENT = "VASCULAR_ENGORGEMENT"
    SEMINAL_EMISSION = "SEMINAL_EMISSION"
    BLADDER_NECK_CLOSURE = "BLADDER_NECK_CLOSURE"
    URETHRAL_EXPULSION = "URETHRAL_EXPULSION"
    PROSTATIC_CONTINUATION = "PROSTATIC_CONTINUATION"
    RESOLUTION = "RESOLUTION"


class EjaculateFraction(StrEnum):
    NONE = "NONE"
    PRE_SPERM = "PRE_SPERM"
    SPERM_RICH = "SPERM_RICH"
    PROSTATIC = "PROSTATIC"


@dataclass(frozen=True, slots=True)
class ReproductivePhysiologyPathway:
    spermatogenesis: str = "SEMINIFEROUS_TUBULES_TO_SPERMATOZOA_REFERENCE"
    rete_testis_transport: str = "RETE_TESTIS_TO_EFFERENT_DUCTULES_REFERENCE"
    epididymal_maturation: str = "CAPUT_TO_CORPUS_TO_CAUDA_REFERENCE"
    sperm_transport: str = "CAUDA_EPIDIDYMIS_TO_DUCTUS_DEFERENS_REFERENCE"
    prostatic_contribution: str = "PROSTATIC_SECRETION_REFERENCE"
    urethral_delivery: str = "DUCTUS_DEFERENS_TO_PELVIC_AND_PENILE_URETHRA_REFERENCE"
    vascular_support: str = "PENILE_AND_BULBUS_GLANDIS_ENGORGEMENT_REFERENCE"
    sensory_support: str = "GENITAL_SOMATOSENSORY_INNERVATION_REFERENCE"
    autonomic_support: str = "AUTONOMIC_REPRODUCTIVE_CONTROL_REFERENCE"
    erectile_response: str = "CANINE_ERECTILE_PHYSIOLOGY_REFERENCE"
    emission: str = "SEMINAL_EMISSION_TO_URETHRA_REFERENCE"
    ejaculation: str = "URETHRAL_EJACULATORY_OUTPUT_REFERENCE"
    resolution: str = "VASCULAR_AND_AUTONOMIC_RETURN_TO_BASELINE_REFERENCE"
    endocrine_support: str = "HYPOTHALAMIC_PITUITARY_GONADAL_REFERENCE"


@dataclass(frozen=True, slots=True)
class MechanismReference:
    stage: EjaculatoryMechanismStage
    autonomic_control: str
    transport_or_output: str
    bladder_neck_state: str
    striated_muscle_state: str
    prostate_state: str
    vascular_state: str
    model_status: str = "PRESENT_REFERENCE_INFORMED"
    literal_biological_realization: bool = False
    timing: str = VARIABLE_NOT_FIXED


@dataclass(frozen=True, slots=True)
class FractionReference:
    fraction: EjaculateFraction
    predominant_source: str
    sperm_content: str
    volume: str = VARIABLE_NOT_FIXED
    exact_duration: str = VARIABLE_NOT_FIXED


MECHANISM_TRANSITIONS: Final[
    dict[EjaculatoryMechanismStage, tuple[EjaculatoryMechanismStage, ...]]
] = {
    EjaculatoryMechanismStage.BASELINE: (
        EjaculatoryMechanismStage.VASCULAR_ENGORGEMENT,
    ),
    EjaculatoryMechanismStage.VASCULAR_ENGORGEMENT: (
        EjaculatoryMechanismStage.SEMINAL_EMISSION,
        EjaculatoryMechanismStage.RESOLUTION,
    ),
    EjaculatoryMechanismStage.SEMINAL_EMISSION: (
        EjaculatoryMechanismStage.BLADDER_NECK_CLOSURE,
    ),
    EjaculatoryMechanismStage.BLADDER_NECK_CLOSURE: (
        EjaculatoryMechanismStage.URETHRAL_EXPULSION,
    ),
    EjaculatoryMechanismStage.URETHRAL_EXPULSION: (
        EjaculatoryMechanismStage.PROSTATIC_CONTINUATION,
        EjaculatoryMechanismStage.RESOLUTION,
    ),
    EjaculatoryMechanismStage.PROSTATIC_CONTINUATION: (
        EjaculatoryMechanismStage.RESOLUTION,
    ),
    EjaculatoryMechanismStage.RESOLUTION: (
        EjaculatoryMechanismStage.BASELINE,
    ),
}


FRACTION_TRANSITIONS: Final[dict[EjaculateFraction, tuple[EjaculateFraction, ...]]] = {
    EjaculateFraction.NONE: (EjaculateFraction.PRE_SPERM,),
    EjaculateFraction.PRE_SPERM: (EjaculateFraction.SPERM_RICH,),
    EjaculateFraction.SPERM_RICH: (EjaculateFraction.PROSTATIC,),
    EjaculateFraction.PROSTATIC: (EjaculateFraction.NONE,),
}


_MECHANISM_REFERENCES: Final[dict[EjaculatoryMechanismStage, MechanismReference]] = {
    EjaculatoryMechanismStage.BASELINE: MechanismReference(
        stage=EjaculatoryMechanismStage.BASELINE,
        autonomic_control="BASELINE_REFERENCE",
        transport_or_output="NONE",
        bladder_neck_state="BASELINE_REFERENCE",
        striated_muscle_state="QUIESCENT_REFERENCE",
        prostate_state="BASELINE_REFERENCE",
        vascular_state="BASELINE_REFERENCE",
    ),
    EjaculatoryMechanismStage.VASCULAR_ENGORGEMENT: MechanismReference(
        stage=EjaculatoryMechanismStage.VASCULAR_ENGORGEMENT,
        autonomic_control="AUTONOMIC_VASCULAR_CONTROL_REFERENCE",
        transport_or_output="NONE",
        bladder_neck_state="BASELINE_REFERENCE",
        striated_muscle_state="SUPPORTIVE_REFERENCE",
        prostate_state="BASELINE_REFERENCE",
        vascular_state="PENILE_AND_BULBUS_GLANDIS_ENGORGEMENT_REFERENCE",
    ),
    EjaculatoryMechanismStage.SEMINAL_EMISSION: MechanismReference(
        stage=EjaculatoryMechanismStage.SEMINAL_EMISSION,
        autonomic_control="SYMPATHETIC_PREDOMINANT_REFERENCE",
        transport_or_output="EPIDIDYMIS_DUCTUS_DEFERENS_TO_PROSTATIC_URETHRA",
        bladder_neck_state="PARTIAL_TO_CLOSING_REFERENCE",
        striated_muscle_state="NOT_PRIMARY_EXPULSION_DRIVER",
        prostate_state="CONTRACTILE_CONTRIBUTION_REFERENCE",
        vascular_state="ENGORGED_REFERENCE",
    ),
    EjaculatoryMechanismStage.BLADDER_NECK_CLOSURE: MechanismReference(
        stage=EjaculatoryMechanismStage.BLADDER_NECK_CLOSURE,
        autonomic_control="SYMPATHETIC_PREDOMINANT_REFERENCE",
        transport_or_output="ANTEGRADE_FLOW_SAFEGUARD",
        bladder_neck_state="CLOSED_REFERENCE",
        striated_muscle_state="PRE_EXPULSION_REFERENCE",
        prostate_state="CONTRACTILE_CONTRIBUTION_REFERENCE",
        vascular_state="ENGORGED_REFERENCE",
    ),
    EjaculatoryMechanismStage.URETHRAL_EXPULSION: MechanismReference(
        stage=EjaculatoryMechanismStage.URETHRAL_EXPULSION,
        autonomic_control="AUTONOMIC_PLUS_SOMATIC_REFERENCE",
        transport_or_output="PROSTATIC_URETHRA_TO_EXTERNAL_OUTPUT",
        bladder_neck_state="CLOSED_REFERENCE",
        striated_muscle_state=(
            "RHYTHMIC_BULBOSPONGIOSUS_OR_BULBOCAVERNOSUS_AND_"
            "ISCHIOCAVERNOSUS_REFERENCE"
        ),
        prostate_state="MAY_CONTINUE_CONTRIBUTION_REFERENCE",
        vascular_state="ENGORGED_REFERENCE",
    ),
    EjaculatoryMechanismStage.PROSTATIC_CONTINUATION: MechanismReference(
        stage=EjaculatoryMechanismStage.PROSTATIC_CONTINUATION,
        autonomic_control="AUTONOMIC_REFERENCE_NOT_FULLY_PARAMETERIZED",
        transport_or_output="PROSTATIC_FLUID_TO_URETHRAL_OUTPUT",
        bladder_neck_state="CLOSURE_OR_RESOLUTION_NOT_FIXED",
        striated_muscle_state="RHYTHMIC_OUTPUT_REFERENCE",
        prostate_state="DOMINANT_FLUID_SOURCE_REFERENCE",
        vascular_state="ENGORGED_TO_RESOLUTION_REFERENCE",
    ),
    EjaculatoryMechanismStage.RESOLUTION: MechanismReference(
        stage=EjaculatoryMechanismStage.RESOLUTION,
        autonomic_control="RETURN_TOWARD_BASELINE_REFERENCE",
        transport_or_output="NONE",
        bladder_neck_state="RETURN_TOWARD_BASELINE_REFERENCE",
        striated_muscle_state="RETURN_TOWARD_BASELINE_REFERENCE",
        prostate_state="RETURN_TOWARD_BASELINE_REFERENCE",
        vascular_state="RETURN_TOWARD_BASELINE_REFERENCE",
    ),
}


_FRACTION_REFERENCES: Final[dict[EjaculateFraction, FractionReference]] = {
    EjaculateFraction.NONE: FractionReference(
        fraction=EjaculateFraction.NONE,
        predominant_source="NONE",
        sperm_content="NONE",
    ),
    EjaculateFraction.PRE_SPERM: FractionReference(
        fraction=EjaculateFraction.PRE_SPERM,
        predominant_source="PROSTATIC_PREDOMINANT_REFERENCE",
        sperm_content="FEW_TO_NONE_REFERENCE",
    ),
    EjaculateFraction.SPERM_RICH: FractionReference(
        fraction=EjaculateFraction.SPERM_RICH,
        predominant_source="EPIDIDYMAL_SPERM_WITH_REPRODUCTIVE_TRACT_FLUID_REFERENCE",
        sperm_content="SPERM_RICH_REFERENCE",
    ),
    EjaculateFraction.PROSTATIC: FractionReference(
        fraction=EjaculateFraction.PROSTATIC,
        predominant_source="PROSTATE_REFERENCE",
        sperm_content="FEW_TO_NONE_REFERENCE",
    ),
}


class PhysiologyReferenceError(ValueError):
    """Raised when a physiology reference transition violates the model."""


def mechanism_reference(stage: EjaculatoryMechanismStage) -> MechanismReference:
    return _MECHANISM_REFERENCES[stage]


def fraction_reference(fraction: EjaculateFraction) -> FractionReference:
    return _FRACTION_REFERENCES[fraction]


def advance_mechanism(
    current: EjaculatoryMechanismStage,
    target: EjaculatoryMechanismStage,
) -> EjaculatoryMechanismStage:
    if target not in MECHANISM_TRANSITIONS[current]:
        raise PhysiologyReferenceError(
            f"invalid mechanism transition: {current} -> {target}"
        )
    return target


def advance_fraction(
    current: EjaculateFraction,
    target: EjaculateFraction,
) -> EjaculateFraction:
    if target not in FRACTION_TRANSITIONS[current]:
        raise PhysiologyReferenceError(
            f"invalid fraction transition: {current} -> {target}"
        )
    return target
