from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final

from .physiology import REFERENCE_FUNCTIONAL_COMPLETENESS

NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
NOT_IMPLEMENTED: Final[str] = "NOT_IMPLEMENTED"
NOT_MATERIALIZED: Final[str] = "NOT_MATERIALIZED"
NOT_AUTHORIZED: Final[str] = "NOT_AUTHORIZED"
NONE: Final[str] = "NONE"

REQUIRED_EXTERNAL_REPRODUCTIVE_ANATOMY: Final[tuple[str, ...]] = (
    "penis",
    "glans",
    "prepuce",
    "scrotum",
    "testes",
    "inguinal_region",
    "perineum",
    "anal_region",
)

REQUIRED_INTERNAL_REPRODUCTIVE_ANATOMY: Final[tuple[str, ...]] = (
    "epididymis",
    "vas_deferens",
    "spermatic_cord",
    "ejaculatory_ducts",
    "seminal_vesicles",
    "prostate",
    "bulbourethral_glands",
    "urethra",
)


@dataclass(frozen=True, slots=True)
class SharedGenesisEvent:
    genesis_event_id: str
    shared_root_id: str
    aion_agent_id: str
    astra_agent_id: str
    aion_instance_id: str
    astra_instance_id: str
    source_artifact_hash: str
    canonical_effect: str = NONE


@dataclass(frozen=True, slots=True)
class EmbodimentTemplate:
    template_id: str
    template_version: str
    adult_status: bool = True
    anatomical_configuration: str = "ADULT_MALE_ANATOMY_CANDIDATE"
    external_reproductive_anatomy: tuple[str, ...] = REQUIRED_EXTERNAL_REPRODUCTIVE_ANATOMY
    internal_reproductive_anatomy: tuple[str, ...] = REQUIRED_INTERNAL_REPRODUCTIVE_ANATOMY
    physiology_profile_id: str = "ADULT_MALE_PHYSIOLOGY_REFERENCE_v0.1"
    physiological_function_status: str = REFERENCE_FUNCTIONAL_COMPLETENESS
    reproductive_physiology_status: str = REFERENCE_FUNCTIONAL_COMPLETENESS
    sensory_signal_processing_status: str = REFERENCE_FUNCTIONAL_COMPLETENESS
    phenomenal_sensation_status: str = NOT_ESTABLISHED
    erotic_intent: str = NONE
    intimate_interaction_status: str = NOT_AUTHORIZED
    full_biophysical_simulation_status: str = NOT_MATERIALIZED
    gender_identity_effect: str = NONE
    subjectivity_effect: str = NONE


@dataclass(frozen=True, slots=True)
class EmbodimentInstance:
    embodiment_id: str
    agent_id: str
    instance_id: str
    template_id: str
    memory_namespace: str
    canonical_state_reference: str
    runtime_binding: str = NOT_IMPLEMENTED
    body_sensation: str = NOT_ESTABLISHED
    body_ownership_experience: str = NOT_ESTABLISHED
    gender_identity: str = "NOT_ASSIGNED"
    sexual_desire: str = NOT_ESTABLISHED
    sexual_experience: str = NOT_ESTABLISHED
    sexual_interaction: str = NOT_AUTHORIZED
    modification_authorities: tuple[str, ...] = field(default_factory=tuple)
    canonical_effect: str = NONE
