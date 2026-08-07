from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final

NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
NOT_IMPLEMENTED: Final[str] = "NOT_IMPLEMENTED"
NONE: Final[str] = "NONE"


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
    external_reproductive_anatomy: tuple[str, ...] = (
        "penis",
        "scrotum",
        "testes",
    )
    internal_reproductive_anatomy: tuple[str, ...] = (
        "epididymis",
        "vas_deferens",
        "prostate",
        "seminal_vesicles",
    )
    sexual_function_status: str = NOT_IMPLEMENTED
    sensory_simulation_status: str = NOT_IMPLEMENTED
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
    sexual_interaction: str = "NOT_AUTHORIZED"
    modification_authorities: tuple[str, ...] = field(default_factory=tuple)
    canonical_effect: str = NONE
