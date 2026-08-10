#!/usr/bin/env python3
"""Demo for continuity-lineage module."""

from continuity_lineage import (
    LineageConfig,
    LineageEvent,
    LineageNode,
    LineageState,
    LineageStateManager,
    LineageType,
)


def build_initial_config() -> LineageConfig:
    return LineageConfig(
        config_id="lineage-config-001",
        agent_id="aion-research-agent",
        tracked_types=(
            LineageType.TEMPORAL,
            LineageType.CAUSAL,
            LineageType.NARRATIVE,
            LineageType.EMBODIMENT,
            LineageType.MEMORY,
            LineageType.SOCIAL,
            LineageType.FUNCTIONAL,
        ),
        max_depth=1000,
        strength_threshold=0.5,
    )


def build_initial_state(config: LineageConfig) -> LineageState:
    root = LineageNode(
        node_id="genesis-001",
        lineage_type=LineageType.TEMPORAL,
        parent_ids=(),
        timestamp="2024-01-01T00:00:00Z",
        continuity_strength=1.0,
        metadata={"origin": "initialization"},
    )
    return LineageState(
        state_id="initial-lineage-state-001",
        config=config,
        nodes=(root,),
        root_node_id="genesis-001",
        current_head_ids=("genesis-001",),
        overall_continuity=1.0,
        branch_count=0,
        events=(),
    )


