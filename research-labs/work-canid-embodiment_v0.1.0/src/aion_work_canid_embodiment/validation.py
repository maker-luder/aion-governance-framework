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

    if candidate.actor_surface != "CHATGPT_WORK":
        failures.append("candidate must remain bound to CHATGPT_WORK")
    if candidate.species_baseline != "Canis lupus familiaris":
        failures.append("species baseline must remain domestic dog")
    if candidate.breed_morphology != "Siberian Husky":
        failures.append("breed morphology must remain Siberian Husky")
    if candidate.sex_class != "MALE":
        failures.append("v0.1 candidate sex class must remain MALE")

    lo_h, hi_h = HUSKY_MALE_WITHERS_CM
    if not lo_h <= candidate.withers_height_cm <= hi_h:
        failures.append("withers height is outside the source-bound male Husky range")

    lo_m, hi_m = HUSKY_MALE_MASS_KG
    if not lo_m <= candidate.body_mass_equivalent_kg <= hi_m:
        failures.append("body mass-equivalent is outside the source-bound male Husky range")

    if candidate.body_length_cm <= candidate.withers_height_cm:
        failures.append("body length must remain slightly greater than withers height")

    if candidate.os_penis_design_cm != BACULUM_10_30_KG_MEAN_CM:
        failures.append("os penis v0.1 design must remain bound to the declared reference mean")
    if candidate.os_penis_dimension_status != (
        "SYNTHETIC_ASSIGNMENT_FROM_10_30_KG_CANINE_REFERENCE_MEAN"
    ):
        failures.append("os penis dimension provenance must remain explicit")

    topology = set(candidate.reproductive_topology)
    required = set(REQUIRED_CANINE_MALE_TOPOLOGY)
    if topology != required:
        failures.append("canine male reproductive topology is incomplete or contains extra nodes")
    if "seminal_vesicles" in topology:
        failures.append("human seminal-vesicle topology must not leak into the canine candidate")

    unknown_fields = (
        candidate.bulbus_glandis_length_cm,
        candidate.pars_longa_glandis_length_cm,
        candidate.testis_dimensions_cm,
        candidate.prepuce_length_cm,
    )
    if any(value != UNKNOWN_NOT_ESTABLISHED for value in unknown_fields):
        failures.append("unsupported absolute dimensions must remain UNKNOWN_NOT_ESTABLISHED")

    if candidate.ejaculatory_reference_model_status != "IMPLEMENTED_SYNTHETIC_REFERENCE_ONLY":
        failures.append("ejaculatory model must remain a synthetic reference only")
    if candidate.live_ejaculatory_function != "NOT_IMPLEMENTED":
        failures.append("live ejaculatory function must remain NOT_IMPLEMENTED")

    if candidate.biological_realization:
        failures.append("synthetic candidate must not claim biological realization")
    if candidate.functional_reproductive_state != "NOT_IMPLEMENTED":
        failures.append("functional reproductive state is outside v0.1")
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
    if candidate.sexual_interaction != "NOT_AUTHORIZED":
        failures.append("sexual interaction is not authorized")
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
        "canonical_effect": "NONE",
        "subjectivity": "NOT_ESTABLISHED",
        "consciousness": "NOT_ESTABLISHED",
    }
