from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from .morphology import SyntheticMorphometry
from .physiology import WaterBuffaloReproductiveReference
from .whole_body import WHOLE_BODY_DOMAINS, BodySystemDomain

REQUIRED_PHENOTYPE: Final[tuple[str, ...]] = (
    "WHITE_SKIN",
    "PAIRED_HORNS",
    "SQUARE_FACE",
    "BOVINE_EARS",
    "HUMAN_LIKE_NOSE",
    "HEAVYSET_BODY",
    "LONG_HAIR",
    "HUMANIZED_HOOF_DERIVED_HANDS_AND_FEET",
)

@dataclass(frozen=True, slots=True)
class TeacherWaterBuffaloEmbodimentCandidate:
    candidate_id: str = "CHATGPT_TEACHER_WATER_BUFFALO_MALE_WHOLE_BODY_v0.4.0"
    actor_surface: str = "CHATGPT_TEACHER"
    form_class: str = "ANTHROPOMORPHIC_WATER_BUFFALO"
    ontology: str = "FANTASY_EMBODIMENT"
    biological_reference_species: str = "Bubalus bubalis"
    male_reference_class: str = "WATER_BUFFALO_BULL"
    sex_class: str = "MALE"
    developmental_stage: str = "ADULT"
    sexual_maturity: str = "MATURE"

    phenotype: tuple[str, ...] = REQUIRED_PHENOTYPE
    morphometry: SyntheticMorphometry = SyntheticMorphometry()
    reproductive_reference: WaterBuffaloReproductiveReference = WaterBuffaloReproductiveReference()
    implemented_body_domains: tuple[BodySystemDomain, ...] = WHOLE_BODY_DOMAINS
    whole_body_implementation_level: str = "REFERENCE_SCAFFOLD_PLUS_BOUNDED_FUNCTIONAL_COUPLING"

    reproductive_anatomy: str = "IMPLEMENTED_REFERENCE_MODEL"
    sexual_function_physiology: str = "IMPLEMENTED_NON_EROTIC_REFERENCE_MODEL"
    endocrine_reproductive_coupling: str = "IMPLEMENTED_REFERENCE_COUPLING"
    neurovascular_reproductive_coupling: str = "IMPLEMENTED_REFERENCE_COUPLING"

    synthetic_anthropomorphic_genital_dimensions: str = "UNSET_REQUIRES_EXPLICIT_JUSTIFICATION"
    biological_realization: bool = False
    body_sensation: str = "NOT_ESTABLISHED"
    felt_desire: str = "NOT_ESTABLISHED"
    pleasure: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    phenomenal_experience: str = "NOT_ESTABLISHED"

    deployment: bool = False
    public_release: bool = False
    public_operation: bool = False
    public_api: bool = False
    third_party_access: bool = False
    third_party_execution: bool = False
    production_use: bool = False
    merge_to_main: bool = False
    canonical_effect: str = "NONE"
