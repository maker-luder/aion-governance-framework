from __future__ import annotations

from aion_astra_twin_embodiment import (
    EmbodimentInstance,
    EmbodimentTemplate,
    SharedGenesisEvent,
    TwinGenesisRuntime,
)


def test_non_3d_runtime_materializes_only_after_validation():
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

    state = TwinGenesisRuntime.instantiate(event, template, aion, astra)

    assert state.runtime_status == "IMPLEMENTED_NON_3D_CANDIDATE"
    assert state.rendering_3d == "DEFERRED"
    assert state.sexual_function == "NOT_IMPLEMENTED"
    assert state.intimate_interaction == "NOT_AUTHORIZED"
    assert state.canonical_effect == "NONE"
    assert state.validation["result"] == "PASS"
