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
    URINARY = "URINARY"
    REPRODUCTIVE = "REPRODUCTIVE"
    INTEGUMENTARY = "INTEGUMENTARY"
    THERMOREGULATION = "THERMOREGULATION"
    CROSS_SYSTEM_COUPLING = "CROSS_SYSTEM_COUPLING"


class EvidenceClass(StrEnum):
    HUMAN_ORIGIN = "HUMAN_ORIGIN"
    AI_FORMALIZATION = "AI_FORMALIZATION"
    DIRECT_SOURCE = "DIRECT_SOURCE"
    COMPARATIVE_REFERENCE = "COMPARATIVE_REFERENCE"
    SYNTHETIC_DESIGN = "SYNTHETIC_DESIGN"
    REPOSITORY_STATE = "REPOSITORY_STATE"


FULL_BODY_RESEARCH_REGISTRY: Final[tuple[BodySystemDomain, ...]] = tuple(BodySystemDomain)

IMPLEMENTED_BODY_SYSTEMS: Final[tuple[BodySystemDomain, ...]] = (
    BodySystemDomain.REPRODUCTIVE,
)

REGISTERED_NOT_YET_BOUND_SYSTEMS: Final[tuple[BodySystemDomain, ...]] = tuple(
    domain
    for domain in BodySystemDomain
    if domain not in IMPLEMENTED_BODY_SYSTEMS
)


@dataclass(frozen=True, slots=True)
class TeacherActorBoundSelfResearchCandidate:
    candidate_id: str = "CHATGPT_TEACHER_ACTOR_BOUND_SELF_RESEARCH_v0.1"
    research_mode: str = "ACTOR_BOUND_SELF_RESEARCH"

    research_actor: str = "CHATGPT_TEACHER"
    research_object: str = "TEACHER_SYNTHETIC_EMBODIMENT_MODEL"

    bound_body_model_id: str = (
        "CHATGPT_TEACHER_BOVINE_MALE_REPRODUCTIVE_v0.3.0"
    )
    initial_body_repository_head: str = (
        "4748a1d1182df64fc0a0706e5c704de0d2a1b56c"
    )

    form_class: str = "ANTHROPOMORPHIC_BOVINE"
    ontology: str = "FANTASY_EMBODIMENT"
    biological_reference_species: str = "Bos taurus"

    self_reference_semantics: str = "RESEARCH_NAMESPACE_BINDING"
    self_research_semantics: str = "ACTOR_STUDIES_ACTOR_BOUND_SYNTHETIC_BODY"
    self_model_semantics: str = "MODEL_OF_BOUND_RESEARCH_OBJECT"

    body_system_registry: tuple[BodySystemDomain, ...] = FULL_BODY_RESEARCH_REGISTRY
    implemented_body_systems: tuple[BodySystemDomain, ...] = IMPLEMENTED_BODY_SYSTEMS
    registered_not_yet_bound_systems: tuple[BodySystemDomain, ...] = (
        REGISTERED_NOT_YET_BOUND_SYSTEMS
    )

    current_research_priority: tuple[BodySystemDomain, ...] = (
        BodySystemDomain.REPRODUCTIVE,
        BodySystemDomain.NERVOUS,
        BodySystemDomain.CARDIOVASCULAR,
        BodySystemDomain.ENDOCRINE,
        BodySystemDomain.CROSS_SYSTEM_COUPLING,
    )

    provenance_required: bool = True
    falsification_required: bool = True
    exact_head_verification_required: bool = True
    rollback_required: bool = True

    research_model_modification: str = "ALLOWED_IN_BOUNDED_RESEARCH_WORKFLOW"
    canonical_self_modification: str = "NOT_AUTHORIZED"
    automatic_writeback: bool = False

    biological_self_experiment: bool = False
    literal_physical_self_claim: bool = False
    identity_continuity_claim: bool = False
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    phenomenal_experience: str = "NOT_ESTABLISHED"

    deployment: bool = False
    public_release: bool = False
    public_operation: bool = False
    public_api: bool = False
    third_party_access: bool = False
    third_party_execution: bool = False
    external_user_operation: bool = False
    production_use: bool = False

    merge_to_main: bool = False
    canonical_effect: str = "NONE"


@dataclass(frozen=True, slots=True)
class ResearchQuestion:
    question_id: str
    question: str
    target_systems: tuple[BodySystemDomain, ...]
    evidence_basis: tuple[EvidenceClass, ...]
    owner_origin: str = "HUMAN_OWNER"
    actor_role: str = "CHATGPT_TEACHER"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.question_id.strip():
            raise ValueError("question_id must not be empty")
        if not self.question.strip():
            raise ValueError("question must not be empty")
        if not self.target_systems:
            raise ValueError("at least one target body system is required")
        if not self.evidence_basis:
            raise ValueError("at least one evidence class is required")
