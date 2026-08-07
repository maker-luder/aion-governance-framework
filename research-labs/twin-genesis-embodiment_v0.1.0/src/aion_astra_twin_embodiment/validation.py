from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from typing import Any

from .models import EmbodimentInstance, EmbodimentTemplate, SharedGenesisEvent


class ValidationError(ValueError):
    """Raised when a candidate violates a governance invariant."""


def deterministic_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_candidate(
    event: SharedGenesisEvent,
    template: EmbodimentTemplate,
    aion: EmbodimentInstance,
    astra: EmbodimentInstance,
) -> dict[str, str]:
    failures: list[str] = []

    if event.aion_agent_id == event.astra_agent_id:
        failures.append("AION and Astra must have distinct agent_id values")
    if event.aion_instance_id == event.astra_instance_id:
        failures.append("AION and Astra must have distinct instance_id values")
    if aion.embodiment_id == astra.embodiment_id:
        failures.append("AION and Astra must have distinct embodiment_id values")
    if aion.memory_namespace == astra.memory_namespace:
        failures.append("AION and Astra must have distinct private memory namespaces")
    if aion.canonical_state_reference == astra.canonical_state_reference:
        failures.append("AION and Astra must have distinct canonical state references")
    if not template.adult_status:
        failures.append("Only adult embodiment candidates are permitted")
    if aion.template_id != template.template_id or astra.template_id != template.template_id:
        failures.append("Both candidates must reference the shared template")
    if aion.agent_id != event.aion_agent_id or astra.agent_id != event.astra_agent_id:
        failures.append("Embodiment-to-agent binding does not match the genesis event")
    if aion.instance_id != event.aion_instance_id or astra.instance_id != event.astra_instance_id:
        failures.append("Embodiment-to-instance binding does not match the genesis event")
    if template.sexual_function_status != "NOT_IMPLEMENTED":
        failures.append("Sexual function is outside this candidate scope")
    if template.gender_identity_effect != "NONE":
        failures.append("Anatomy must not assign gender identity")
    if template.subjectivity_effect != "NONE":
        failures.append("Anatomy must not alter subjectivity conclusions")
    for instance in (aion, astra):
        if instance.runtime_binding != "NOT_IMPLEMENTED":
            failures.append("Live embodiment runtime is not authorized")
        if instance.body_sensation != "NOT_ESTABLISHED":
            failures.append("Body sensation must remain NOT_ESTABLISHED")
        if instance.sexual_interaction != "NOT_AUTHORIZED":
            failures.append("Sexual interaction is not authorized")
        forbidden = {"relationship", "trust", "familiarity", "intimacy"}
        if forbidden.intersection(set(instance.modification_authorities)):
            failures.append("Relationship or trust cannot grant modification authority")
        if instance.canonical_effect != "NONE":
            failures.append("Candidate embodiment must have no canonical effect")

    if event.canonical_effect != "NONE":
        failures.append("Shared genesis candidate must have no canonical effect")

    if failures:
        raise ValidationError("; ".join(sorted(set(failures))))

    return {
        "result": "PASS",
        "event_hash": deterministic_hash(asdict(event)),
        "template_hash": deterministic_hash(asdict(template)),
        "aion_hash": deterministic_hash(asdict(aion)),
        "astra_hash": deterministic_hash(asdict(astra)),
        "canonical_effect": "NONE",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
    }
