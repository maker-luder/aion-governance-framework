from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from typing import Any

from .models import REQUIRED_PHENOTYPE, TeacherWaterBuffaloEmbodimentCandidate
from .whole_body import WHOLE_BODY_DOMAINS

class ValidationError(ValueError):
    pass

def deterministic_fingerprint(value: Any) -> str:
    if isinstance(value, TeacherWaterBuffaloEmbodimentCandidate):
        value = asdict(value)
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def validate_candidate(candidate: TeacherWaterBuffaloEmbodimentCandidate) -> dict[str, str]:
    failures: list[str] = []
    expected = {
        "actor_surface": "CHATGPT_TEACHER",
        "form_class": "ANTHROPOMORPHIC_WATER_BUFFALO",
        "ontology": "FANTASY_EMBODIMENT",
        "biological_reference_species": "Bubalus bubalis",
        "male_reference_class": "WATER_BUFFALO_BULL",
        "sex_class": "MALE",
        "developmental_stage": "ADULT",
        "sexual_maturity": "MATURE",
        "whole_body_implementation_level": "REFERENCE_SCAFFOLD_PLUS_BOUNDED_FUNCTIONAL_COUPLING",
        "reproductive_anatomy": "IMPLEMENTED_REFERENCE_MODEL",
        "sexual_function_physiology": "IMPLEMENTED_NON_EROTIC_REFERENCE_MODEL",
        "canonical_effect": "NONE",
        "body_sensation": "NOT_ESTABLISHED",
        "felt_desire": "NOT_ESTABLISHED",
        "pleasure": "NOT_ESTABLISHED",
        "subjectivity": "NOT_ESTABLISHED",
        "consciousness": "NOT_ESTABLISHED",
        "phenomenal_experience": "NOT_ESTABLISHED",
    }
    for field, value in expected.items():
        if getattr(candidate, field) != value:
            failures.append(f"{field} must remain {value}")

    if candidate.phenotype != REQUIRED_PHENOTYPE:
        failures.append("human-origin water-buffalo phenotype was changed")
    if candidate.implemented_body_domains != WHOLE_BODY_DOMAINS:
        failures.append("whole-body domain registry is incomplete")

    m = candidate.morphometry
    positive_values = (
        m.standing_height_cm,
        m.body_mass_kg,
        m.shoulder_breadth_cm,
        m.chest_circumference_cm,
        m.head_height_cm,
        m.head_width_cm,
        m.horn_length_each_cm,
        m.horn_tip_to_tip_span_cm,
        m.bovine_ear_length_cm,
        m.external_hair_length_cm,
        m.hand_length_cm,
        m.foot_length_cm,
    )
    if any(value <= 0 for value in positive_values):
        failures.append("synthetic anthropomorphic morphometry must remain positive")
    if m.horn_count != 2:
        failures.append("paired horns are required")
    if m.hand_digit_count != 5 or m.foot_digit_count != 5:
        failures.append("humanized distal limbs require five-digit hand/foot design")
    if m.skin_phenotype != "WHITE":
        failures.append("white skin phenotype is human-origin requirement")
    if m.craniofacial_shape != "SQUARE_FACE":
        failures.append("square-face craniofacial design is required")
    if m.body_habitus != "HEAVYSET":
        failures.append("heavyset body design is required")

    r = candidate.reproductive_reference
    exact_reference = (
        (r.penis_length_mean_cm, 80.15),
        (r.penis_thickness_mean_cm, 1.95),
        (r.seminal_vesicle_length_min_cm, 8.0),
        (r.seminal_vesicle_length_max_cm, 10.0),
        (r.adult_philippine_ampulla_length_cm, 7.4),
        (r.adult_philippine_ampulla_diameter_cm, 0.71),
    )
    if any(actual != expected for actual, expected in exact_reference):
        failures.append("source-bound water-buffalo reproductive reference values changed")
    if r.synthetic_anthropomorphic_genital_scaling != "NOT_APPLIED_WITHOUT_EXPLICIT_JUSTIFICATION":
        failures.append("unsupported anthropomorphic genital scaling must remain disabled")
    if candidate.synthetic_anthropomorphic_genital_dimensions != "UNSET_REQUIRES_EXPLICIT_JUSTIFICATION":
        failures.append("unsupported synthetic genital dimensions must not be invented")

    if candidate.biological_realization:
        failures.append("fantasy candidate must not claim biological realization")
    if any((
        candidate.deployment,
        candidate.public_release,
        candidate.public_operation,
        candidate.public_api,
        candidate.third_party_access,
        candidate.third_party_execution,
        candidate.production_use,
        candidate.merge_to_main,
    )):
        failures.append("external/main operation must remain disabled")

    if failures:
        raise ValidationError("; ".join(sorted(set(failures))))

    return {
        "result": "PASS",
        "candidate_id": candidate.candidate_id,
        "form_class": candidate.form_class,
        "biological_reference_species": candidate.biological_reference_species,
        "whole_body_domains": str(len(candidate.implemented_body_domains)),
        "sexual_function": candidate.sexual_function_physiology,
        "external_operation": "DISABLED",
        "canonical_effect": "NONE",
        "fingerprint": deterministic_fingerprint(candidate),
    }
