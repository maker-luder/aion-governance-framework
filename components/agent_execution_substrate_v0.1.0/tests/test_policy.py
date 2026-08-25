from __future__ import annotations

from aion_astra_agent_substrate import (
    Capability,
    Decision,
    PolicyRequest,
    RuntimeBinding,
    evaluate,
)


def _binding() -> RuntimeBinding:
    return RuntimeBinding.from_runtime_context(
        {
            "agent_id": "AION",
            "runtime_instance_id": "AION-I-001",
            "memory_stream_id": "AION-MEM-001",
            "event_lineage_id": "AION-EVT-001",
            "canonical_state_reference": "AION-CANONICAL",
            "genesis_root_id": "GENESIS-001",
        },
        substrate_id="substrate",
        session_id="session-001",
    )


def test_observation_capability_is_allowed_without_mutation_authority() -> None:
    result = evaluate(PolicyRequest(_binding(), Capability.TRAJECTORY_EXPORT))
    assert result.decision is Decision.ALLOW
    assert result.mutation_performed is False
    assert result.canonical_effect == "NONE"


def test_mutating_capability_requires_owner_approval_and_reference() -> None:
    result = evaluate(PolicyRequest(_binding(), Capability.TOOL_INVOKE))
    assert result.decision is Decision.HOLD
    assert "explicit Owner approval" in " ".join(result.reasons)
    assert "authority_reference" in " ".join(result.reasons)


def test_mutating_capability_can_be_admitted_as_abstract_bounded_permission() -> None:
    result = evaluate(
        PolicyRequest(
            _binding(),
            Capability.TOOL_INVOKE,
            owner_approved=True,
            authority_reference="approval:test",
        )
    )
    assert result.decision is Decision.ALLOW
    assert result.mutation_performed is False


def test_network_access_always_holds_in_v0_1_0() -> None:
    result = evaluate(
        PolicyRequest(
            _binding(),
            Capability.MODEL_ROUTE,
            owner_approved=True,
            authority_reference="approval:test",
            network_access=True,
        )
    )
    assert result.decision is Decision.HOLD
    assert "network access" in " ".join(result.reasons)


def test_deployment_and_canonical_effect_fail_closed() -> None:
    result = evaluate(
        PolicyRequest(
            _binding(),
            Capability.STORAGE_READ,
            deployment=True,
            canonical_effect="PROMOTE",
        )
    )
    assert result.decision is Decision.HOLD
    joined = " ".join(result.reasons)
    assert "deployment" in joined
    assert "canonical effects" in joined


def test_plugin_generated_self_composition_does_not_self_authorize() -> None:
    result = evaluate(
        PolicyRequest(
            _binding(),
            Capability.PLUGIN_MOUNT,
            self_requested=True,
            plugin_generated=True,
        )
    )
    assert result.decision is Decision.HOLD
    assert any("self-composition" in reason for reason in result.reasons)
