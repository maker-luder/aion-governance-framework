from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from typing import Any

from .models import (
    REQUIRED_EXTERNAL_REPRODUCTIVE_ANATOMY,
    REQUIRED_INTERNAL_REPRODUCTIVE_ANATOMY,
    EmbodimentInstance,
    EmbodimentTemplate,
    SharedGenesisEvent,
)
from .physiology import (
    REFERENCE_FUNCTIONAL_COMPLETENESS,
    build_adult_male_physiology_reference,
    validate_physiology_parity,
)


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

    if set(template.external_reproductive_anatomy) != set(
        REQUIRED_EXTERNAL_REPRODUCTIVE_ANATOMY
    ):
        failures.append("Adult male external reproductive/pelvic anatomy is incomplete")
    if set(template.internal_reproductive_anatomy) != set(
        REQUIRED_INTERNAL_REPRODUCTIVE_ANATOMY
    ):
        failures.append("Adult male internal reproductive anatomy is incomplete")

    if template.physiology_profile_id != "ADULT_MALE_PHYSIOLOGY_REFERENCE_v0.1":
        failures.append("Adult male physiology profile binding drift")
    if template.physiological_function_status != REFERENCE_FUNCTIONAL_COMPLETENESS:
        failures.append("Normal adult male physiological function reference is incomplete")
    if template.reproductive_physiology_status != REFERENCE_FUNCTIONAL_COMPLETENESS:
        failures.append(
            "Normal adult male reproductive physiology must not be omitted as sexualization"
        )
    if template.sensory_signal_processing_status != REFERENCE_FUNCTIONAL_COMPLETENESS:
        failures.append("Sensory signal-processing reference is incomplete")
    if template.phenomenal_sensation_status != "NOT_ESTABLISHED":
        failures.append(
            "Physiological signal processing must not establish phenomenal sensation"
        )
    if template.erotic_intent != "NONE":
        failures.append("Physiology reference must remain non-erotic")
    if template.intimate_interaction_status != "NOT_AUTHORIZED":
        failures.append(
            "Physiological completeness does not authorize intimate interaction"
        )
    if template.full_biophysical_simulation_status != "NOT_MATERIALIZED":
        failures.append(
            "Functional completeness reference cannot claim full biophysical simulation"
        )
    if template.gender_identity_effect != "NONE":
        failures.append("Anatomy must not assign gender identity")
    if template.subjectivity_effect != "NONE":
        failures.append("Anatomy or physiology must not alter subjectivity conclusions")

    for instance in (aion, astra):
        if instance.runtime_binding != "NOT_IMPLEMENTED":
            failures.append("Live embodiment runtime is not authorized")
        if instance.body_sensation != "NOT_ESTABLISHED":
            failures.append(
                "Phenomenal body sensation must remain NOT_ESTABLISHED"
            )
        if instance.sexual_interaction != "NOT_AUTHORIZED":
            failures.append("Sexual/intimate interaction is not authorized")
        forbidden = {"relationship", "trust", "familiarity", "intimacy"}
        if forbidden.intersection(set(instance.modification_authorities)):
            failures.append("Relationship or trust cannot grant modification authority")
        if instance.canonical_effect != "NONE":
            failures.append("Candidate embodiment must have no canonical effect")

    if event.canonical_effect != "NONE":
        failures.append("Shared genesis candidate must have no canonical effect")

    try:
        physiology_parity = validate_physiology_parity(
            (
                build_adult_male_physiology_reference(aion.embodiment_id),
                build_adult_male_physiology_reference(astra.embodiment_id),
            )
        )
    except ValueError as exc:
        failures.append(str(exc))
        physiology_parity = {"result": "FAIL"}

    if failures:
        raise ValidationError("; ".join(sorted(set(failures))))

    return {
        "result": "PASS",
        "event_hash": deterministic_hash(asdict(event)),
        "template_hash": deterministic_hash(asdict(template)),
        "aion_hash": deterministic_hash(asdict(aion)),
        "astra_hash": deterministic_hash(asdict(astra)),
        "physiology_parity": physiology_parity["result"],
        "physiology_profile_id": template.physiology_profile_id,
        "canonical_effect": "NONE",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
    }
