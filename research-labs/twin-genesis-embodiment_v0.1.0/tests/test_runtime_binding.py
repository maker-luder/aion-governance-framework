from __future__ import annotations

import pytest

from aion_astra_twin_embodiment import (
    EmbodimentInstance,
    EmbodimentTemplate,
    SharedGenesisEvent,
    ValidationError,
    build_runtime_contexts,
)


def objects():
    event = SharedGenesisEvent(
        genesis_event_id="GEN-1",
        shared_root_id="ROOT-1",
        aion_agent_id="AION",
        astra_agent_id="ASTRA",
        aion_instance_id="AION-I1",
        astra_instance_id="ASTRA-I1",
        source_artifact_hash="sha256:test",
    )
    template = EmbodimentTemplate(template_id="adult-template", template_version="0.1.0")
    aion = EmbodimentInstance(
        embodiment_id="BODY-AION",
        agent_id="AION",
        instance_id="AION-I1",
        template_id="adult-template",
        memory_namespace="aion-private",
        canonical_state_reference="aion-state",
    )
    astra = EmbodimentInstance(
        embodiment_id="BODY-ASTRA",
        agent_id="ASTRA",
        instance_id="ASTRA-I1",
        template_id="adult-template",
        memory_namespace="astra-private",
        canonical_state_reference="astra-state",
    )
    return event, template, aion, astra


def test_validated_genesis_builds_separate_runtime_contexts():
    contexts = build_runtime_contexts(
        *objects(),
        aion_event_lineage_id="AION-EVENTS-1",
        astra_event_lineage_id="ASTRA-EVENTS-1",
    )
    assert contexts.aion.agent_id == "AION"
    assert contexts.astra.agent_id == "ASTRA"
    assert contexts.aion.genesis_root_id == contexts.astra.genesis_root_id == "ROOT-1"
    assert contexts.aion.memory_stream_id != contexts.astra.memory_stream_id
    assert contexts.aion.event_lineage_id != contexts.astra.event_lineage_id
    assert contexts.canonical_effect == "NONE"
    assert contexts.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_shared_event_lineage_is_rejected():
    with pytest.raises(ValidationError):
        build_runtime_contexts(
            *objects(),
            aion_event_lineage_id="SHARED-EVENTS",
            astra_event_lineage_id="SHARED-EVENTS",
        )
