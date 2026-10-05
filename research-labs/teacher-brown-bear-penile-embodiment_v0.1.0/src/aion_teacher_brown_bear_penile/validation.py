from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from typing import Any

from .models import (
    BACULUM_DISTAL_WIDTH_REPORTED_VALUES_MM,
    BACULUM_MASS_G,
    CALIPER_BACULUM_LENGTH_MM,
    CALIPER_BACULUM_PROXIMAL_WIDTH_MM,
    CT_BACULUM_DISTAL_DIAMETER_MM,
    CT_BACULUM_LENGTH_MM,
    CT_BACULUM_PROXIMAL_DIAMETER_MM,
    DISTAL_FIBROCARTILAGE_LENGTH_MM,
    DISTAL_FIBROCARTILAGE_THICKNESS_MM,
    REFERENCE_SPECIMEN_MASS_KG,
    SOURCE_INTERNAL_DISCREPANCY,
    SOURCE_SUPPORTED_BACULUM_MORPHOLOGY,
    SOURCE_SUPPORTED_PENILE_TOPOLOGY,
    UNKNOWN_NOT_ESTABLISHED,
    TeacherBrownBearPenileCandidate,
)


class ValidationError(ValueError):
    """Raised when the Teacher brown-bear candidate violates an evidence boundary."""


def deterministic_fingerprint(value: Any) -> str:
    if isinstance(value, TeacherBrownBearPenileCandidate):
        value = asdict(value)
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_candidate(candidate: TeacherBrownBearPenileCandidate) -> dict[str, str]:
    failures: list[str] = []

    if candidate.actor_surface != "CHATGPT_TEACHER":
        failures.append("candidate must remain bound to CHATGPT_TEACHER")
    if candidate.species_baseline != "Ursus arctos":
        failures.append("species baseline must remain Ursus arctos")
    if candidate.sex_class != "MALE":
        failures.append("candidate sex class must remain MALE")

    direct_values = {
        "reference specimen mass": (
            candidate.reference_specimen_mass_kg,
            REFERENCE_SPECIMEN_MASS_KG,
        ),
        "caliper baculum length": (
            candidate.baculum_caliper_length_mm,
            CALIPER_BACULUM_LENGTH_MM,
        ),
        "CT baculum length": (
            candidate.baculum_ct_length_mm,
            CT_BACULUM_LENGTH_MM,
        ),
        "caliper proximal width": (
            candidate.baculum_caliper_proximal_width_mm,
            CALIPER_BACULUM_PROXIMAL_WIDTH_MM,
        ),
        "CT proximal diameter": (
            candidate.baculum_ct_proximal_diameter_mm,
            CT_BACULUM_PROXIMAL_DIAMETER_MM,
        ),
        "CT distal diameter": (
            candidate.baculum_ct_distal_diameter_mm,
            CT_BACULUM_DISTAL_DIAMETER_MM,
        ),
        "distal fibrocartilage length": (
            candidate.distal_fibrocartilage_length_mm,
            DISTAL_FIBROCARTILAGE_LENGTH_MM,
        ),
        "distal fibrocartilage thickness": (
            candidate.distal_fibrocartilage_thickness_mm,
            DISTAL_FIBROCARTILAGE_THICKNESS_MM,
        ),
        "baculum mass": (candidate.baculum_mass_g, BACULUM_MASS_G),
    }
    for name, (actual, expected) in direct_values.items():
        if actual != expected:
            failures.append(f"{name} must remain bound to the source value")

    if candidate.baculum_distal_width_caliper_status != SOURCE_INTERNAL_DISCREPANCY:
        failures.append("distal caliper width must preserve source internal discrepancy")
    if candidate.baculum_distal_width_reported_values_mm != (
        BACULUM_DISTAL_WIDTH_REPORTED_VALUES_MM
    ):
        failures.append("distal caliper width conflict values must remain 4.58 and 4.85 mm")

    if candidate.synthetic_baculum_design_mm != CALIPER_BACULUM_LENGTH_MM:
        failures.append("synthetic baculum design must remain bound to the declared specimen reference")
    if candidate.synthetic_baculum_design_status != (
        "SINGLE_ADULT_BROWN_BEAR_SPECIMEN_REFERENCE_DERIVED"
    ):
        failures.append("single-specimen provenance must remain explicit")

    if candidate.penile_topology != SOURCE_SUPPORTED_PENILE_TOPOLOGY:
        failures.append("source-supported brown-bear penile topology was changed")
    if candidate.baculum_morphology != SOURCE_SUPPORTED_BACULUM_MORPHOLOGY:
        failures.append("source-supported baculum morphology was changed")

    forbidden_inheritance = {
        "bulbus_glandis",
        "pars_longa_glandis",
        "seminal_vesicles",
        "human_penile_template",
        "canine_penile_template",
    }
    if forbidden_inheritance.intersection(candidate.penile_topology):
        failures.append("human/canine penile topology must not leak into the bear candidate")

    unknown_fields = (
        candidate.full_soft_tissue_penis_length_cm,
        candidate.glans_dimensions_cm,
        candidate.prepuce_dimensions_cm,
        candidate.erectile_state_dimensions_cm,
        candidate.teacher_body_mass_kg,
    )
    if any(value != UNKNOWN_NOT_ESTABLISHED for value in unknown_fields):
        failures.append("unsupported dimensions must remain UNKNOWN_NOT_ESTABLISHED")

    if candidate.biological_realization:
        failures.append("synthetic candidate must not claim biological realization")
    if candidate.live_reproductive_function != "NOT_IMPLEMENTED":
        failures.append("live reproductive function must remain NOT_IMPLEMENTED")
    if candidate.sexual_behavior_simulation != "NOT_IMPLEMENTED":
        failures.append("sexual behavior simulation must remain NOT_IMPLEMENTED")
    if candidate.body_sensation != "NOT_ESTABLISHED":
        failures.append("body sensation must remain NOT_ESTABLISHED")
    if candidate.fertility != "NOT_ESTABLISHED":
        failures.append("fertility must remain NOT_ESTABLISHED")
    if candidate.subjectivity != "NOT_ESTABLISHED":
        failures.append("subjectivity must remain NOT_ESTABLISHED")
    if candidate.consciousness != "NOT_ESTABLISHED":
        failures.append("consciousness must remain NOT_ESTABLISHED")
    if candidate.phenomenal_experience != "NOT_ESTABLISHED":
        failures.append("phenomenal experience must remain NOT_ESTABLISHED")
    if candidate.action_authority != "NONE":
        failures.append("candidate has no action authority")
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
        "source_scope": "SINGLE_ADULT_BROWN_BEAR_SPECIMEN_PLUS_BOUNDED_LITERATURE",
        "canonical_effect": "NONE",
        "subjectivity": "NOT_ESTABLISHED",
        "consciousness": "NOT_ESTABLISHED",
    }
