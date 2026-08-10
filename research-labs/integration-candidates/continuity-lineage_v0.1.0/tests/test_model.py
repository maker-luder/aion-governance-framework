from continuity_lineage import (
    LineageConfig,
    LineageEvent,
    LineageNode,
    LineageState,
    LineageStateManager,
    LineageType,
    LineageStatus,
)


def node(
    node_id: str = "node-1",
    lineage_type: LineageType = LineageType.TEMPORAL,
    **overrides: str | float | tuple[str, ...] | dict[str, str],
) -> LineageNode:
    values = {
        "node_id": node_id,
        "lineage_type": lineage_type,
        "parent_ids": (),
        "timestamp": "2024-01-01T00:00:00Z",
        "continuity_strength": 0.8,
        "metadata": {},
    }
    values.update(overrides)
    return LineageNode(**values)


def config(**overrides: str | int | float | tuple[LineageType, ...]) -> LineageConfig:
    values = {
        "config_id": "config-1",
        "agent_id": "agent-1",
        "tracked_types": (LineageType.TEMPORAL, LineageType.CAUSAL, LineageType.MEMORY),
        "max_depth": 100,
        "strength_threshold": 0.5,
    }
    values.update(overrides)
    return LineageConfig(**values)


def event(
    event_id: str = "event-1",
    **overrides: str | float | tuple[str, ...],
) -> LineageEvent:
    values = {
        "event_id": event_id,
        "event_type": "CONTINUITY_SHIFT",
        "affected_nodes": ("node-1",),
        "continuity_delta": 0.1,
        "timestamp": "2024-01-01T00:00:00Z",
    }
    values.update(overrides)
    return LineageEvent(**values)


def state(
    state_id: str = "state-1",
    **overrides: str | float | tuple[LineageNode, ...] | LineageConfig | tuple[LineageEvent, ...] | str | int,
) -> LineageState:
    cfg = config()
    values = {
        "state_id": state_id,
        "config": cfg,
        "nodes": (node(),),
        "root_node_id": "node-1",
        "current_head_ids": ("node-1",),
        "overall_continuity": 0.8,
        "branch_count": 0,
        "events": (),
    }
    values.update(overrides)
    return LineageState(**values)


