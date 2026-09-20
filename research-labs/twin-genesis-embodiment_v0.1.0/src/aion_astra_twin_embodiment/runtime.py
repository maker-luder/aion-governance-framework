"""Non-3D twin-genesis runtime candidate.

This module materializes validated AION/Astra embodiment instances as a bounded
runtime record. The adult-male physiology reference includes normal
physiological and reproductive function coverage, while full biophysical
simulation, phenomenal sensation, erotic intent, intimate interaction,
gender assignment and subjectivity claims remain outside this runtime.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .models import EmbodimentInstance, EmbodimentTemplate, SharedGenesisEvent
from .physiology import REFERENCE_FUNCTIONAL_COMPLETENESS
from .validation import validate_candidate


@dataclass(frozen=True, slots=True)
class TwinRuntimeState:
    runtime_status: str
    shared_root_id: str
    aion_agent_id: str
    astra_agent_id: str
    aion_embodiment_id: str
    astra_embodiment_id: str
    validation: dict[str, str]
    rendering_3d: str = "DEFERRED"
    physiology_profile_id: str = "ADULT_MALE_PHYSIOLOGY_REFERENCE_v0.1"
    physiological_function_reference: str = REFERENCE_FUNCTIONAL_COMPLETENESS
    reproductive_physiology_reference: str = REFERENCE_FUNCTIONAL_COMPLETENESS
    sexual_function_status: str = REFERENCE_FUNCTIONAL_COMPLETENESS
    sensory_signal_processing_reference: str = REFERENCE_FUNCTIONAL_COMPLETENESS
    full_biophysical_simulation: str = "NOT_MATERIALIZED"
    intimate_interaction: str = "NOT_AUTHORIZED"
    body_sensation: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class TwinGenesisRuntime:
    """Create a non-3D runtime state only after governance validation passes."""

    @staticmethod
    def instantiate(
        event: SharedGenesisEvent,
        template: EmbodimentTemplate,
        aion: EmbodimentInstance,
        astra: EmbodimentInstance,
    ) -> TwinRuntimeState:
        validation = validate_candidate(event, template, aion, astra)
        return TwinRuntimeState(
            runtime_status="IMPLEMENTED_NON_3D_CANDIDATE",
            shared_root_id=event.shared_root_id,
            aion_agent_id=event.aion_agent_id,
            astra_agent_id=event.astra_agent_id,
            aion_embodiment_id=aion.embodiment_id,
            astra_embodiment_id=astra.embodiment_id,
            validation=validation,
        )