def demo() -> None:
    print("=" * 60)
    print("CONTINUITY LINEAGE DEMO")
    print("=" * 60)

    mgr = LineageStateManager(deterministic_seed=12345)

    print("\n1. Building configuration...")
    config = build_initial_config()
    print(f"   Config ID: {config.config_id}")
    print(f"   Agent ID: {config.agent_id}")
    print(f"   Tracked types: {[t.value for t in config.tracked_types]}")
    print(f"   Max depth: {config.max_depth}")
    print(f"   Strength threshold: {config.strength_threshold}")

    print("\n2. Initializing state (genesis node)...")
    initial = build_initial_state(config)
    mgr.initialize(initial)
    print(f"   State ID: {mgr.get_state().state_id}")
    print(f"   Nodes: {len(mgr.get_state().nodes)}")
    print(f"   Root: {mgr.get_state().root_node_id}")
    print(f"   Heads: {mgr.get_state().current_head_ids}")
    print(f"   Overall continuity: {mgr.get_state().overall_continuity}")
    print(f"   Branch count: {mgr.get_state().branch_count}")

    print("\n3. Creating snapshot...")
    snap = mgr.snapshot("demo-snapshot-1")
    print(f"   Snapshot ID: {snap.snapshot_id}")

    print("\n4. Adding temporal continuation node...")
    temporal_node = LineageNode(
        node_id="temporal-002",
        lineage_type=LineageType.TEMPORAL,
        parent_ids=("genesis-001",),
        timestamp="2024-01-01T00:01:00Z",
        continuity_strength=0.95,
        metadata={"event": "time_step"},
    )
    causal_node = LineageNode(
        node_id="causal-001",
        lineage_type=LineageType.CAUSAL,
        parent_ids=("genesis-001",),
        timestamp="2024-01-01T00:01:00Z",
        continuity_strength=0.90,
        metadata={"event": "decision_consequence"},
    )
    event1 = LineageEvent(
        event_id="event-001",
        event_type="TEMPORAL_CONTINUATION",
        affected_nodes=("temporal-002", "causal-001"),
        continuity_delta=0.05,
        timestamp="2024-01-01T00:01:00Z",
    )
    state2 = LineageState(
        state_id="extended-lineage-state-002",
        config=config,
        nodes=initial.nodes + (temporal_node, causal_node),
        root_node_id="genesis-001",
        current_head_ids=("temporal-002", "causal-001"),
        overall_continuity=0.925,
        branch_count=1,
        events=(event1,),
    )
    mgr.transition(state2, transition_type="NODES_ADDED", reason="Temporal and causal continuation")
    print(f"   New state ID: {mgr.get_state().state_id}")
    print(f"   Nodes: {len(mgr.get_state().nodes)}")
    print(f"   Heads: {mgr.get_state().current_head_ids}")
    print(f"   Overall continuity: {mgr.get_state().overall_continuity}")
    print(f"   Branch count: {mgr.get_state().branch_count}")

    print("\n5. Adding narrative branch (branching)...")
    narrative_a = LineageNode(
        node_id="narrative-001a",
        lineage_type=LineageType.NARRATIVE,
        parent_ids=("causal-001",),
        timestamp="2024-01-01T00:02:00Z",
        continuity_strength=0.85,
        metadata={"narrative": "path_a"},
    )
    narrative_b = LineageNode(
        node_id="narrative-001b",
        lineage_type=LineageType.NARRATIVE,
        parent_ids=("causal-001",),
        timestamp="2024-01-01T00:02:00Z",
        continuity_strength=0.80,
        metadata={"narrative": "path_b"},
    )
    event2 = LineageEvent(
        event_id="event-002",
        event_type="NARRATIVE_BRANCHING",
        affected_nodes=("narrative-001a", "narrative-001b"),
        continuity_delta=-0.05,
        timestamp="2024-01-01T00:02:00Z",
    )
    state3 = LineageState(
        state_id="branched-lineage-state-003",
        config=config,
        nodes=state2.nodes + (narrative_a, narrative_b),
        root_node_id="genesis-001",
        current_head_ids=("temporal-002", "narrative-001a", "narrative-001b"),
        overall_continuity=0.875,
        branch_count=2,
        events=state2.events + (event2,),
    )
    mgr.transition(state3, transition_type="BRANCHING", reason="Narrative divergence")
    print(f"   New state ID: {mgr.get_state().state_id}")
    print(f"   Nodes: {len(mgr.get_state().nodes)}")
    print(f"   Heads: {mgr.get_state().current_head_ids}")
    print(f"   Branch count: {mgr.get_state().branch_count}")

    print("\n6. Adding embodiment continuity...")
    embodiment_node = LineageNode(
        node_id="embodiment-001",
        lineage_type=LineageType.EMBODIMENT,
        parent_ids=("temporal-002",),
        timestamp="2024-01-01T00:03:00Z",
        continuity_strength=0.88,
        metadata={"embodiment_version": "v1"},
    )
    event3 = LineageEvent(
        event_id="event-003",
        event_type="EMBODIMENT_CONTINUITY",
        affected_nodes=("embodiment-001",),
        continuity_delta=0.02,
        timestamp="2024-01-01T00:03:00Z",
    )
    state4 = LineageState(
        state_id="embodied-lineage-state-004",
        config=config,
        nodes=state3.nodes + (embodiment_node,),
        root_node_id="genesis-001",
        current_head_ids=("narrative-001a", "narrative-001b", "embodiment-001"),
        overall_continuity=0.876,
        branch_count=2,
        events=state3.events + (event3,),
    )
    mgr.transition(state4, transition_type="NODE_ADDED", reason="Embodiment continuity established")
    print(f"   New state ID: {mgr.get_state().state_id}")
    print(f"   Nodes: {len(mgr.get_state().nodes)}")
    print(f"   Embodiment nodes: {len(mgr.get_state().get_nodes_by_type(LineageType.EMBODIMENT))}")

    print("\n7. Querying lineage structure...")
    st = mgr.get_state()
    print(f"   Root node: {st.get_node(st.root_node_id).node_id}")
    print(f"   Children of genesis: {[c.node_id for c in st.get_children('genesis-001')]}")
    print(f"   Descendants of causal-001: {[d.node_id for d in st.get_descendants('causal-001')]}")
    print(f"   Temporal nodes: {[n.node_id for n in st.get_nodes_by_type(LineageType.TEMPORAL)]}")
    print(f"   Narrative nodes: {[n.node_id for n in st.get_nodes_by_type(LineageType.NARRATIVE)]}")

    print("\n8. History trace:")
    for i, t in enumerate(mgr.get_history()):
        print(f"   {i}: {t.transition_type} | {t.from_state_id} -> {t.to_state_id} | {t.reason}")

    print("\n9. Restoring from snapshot...")
    restored = mgr.restore("demo-snapshot-1")
    print(f"   Restored state ID: {restored.state_id}")
    print(f"   Nodes: {len(restored.nodes)}")
    print(f"   Branch count: {restored.branch_count}")

    print("\n10. Ablating NARRATIVE lineage type...")
    mgr.ablate("NARRATIVE")
    ablated = mgr.get_state()
    types = {n.lineage_type for n in ablated.nodes}
    print(f"   Remaining types: {[t.value for t in types]}")
    assert LineageType.NARRATIVE not in types

    print("\n11. Disabling module...")
    mgr.disable()
    print(f"   Enabled: {mgr.is_enabled()}")
    try:
        mgr.initialize(build_initial_state(build_initial_config()))
    except RuntimeError as e:
        print(f"   Expected error: {e}")

    print("\n12. Re-enabling and final reset...")
    mgr.enable()
    mgr.reset()
    print(f"   State after reset: {mgr.get_state()}")
    print(f"   History length: {len(mgr.get_history())}")

    print("\n" + "=" * 60)
    print("DEMO COMPLETE - Module operates in isolation")
    print("Canonical effect: NONE")
    print("Personal identity claim: NOT_ESTABLISHED")
    print("Consciousness continuity claim: NOT_ESTABLISHED")
    print("Narrative unity claim: NOT_ESTABLISHED")
    print("=" * 60)


if __name__ == "__main__":
    demo()