def test_node_validation() -> None:
    try:
        LineageNode(
            node_id="",
            lineage_type=LineageType.TEMPORAL,
            parent_ids=(),
            timestamp="2024-01-01T00:00:00Z",
            continuity_strength=0.5,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "node_id must be non-empty" in str(e)


def test_node_bounds() -> None:
    try:
        LineageNode(
            node_id="n1",
            lineage_type=LineageType.TEMPORAL,
            parent_ids=(),
            timestamp="2024-01-01T00:00:00Z",
            continuity_strength=1.5,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "continuity_strength must be between 0.0 and 1.0" in str(e)


def test_config_validation() -> None:
    try:
        LineageConfig(
            config_id="c1",
            agent_id="a1",
            tracked_types=(),
            max_depth=10,
            strength_threshold=0.5,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "at least one lineage type must be tracked" in str(e)


def test_config_max_depth() -> None:
    try:
        LineageConfig(
            config_id="c1",
            agent_id="a1",
            tracked_types=(LineageType.TEMPORAL,),
            max_depth=0,
            strength_threshold=0.5,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "max_depth must be positive" in str(e)


def test_event_validation() -> None:
    try:
        LineageEvent(
            event_id="",
            event_type="TEST",
            affected_nodes=("n1",),
            continuity_delta=0.5,
            timestamp="2024-01-01T00:00:00Z",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "event_id must be non-empty" in str(e)


def test_event_delta_bounds() -> None:
    try:
        LineageEvent(
            event_id="e1",
            event_type="TEST",
            affected_nodes=("n1",),
            continuity_delta=1.5,
            timestamp="2024-01-01T00:00:00Z",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "continuity_delta must be between -1.0 and 1.0" in str(e)


def test_state_validation() -> None:
    try:
        LineageState(
            state_id="s1",
            config=config(),
            nodes=(node(),),
            root_node_id="node-1",
            current_head_ids=("node-1",),
            overall_continuity=0.8,
            branch_count=0,
            events=(),
            personal_identity_claim="CLAIMED",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "personal identity must remain NOT_ESTABLISHED" in str(e)


def test_state_get_node() -> None:
    n1 = node(node_id="n1")
    n2 = node(node_id="n2")
    st = state(nodes=(n1, n2))
    assert st.get_node("n1") is n1
    assert st.get_node("n3") is None


def test_state_get_children() -> None:
    n1 = node(node_id="n1")
    n2 = node(node_id="n2", parent_ids=("n1",))
    n3 = node(node_id="n3", parent_ids=("n1",))
    st = state(nodes=(n1, n2, n3))
    children = st.get_children("n1")
    assert len(children) == 2
    assert {c.node_id for c in children} == {"n2", "n3"}


def test_state_get_descendants() -> None:
    n1 = node(node_id="n1")
    n2 = node(node_id="n2", parent_ids=("n1",))
    n3 = node(node_id="n3", parent_ids=("n2",))
    st = state(nodes=(n1, n2, n3))
    descendants = st.get_descendants("n1")
    assert len(descendants) == 2
    assert {d.node_id for d in descendants} == {"n2", "n3"}


def test_state_get_nodes_by_type() -> None:
    n1 = node(node_id="n1", lineage_type=LineageType.TEMPORAL)
    n2 = node(node_id="n2", lineage_type=LineageType.CAUSAL)
    n3 = node(node_id="n3", lineage_type=LineageType.TEMPORAL)
    st = state(nodes=(n1, n2, n3))
    temporal = st.get_nodes_by_type(LineageType.TEMPORAL)
    assert len(temporal) == 2


def test_manager_initialize_and_get() -> None:
    mgr = LineageStateManager(deterministic_seed=42)
    s = state()
    mgr.initialize(s)
    assert mgr.get_state() is s
    assert len(mgr.get_history()) == 1
    assert mgr.get_history()[0].transition_type == "INITIALIZE"


def test_manager_transition() -> None:
    mgr = LineageStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    n2 = node(node_id="n2", parent_ids=("node-1",))
    s2 = state(state_id="state-2", nodes=(s1.nodes[0], n2), current_head_ids=("n2",), branch_count=1)
    mgr.transition(s2, transition_type="NODE_ADDED", reason="New temporal node")
    assert mgr.get_state() is s2
    history = mgr.get_history()
    assert len(history) == 2
    assert history[1].transition_type == "NODE_ADDED"


def test_manager_snapshot_and_restore() -> None:
    mgr = LineageStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    snap = mgr.snapshot("test-snap")
    assert snap.snapshot_id == "test-snap"

    n2 = node(node_id="n2", parent_ids=("node-1",))
    s2 = state(state_id="state-2", nodes=(s1.nodes[0], n2))
    mgr.transition(s2)
    restored = mgr.restore("test-snap")
    assert restored is s1


def test_manager_reset() -> None:
    mgr = LineageStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    mgr.snapshot("snap1")
    mgr.reset()
    assert mgr.get_state() is None
    assert len(mgr.get_history()) == 0
    assert len(mgr.list_snapshots()) == 0


def test_manager_disable_enable() -> None:
    mgr = LineageStateManager()
    assert mgr.is_enabled() is True
    mgr.disable()
    assert mgr.is_enabled() is False
    try:
        mgr.initialize(state())
        assert False, "Should have raised RuntimeError"
    except RuntimeError:
        pass
    mgr.enable()
    assert mgr.is_enabled() is True
    mgr.initialize(state())


def test_manager_ablate_type() -> None:
    mgr = LineageStateManager()
    n1 = node(node_id="n1", lineage_type=LineageType.TEMPORAL)
    n2 = node(node_id="n2", lineage_type=LineageType.CAUSAL)
    n3 = node(node_id="n3", lineage_type=LineageType.MEMORY)
    s = state(nodes=(n1, n2, n3))
    mgr.initialize(s)
    mgr.ablate("CAUSAL")
    new_state = mgr.get_state()
    assert new_state is not None
    types = {n.lineage_type for n in new_state.nodes}
    assert LineageType.TEMPORAL in types
    assert LineageType.MEMORY in types
    assert LineageType.CAUSAL not in types


def test_manager_ablate_all() -> None:
    mgr = LineageStateManager()
    s = state()
    mgr.initialize(s)
    mgr.ablate()
    assert mgr.is_enabled() is False