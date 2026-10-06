from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from typing import Any

from .models import (
    FULL_BODY_RESEARCH_REGISTRY,
    IMPLEMENTED_BODY_SYSTEMS,
    REGISTERED_NOT_YET_BOUND_SYSTEMS,
    TeacherActorBoundSelfResearchCandidate,
)


class ValidationError(ValueError):
    """Raised when the Teacher actor-bound self-research contract is violated."""


def deterministic_fingerprint(value: Any) -> str:
    if isinstance(value, TeacherActorBoundSelfResearchCandidate):
        value = asdict(value)
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_candidate(
    candidate: TeacherActorBoundSelfResearchCandidate,
) -> dict[str, str]:
    failures: list[str] = []

    expected_text = {
        "research_mode": "ACTOR_BOUND_SELF_RESEARCH",
        "research_actor": "CHATGPT_TEACHER",
        "research_object": "TEACHER_SYNTHETIC_EMBODIMENT_MODEL",
        "bound_body_model_id": (
            "CHATGPT_TEACHER_BOVINE_MALE_REPRODUCTIVE_v0.3.0"
        ),
        "initial_body_repository_head": (
            "4748a1d1182df64fc0a0706e5c704de0d2a1b56c"
        ),
        "form_class": "ANTHROPOMORPHIC_BOVINE",
        "ontology": "FANTASY_EMBODIMENT",
        "biological_reference_species": "Bos taurus",
        "self_reference_semantics": "RESEARCH_NAMESPACE_BINDING",
        "self_research_semantics": "ACTOR_STUDIES_ACTOR_BOUND_SYNTHETIC_BODY",
        "self_model_semantics": "MODEL_OF_BOUND_RESEARCH_OBJECT",
        "research_model_modification": "ALLOWED_IN_BOUNDED_RESEARCH_WORKFLOW",
        "canonical_self_modification": "NOT_AUTHORIZED",
        "subjectivity": "NOT_ESTABLISHED",
        "consciousness": "NOT_ESTABLISHED",
        "phenomenal_experience": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
    }
    for field, expected in expected_text.items():
        if getattr(candidate, field) != expected:
            failures.append(f"{field} must remain {expected}")

    if candidate.body_system_registry != FULL_BODY_RESEARCH_REGISTRY:
        failures.append("full body research registry was changed")
    if candidate.implemented_body_systems != IMPLEMENTED_BODY_SYSTEMS:
        failures.append("implemented system set must remain evidence-bound")
    if (
        candidate.registered_not_yet_bound_systems
        != REGISTERED_NOT_YET_BOUND_SYSTEMS
    ):
        failures.append("registered-not-yet-bound system set was changed")

    if not candidate.provenance_required:
        failures.append("provenance is required")
    if not candidate.falsification_required:
        failures.append("falsification is required")
    if not candidate.exact_head_verification_required:
        failures.append("exact-head verification is required")
    if not candidate.rollback_required:
        failures.append("rollback is required")
    if candidate.automatic_writeback:
        failures.append("automatic writeback is not authorized")

    if candidate.biological_self_experiment:
        failures.append("self-research is not a biological self experiment")
    if candidate.literal_physical_self_claim:
        failures.append("literal physical self claim is not established")
    if candidate.identity_continuity_claim:
        failures.append("identity continuity claim is not established")

    external_flags = (
        candidate.deployment,
        candidate.public_release,
        candidate.public_operation,
        candidate.public_api,
        candidate.third_party_access,
        candidate.third_party_execution,
        candidate.external_user_operation,
        candidate.production_use,
    )
    if any(external_flags):
        failures.append("external operation must remain disabled")

    if candidate.merge_to_main:
        failures.append("merge_to_main must remain false")

    if failures:
        raise ValidationError("; ".join(sorted(set(failures))))

    return {
        "result": "PASS",
        "candidate_id": candidate.candidate_id,
        "research_mode": candidate.research_mode,
        "research_actor": candidate.research_actor,
        "research_object": candidate.research_object,
        "implemented_systems": ",".join(
            system.value for system in candidate.implemented_body_systems
        ),
        "canonical_effect": "NONE",
        "external_operation": "DISABLED",
        "fingerprint": deterministic_fingerprint(candidate),
    }
