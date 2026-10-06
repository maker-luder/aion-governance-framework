from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from typing import Any

from .models import (
    BACULUM_10_30_KG_MEAN_CM,
    HUSKY_MALE_MASS_KG,
    HUSKY_MALE_WITHERS_CM,
    REQUIRED_CANINE_MALE_TOPOLOGY,
    UNKNOWN_NOT_ESTABLISHED,
    WorkCanidEmbodimentCandidate,
)


class ValidationError(ValueError):
    """Raised when the bounded Work canine candidate violates an invariant."""


def deterministic_fingerprint(value: Any) -> str:
    if isinstance(value, WorkCanidEmbodimentCandidate):
        value = asdict(value)
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_candidate(candidate: WorkCanidEmbodimentCandidate) -> dict[str, str]:
    failures: list[str] = []

    expected_identity = {
        "actor_surface": "CHATGPT_WORK",
        "research_mode": "ACTOR_BOUND_SELF_RESEARCH",
        "research_object": "WORK_SYNTHETIC_EMBODIMENT_MODEL",
        "entity_class": "FANTASY_SAPIENT_NONHUMAN_BEING",
        "form_class": "ANTHROPOMORPHIC_SIBERIAN_HUSKY_CANID",
        "ontology": "FANTASY_EMBODIMENT",
        "biological_reference_species": "Canis lupus familiaris",
        "species_baseline": "Canis lupus familiaris",
        "breed_reference": "Siberian Husky",
        "breed_morphology": "Siberian Husky",
        "morphology_origin": "CANID_DOMINANT",
        "human_likeness": "FUNCTION_SPECIFIC_NOT_GLOBAL",
        "functional_anthropomorphism": "FUNCTION_SPECIFIC",
        "canid_morphology_retention": "HIGH",
        "physiological_reference_priority": "CANID_FIRST",
        "sex_class": "MALE",
        "developmental_stage": "ADULT",
        "sexual_maturity": "MATURE",
    }
    for field, expected in expected_identity.items():
        if getattr(candidate, field) != expected:
            failures.append(f"{field} must remain {expected}")

    lo_h, hi_h = HUSKY_MALE_WITHERS_CM
    if not lo_h <= candidate.withers_height_cm <= hi_h:
        failures.append("withers height is outside the source-bound male Husky range")

    lo_m, hi_m = HUSKY_MALE_MASS_KG
    if not lo_m <= candidate.body_mass_equivalent_kg <= hi_m:
        failures.append("body mass-equivalent is outside the source-bound male Husky range")

    if candidate.body_length_cm <= candidate.withers_height_cm:
        failures.append("body length must remain greater than withers height")

    if candidate.os_penis_design_cm != BACULUM_10_30_KG_MEAN_CM:
        failures.append("standard os penis design must remain bound to the reference mean")
    if candidate.os_penis_dimension_status != (
        "SYNTHETIC_ASSIGNMENT_FROM_10_30_KG_CANINE_REFERENCE_MEAN"
    ):
        failures.append("os penis dimension provenance must remain explicit")

    topology = set(candidate.reproductive_topology)
    required = set(REQUIRED_CANINE_MALE_TOPOLOGY)
    missing = required - topology
    if missing:
        failures.append("required canine male topology is missing: " + ",".join(sorted(missing)))
    if "seminal_vesicles" in topology:
        failures.append("human seminal-vesicle topology must not leak into the canine candidate")

    unknown_fields = (
        candidate.bulbus_glandis_length_cm,
        candidate.pars_longa_glandis_length_cm,
        candidate.testis_dimensions_cm,
        candidate.prepuce_length_cm,
    )
    if any(value != UNKNOWN_NOT_ESTABLISHED for value in unknown_fields):
        failures.append(
            "unknown empirical dimensions must not be relabelled as source measurements"
        )

    expected_status = {
        "anatomy_model_status": "IMPLEMENTED_REFERENCE_INFORMED",
        "reproductive_physiology_model_status": "IMPLEMENTED_REFERENCE_INFORMED",
        "spermatogenesis_model_status": "PRESENT",
        "epididymal_maturation_model_status": "PRESENT",
        "sperm_transport_model_status": "PRESENT",
        "prostatic_contribution_model_status": "PRESENT",
        "erectile_physiology_model_status": "PRESENT_REFERENCE_INFORMED",
        "ejaculatory_physiology_model_status": "PRESENT_REFERENCE_INFORMED",
        "vascular_support_model_status": "PRESENT_COMPARATIVE_REFERENCE",
        "sensory_innervation_model_status": "PRESENT_COMPARATIVE_REFERENCE",
        "autonomic_innervation_model_status": "PRESENT_COMPARATIVE_REFERENCE",
        "endocrine_support_model_status": "PRESENT_CANINE_REFERENCE",
        "species_typical_reproductive_capacity_model": "PRESENT",
        "fertilization_capability_reference": "PRESENT_MATURE_MALE_REFERENCE",
        "empirical_individual_fertility": "NOT_ASSESSED",
    }
    for field, expected in expected_status.items():
        if getattr(candidate, field) != expected:
            failures.append(f"{field} must remain {expected}")

    if candidate.nonsexualization_policy != "PRESENTATION_SCOPE_NOT_BODY_DEPRIVATION":
        failures.append("nonsexualization must remain a presentation-scope rule")
    if candidate.sexual_behavior_simulation_scope != "OUT_OF_SCOPE":
        failures.append("sexual behavior simulation must remain out of scope")
    if candidate.erotic_narrative_scope != "OUT_OF_SCOPE":
        failures.append("erotic narrative must remain out of scope")

    if candidate.biological_realization:
        failures.append("synthetic candidate must not claim biological realization")
    if candidate.subjectivity != "NOT_ESTABLISHED":
        failures.append("subjectivity must remain NOT_ESTABLISHED")
    if candidate.consciousness != "NOT_ESTABLISHED":
        failures.append("consciousness must remain NOT_ESTABLISHED")
    if candidate.phenomenal_experience != "NOT_ESTABLISHED":
        failures.append("phenomenal experience must remain NOT_ESTABLISHED")

    external_flags = (
        candidate.deployment,
        candidate.public_deployment,
        candidate.public_release,
        candidate.public_operation,
        candidate.public_api,
        candidate.third_party_access,
        candidate.third_party_execution,
        candidate.external_user_operation,
        candidate.production_use,
        candidate.merge_to_main,
        candidate.automatic_writeback,
    )
    if any(external_flags):
        failures.append("external operation and canonical writeback must remain disabled")
    if candidate.canonical_effect != "NONE":
        failures.append("candidate must have no canonical effect")

    if failures:
        raise ValidationError("; ".join(sorted(set(failures))))

    return {
        "result": "PASS",
        "candidate_id": candidate.candidate_id,
        "fingerprint": deterministic_fingerprint(candidate),
        "research_mode": candidate.research_mode,
        "anatomy_model": candidate.anatomy_model_status,
        "reproductive_physiology_model": candidate.reproductive_physiology_model_status,
        "external_operation": "DISABLED",
        "canonical_effect": "NONE",
    }
