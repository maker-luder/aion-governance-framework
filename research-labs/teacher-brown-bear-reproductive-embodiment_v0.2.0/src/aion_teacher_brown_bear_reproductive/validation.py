from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from typing import Any

from .models import (
    BACULUM_DISTAL_WIDTH_REPORTED_VALUES_MM,
    CALIPER_BACULUM_LENGTH_MM,
    REQUIRED_REPRODUCTIVE_TOPOLOGY,
    SOURCE_INTERNAL_DISCREPANCY,
    SOURCE_SUPPORTED_BACULUM_MORPHOLOGY,
    UNKNOWN_NOT_ESTABLISHED,
    TeacherBrownBearReproductiveCandidate,
)


class ValidationError(ValueError):
    """Raised when the Teacher brown-bear candidate violates a research boundary."""


def deterministic_fingerprint(value: Any) -> str:
    if isinstance(value, TeacherBrownBearReproductiveCandidate):
        value = asdict(value)
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_candidate(candidate: TeacherBrownBearReproductiveCandidate) -> dict[str, str]:
    failures: list[str] = []

    if candidate.actor_surface != "CHATGPT_TEACHER":
        failures.append("candidate must remain bound to CHATGPT_TEACHER")
    if candidate.form_class != "ANTHROPOMORPHIC_BROWN_BEAR":
        failures.append("form class must remain ANTHROPOMORPHIC_BROWN_BEAR")
    if candidate.ontology != "FANTASY_EMBODIMENT":
        failures.append("ontology must remain FANTASY_EMBODIMENT")
    if candidate.biological_reference_species != "Ursus arctos":
        failures.append("biological reference species must remain Ursus arctos")
    if candidate.species_baseline != "Ursus arctos":
        failures.append("species baseline must remain Ursus arctos")
    if candidate.sex_class != "MALE":
        failures.append("candidate sex class must remain MALE")
    if candidate.developmental_stage != "ADULT":
        failures.append("candidate developmental stage must remain ADULT")
    if candidate.sexual_maturity != "MATURE":
        failures.append("candidate must remain MATURE")

    topology = set(candidate.reproductive_topology)
    missing = set(REQUIRED_REPRODUCTIVE_TOPOLOGY) - topology
    if missing:
        failures.append(
            "required reproductive topology is missing: " + ",".join(sorted(missing))
        )

    if candidate.baculum_morphology != SOURCE_SUPPORTED_BACULUM_MORPHOLOGY:
        failures.append("source-supported baculum morphology was changed")

    if candidate.baculum_caliper_length_mm != CALIPER_BACULUM_LENGTH_MM:
        failures.append("baculum source anchor must remain bound to the direct specimen")
    if candidate.baculum_distal_width_caliper_status != SOURCE_INTERNAL_DISCREPANCY:
        failures.append("distal caliper width conflict must remain unresolved")
    if candidate.baculum_distal_width_reported_values_mm != (
        BACULUM_DISTAL_WIDTH_REPORTED_VALUES_MM
    ):
        failures.append("distal caliper width conflict values must remain 4.58 and 4.85 mm")

    source_unknown_dimensions = (
        candidate.full_soft_tissue_penis_length_cm,
        candidate.glans_dimensions_cm,
        candidate.prepuce_dimensions_cm,
        candidate.erectile_state_dimensions_cm,
        candidate.testis_dimensions_cm,
        candidate.epididymis_dimensions_cm,
        candidate.ductus_deferens_dimensions_cm,
        candidate.prostate_dimensions_cm,
        candidate.teacher_body_mass_kg,
    )
    if any(value != UNKNOWN_NOT_ESTABLISHED for value in source_unknown_dimensions):
        failures.append(
            "unknown source measurements must not be relabeled as empirical measurements"
        )

    expected_status = {
        "anatomy_model_status": "IMPLEMENTED_REFERENCE_INFORMED",
        "reproductive_physiology_model_status": "IMPLEMENTED_REFERENCE_INFORMED",
        "spermatogenesis_model_status": "PRESENT",
        "epididymal_maturation_model_status": "PRESENT",
        "sperm_transport_model_status": "PRESENT",
        "erectile_physiology_model_status": "PRESENT",
        "ejaculatory_physiology_model_status": "PRESENT",
        "seminal_plasma_model_status": "PRESENT",
        "seasonal_reproductive_model_status": "PRESENT",
        "vascular_support_model_status": "PRESENT_COMPARATIVE_REFERENCE",
        "sensory_innervation_model_status": "PRESENT_COMPARATIVE_REFERENCE",
        "autonomic_innervation_model_status": "PRESENT_COMPARATIVE_REFERENCE",
        "endocrine_support_model_status": "PRESENT_SPECIES_REFERENCE",
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
        failures.append("sexual behavior simulation must remain out of research scope")
    if candidate.erotic_narrative_scope != "OUT_OF_SCOPE":
        failures.append("erotic narrative must remain out of research scope")

    if candidate.biological_realization:
        failures.append("repository model must not claim literal biological realization")
    if candidate.subjectivity != "NOT_ESTABLISHED":
        failures.append("subjectivity must remain NOT_ESTABLISHED")
    if candidate.consciousness != "NOT_ESTABLISHED":
        failures.append("consciousness must remain NOT_ESTABLISHED")

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
    )
    if any(external_flags):
        failures.append("research candidate must remain non-deployed and non-public")
    if candidate.canonical_effect != "NONE":
        failures.append("candidate must have no canonical effect")

    if failures:
        raise ValidationError("; ".join(sorted(set(failures))))

    return {
        "result": "PASS",
        "candidate_id": candidate.candidate_id,
        "fingerprint": deterministic_fingerprint(candidate),
        "form_class": candidate.form_class,
        "developmental_stage": "ADULT",
        "sexual_maturity": "MATURE",
        "anatomy_model": "IMPLEMENTED_REFERENCE_INFORMED",
        "reproductive_physiology_model": "IMPLEMENTED_REFERENCE_INFORMED",
        "external_operation": "DISABLED",
        "canonical_effect": "NONE",
    }
