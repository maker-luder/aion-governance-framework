import pytest

from aion_astra_autonomous_research.history_replay_policy import (
    DiscoveryNode,
    DiscoveryTree,
    ReplayPolicy,
    ReplayStrategy,
    compare_policies,
    replay,
    select_on_training_history,
)


def _tree(tree_id: str, *, b_score: int = 2, c1_score: int = 5) -> DiscoveryTree:
    return DiscoveryTree(
        tree_id=tree_id,
        nodes=(
            DiscoveryNode("root", None, "start", 0),
            DiscoveryNode("a", "root", "branch-a", 1),
            DiscoveryNode("b", "root", "branch-b", b_score),
            DiscoveryNode("c", "root", "branch-c", 3),
            DiscoveryNode("a1", "a", "refine-a", 10, terminal=True),
            DiscoveryNode("b1", "b", "refine-b", 4, terminal=True),
            DiscoveryNode("c1", "c", "refine-c", c1_score, terminal=True),
        ),
    )


def _policies() -> tuple[ReplayPolicy, ReplayPolicy]:
    return (
        ReplayPolicy("breadth", ReplayStrategy.BREADTH_FIRST, max_visits=3),
        ReplayPolicy("depth", ReplayStrategy.DEPTH_FIRST, max_visits=3),
    )


def test_same_history_different_policy_changes_trajectory_and_score() -> None:
    tree = _tree("train")
    comparison = compare_policies(tree, _policies())

    breadth = comparison.result_for("breadth")
    depth = comparison.result_for("depth")

    assert comparison.history_sha256 == tree.history_sha256
    assert comparison.max_visits == 3
    assert breadth.history_sha256 == depth.history_sha256 == tree.history_sha256
    assert breadth.visited_nodes == ("root", "a", "b")
    assert depth.visited_nodes == ("root", "c", "c1")
    assert breadth.best_score == 2
    assert depth.best_score == 5
    assert breadth.cumulative_cost == depth.cumulative_cost == 3


def test_history_fingerprint_is_content_bound_not_label_bound() -> None:
    first = _tree("first")
    relabeled = _tree("relabeled")
    changed = _tree("changed", b_score=99)

    assert first.history_sha256 == relabeled.history_sha256
    assert first.history_sha256 != changed.history_sha256


def test_history_fingerprint_binds_recorded_node_order() -> None:
    baseline = _tree("baseline")
    reordered = DiscoveryTree(
        tree_id="reordered",
        nodes=(
            baseline.nodes[0],
            baseline.nodes[3],
            baseline.nodes[2],
            baseline.nodes[1],
            baseline.nodes[6],
            baseline.nodes[5],
            baseline.nodes[4],
        ),
    )

    assert baseline.history_sha256 != reordered.history_sha256


def test_unvisited_outcome_cannot_change_policy_path() -> None:
    baseline = _tree("baseline")
    altered = DiscoveryTree(
        tree_id="altered",
        nodes=tuple(
            DiscoveryNode(
                node.node_id,
                node.parent_id,
                node.action_id,
                999 if node.node_id == "a1" else node.score,
                node.execution_cost,
                node.terminal,
            )
            for node in baseline.nodes
        ),
    )
    depth = ReplayPolicy("depth", ReplayStrategy.DEPTH_FIRST, max_visits=3)

    assert baseline.history_sha256 != altered.history_sha256
    assert replay(baseline, depth).visited_nodes == replay(altered, depth).visited_nodes


def test_patience_can_stop_replay_without_exhausting_tree() -> None:
    policy = ReplayPolicy(
        "breadth-patient",
        ReplayStrategy.BREADTH_FIRST,
        max_visits=7,
        patience=1,
    )

    result = replay(_tree("patience", b_score=0), policy)

    assert result.visited_nodes == ("root", "a", "b")
    assert result.terminal_reason == "PATIENCE_EXHAUSTED"


def test_training_winner_does_not_imply_held_out_winner() -> None:
    breadth, depth = _policies()
    train = compare_policies(_tree("train"), (breadth, depth))
    held_out = compare_policies(
        _tree("held-out", b_score=9, c1_score=5),
        (breadth, depth),
    )

    assert train.history_sha256 != held_out.history_sha256
    assert select_on_training_history(train).policy_id == "depth"
    assert held_out.result_for("breadth").best_score == 9
    assert held_out.result_for("depth").best_score == 5


def test_compare_rejects_mismatched_visit_budgets() -> None:
    with pytest.raises(ValueError, match="share max_visits"):
        compare_policies(
            _tree("budget-mismatch"),
            (
                ReplayPolicy("short", ReplayStrategy.BREADTH_FIRST, max_visits=2),
                ReplayPolicy("long", ReplayStrategy.DEPTH_FIRST, max_visits=3),
            ),
        )


def test_tree_rejects_missing_parent() -> None:
    with pytest.raises(ValueError, match="missing parent"):
        DiscoveryTree(
            tree_id="bad-parent",
            nodes=(
                DiscoveryNode("root", None, "start", 0),
                DiscoveryNode("orphan", "missing", "bad", 1),
            ),
        )


def test_tree_rejects_multiple_roots() -> None:
    with pytest.raises(ValueError, match="exactly one root"):
        DiscoveryTree(
            tree_id="bad-roots",
            nodes=(
                DiscoveryNode("root-a", None, "a", 0),
                DiscoveryNode("root-b", None, "b", 0),
            ),
        )


def test_tree_rejects_children_below_terminal_node() -> None:
    with pytest.raises(ValueError, match="terminal nodes cannot have children"):
        DiscoveryTree(
            tree_id="bad-terminal",
            nodes=(
                DiscoveryNode("root", None, "start", 0),
                DiscoveryNode("terminal", "root", "stop", 1, terminal=True),
                DiscoveryNode("impossible-child", "terminal", "continue", 2),
            ),
        )
