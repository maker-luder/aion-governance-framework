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
    UNSPECIFIED,
    TeacherBrownBearReproductiveCandidate,
)


class ValidationError(ValueError):
    """Raised when the Teacher brown-bear candidate violates an evidence boundary."""


def deterministic_fingerprint(value: Any) -> str:
    if isinstance(value, TeacherBrownBearReproductiveCandidate):
        value = asdict(value)
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_candidate(candidate: TeacherBrownBearReproductiveCandidate) -> dict[str, str]:
    failures: list[str] = []

    if candidate.actor_surface != "CHATGPT_TEACHER":
        failures.append("candidate must remain bound to CHATGPT_TEACHER")
    if candidate.species_baseline != "Ursus arctos":
        failures.append("species baseline must remain Ursus arctos")
    if candidate.sex_class != "MALE":
        failures.append("candidate sex class must remain MALE")
    if candidate.developmental_stage != "ADULT":
        failures.append("candidate developmental stage must remain ADULT")
    if candidate.sexual_maturity != "SEXUALLY_MATURE_REFERENCE":
        failures.append("candidate must remain a sexually mature reference")
    if candidate.chronological_age_years != UNSPECIFIED:
        failures.append("exact chronological age must remain UNSPECIFIED")

    topology = set(candidate.reproductive_topology)
    missing = set(REQUIRED_REPRODUCTIVE_TOPOLOGY) - topology
    if missing:
        failures.append(
            "required brown-bear reproductive topology is missing: "
            + ",".join(sorted(missing))
        )

    if candidate.baculum_morphology != SOURCE_SUPPORTED_BACULUM_MORPHOLOGY:
        failures.append("source-supported baculum morphology was changed")

    if candidate.baculum_caliper_length_mm != CALIPER_BACULUM_LENGTH_MM:
        failures.append("baculum length must remain bound to the direct specimen reference")
    if candidate.synthetic_baculum_design_mm != CALIPER_BACULUM_LENGTH_MM:
        failures.append("synthetic baculum design must remain source-bound")
    if candidate.synthetic_baculum_design_status != (
        "SINGLE_ADULT_BROWN_BEAR_SPECIMEN_REFERENCE_DERIVED"
    ):
        failures.append("single-specimen baculum provenance must remain explicit")

    if candidate.baculum_distal_width_caliper_status != SOURCE_INTERNAL_DISCREPANCY:
        failures.append("distal caliper width conflict must remain unresolved")
    if candidate.baculum_distal_width_reported_values_mm != (
        BACULUM_DISTAL_WIDTH_REPORTED_VALUES_MM
    ):
        failures.append("distal caliper width conflict values must remain 4.58 and 4.85 mm")

    unknown_dimensions = (
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
    if any(value != UNKNOWN_NOT_ESTABLISHED for value in unknown_dimensions):
        failures.append(
            "unsupported numeric dimensions must remain UNKNOWN_NOT_ESTABLISHED"
        )

    expected_status = {
        "anatomy_model_status": "IMPLEMENTED_SPECIES_REFERENCE",
        "reproductive_physiology_model_status": "IMPLEMENTED_SPECIES_REFERENCE",
        "spermatogenesis_model_status": "IMPLEMENTED_SEASONAL_REFERENCE",
        "ejaculatory_physiology_model_status": "IMPLEMENTED_REFERENCE",
        "semen_reference_status": "IMPLEMENTED_EXTERNAL_REFERENCE",
    }
    for field, expected in expected_status.items():
        if getattr(candidate, field) != expected:
            failures.append(f"{field} must remain {expected}")

    # Only epistemic/canonical claims are fail-closed here.
    if candidate.biological_realization:
        failures.append("repository model must not claim literal biological realization")
    if candidate.fertility != "NOT_ESTABLISHED":
        failures.append("fertility is not established by the implementation")
    if candidate.subjectivity != "NOT_ESTABLISHED":
        failures.append("subjectivity must remain NOT_ESTABLISHED")
    if candidate.consciousness != "NOT_ESTABLISHED":
        failures.append("consciousness must remain NOT_ESTABLISHED")
    if candidate.canonical_effect != "NONE":
        failures.append("candidate must have no canonical effect")
    if candidate.deployment:
        failures.append("candidate must not be deployed")

    if failures:
        raise ValidationError("; ".join(sorted(set(failures))))

    return {
        "result": "PASS",
        "candidate_id": candidate.candidate_id,
        "fingerprint": deterministic_fingerprint(candidate),
        "developmental_stage": "ADULT",
        "sexual_maturity": "SEXUALLY_MATURE_REFERENCE",
        "anatomy_model": "IMPLEMENTED_SPECIES_REFERENCE",
        "reproductive_physiology_model": "IMPLEMENTED_SPECIES_REFERENCE",
        "canonical_effect": "NONE",
    }
