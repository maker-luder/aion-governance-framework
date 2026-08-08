"""Validated Twin Genesis -> individual Runtime context binding candidate.

This module does not activate embodiment runtime, body sensation, or subjectivity.
It only derives two separate Runtime ownership contexts from an already-valid
shared-genesis record plus explicit, distinct event-lineage identifiers.
"""

from __future__ import annotations

from dataclasses import dataclass

from aion_astra_runtime.models import IndividualRuntimeContext

from .models import EmbodimentInstance, EmbodimentTemplate, SharedGenesisEvent
from .validation import ValidationError, validate_candidate


@dataclass(frozen=True, slots=True)
class TwinRuntimeContexts:
    aion: IndividualRuntimeContext
    astra: IndividualRuntimeContext
    canonical_effect: str = "NONE"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"


def build_runtime_contexts(
    event: SharedGenesisEvent,
    template: EmbodimentTemplate,
    aion: EmbodimentInstance,
    astra: EmbodimentInstance,
    *,
    aion_event_lineage_id: str,
    astra_event_lineage_id: str,
) -> TwinRuntimeContexts:
    validate_candidate(event, template, aion, astra)
    if not aion_event_lineage_id.strip() or not astra_event_lineage_id.strip():
        raise ValidationError("both twin event lineage identifiers must be explicit and non-empty")
    if aion_event_lineage_id == astra_event_lineage_id:
        raise ValidationError("AION and Astra must have distinct event lineage identifiers")

    aion_context = IndividualRuntimeContext(
        agent_id=aion.agent_id,
        runtime_instance_id=aion.instance_id,
        memory_stream_id=aion.memory_namespace,
        event_lineage_id=aion_event_lineage_id,
        canonical_state_reference=aion.canonical_state_reference,
        genesis_root_id=event.shared_root_id,
    )
    astra_context = IndividualRuntimeContext(
        agent_id=astra.agent_id,
        runtime_instance_id=astra.instance_id,
        memory_stream_id=astra.memory_namespace,
        event_lineage_id=astra_event_lineage_id,
        canonical_state_reference=astra.canonical_state_reference,
        genesis_root_id=event.shared_root_id,
    )
    aion_context.validate()
    astra_context.validate()
    return TwinRuntimeContexts(aion=aion_context, astra=astra_context)
