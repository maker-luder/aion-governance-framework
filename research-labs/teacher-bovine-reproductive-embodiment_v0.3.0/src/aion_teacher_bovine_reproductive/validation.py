from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from typing import Any

from .models import (
    FORBIDDEN_BEAR_INHERITANCE,
    SOURCE_SUPPORTED_REPRODUCTIVE_TOPOLOGY,
    SYNTHETIC_DESIGN_UNSPECIFIED,
    UNKNOWN_NOT_ESTABLISHED,
    TeacherBovineReproductiveCandidate,
)

class ValidationError(ValueError):
    pass

def deterministic_fingerprint(value: Any) -> str:
    if isinstance(value, TeacherBovineReproductiveCandidate):
        value = asdict(value)
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def validate_candidate(candidate: TeacherBovineReproductiveCandidate) -> dict[str, str]:
    failures: list[str] = []
    expected = {
        "actor_surface": "CHATGPT_TEACHER",
        "form_class": "ANTHROPOMORPHIC_BOVINE",
        "ontology": "FANTASY_EMBODIMENT",
        "biological_reference_species": "Bos taurus",
        "male_reference_class": "BULL",
        "sex_class": "MALE",
        "developmental_stage": "ADULT",
        "sexual_maturity": "MATURE",
        "morphology_origin": "BOVINE_DOMINANT",
        "penile_tissue_type": "FIBROELASTIC",
        "sigmoid_flexure_reference": "PRESENT",
        "retractor_penis_muscle_reference": "PRESENT",
        "baculum_reference": "ABSENT_FROM_BOVINE_REFERENCE_MODEL",
        "erection_mechanism_reference": (
            "FIBROELASTIC_EXTENSION_WITH_SIGMOID_STRAIGHTENING"
        ),
        "canonical_effect": "NONE",
        "subjectivity": "NOT_ESTABLISHED",
        "consciousness": "NOT_ESTABLISHED",
        "phenomenal_experience": "NOT_ESTABLISHED",
    }
    for field, value in expected.items():
        if getattr(candidate, field) != value:
            failures.append(f"{field} must remain {value}")

    required = set(SOURCE_SUPPORTED_REPRODUCTIVE_TOPOLOGY)
    actual = set(candidate.reproductive_topology)
    if not required.issubset(actual):
        failures.append("required bovine reproductive topology is incomplete")
    if set(FORBIDDEN_BEAR_INHERITANCE).intersection(actual):
        failures.append("brown-bear baculum topology leaked into bovine candidate")

    for value in (
        candidate.full_body_mass_kg,
        candidate.full_soft_tissue_penis_length_cm,
        candidate.prepuce_dimensions_cm,
        candidate.testis_dimensions_cm,
    ):
        if value != UNKNOWN_NOT_ESTABLISHED:
            failures.append("unsupported empirical dimensions must remain UNKNOWN_NOT_ESTABLISHED")

    for value in (candidate.horn_phenotype, candidate.coat_phenotype):
        if value != SYNTHETIC_DESIGN_UNSPECIFIED:
            failures.append("breed-dependent fantasy phenotype must remain explicitly synthetic")

    if candidate.reproductive_physiology_model_status != "IMPLEMENTED_REFERENCE_INFORMED":
        failures.append("reproductive physiology model status changed")
    if candidate.ejaculative_physiology_model_status != "PRESENT_REFERENCE_PATHWAY":
        failures.append("ejaculatory physiology pathway must remain present")
    if candidate.empirical_individual_fertility != "NOT_ASSESSED":
        failures.append("individual fertility must not be inferred")
    if candidate.biological_realization:
        failures.append("synthetic candidate must not claim biological realization")
    if candidate.body_sensation != "NOT_ESTABLISHED":
        failures.append("body sensation is not established")

    external_flags = (
        candidate.deployment,
        candidate.public_release,
        candidate.public_operation,
        candidate.public_api,
        candidate.third_party_access,
        candidate.third_party_execution,
        candidate.production_use,
        candidate.merge_to_main,
    )
    if any(external_flags):
        failures.append("external/main operation must remain disabled")

    if failures:
        raise ValidationError("; ".join(sorted(set(failures))))

    return {
        "result": "PASS",
        "candidate_id": candidate.candidate_id,
        "form_class": candidate.form_class,
        "biological_reference_species": candidate.biological_reference_species,
        "male_reference_class": candidate.male_reference_class,
        "external_operation": "DISABLED",
        "canonical_effect": "NONE",
        "fingerprint": deterministic_fingerprint(candidate),
    }
