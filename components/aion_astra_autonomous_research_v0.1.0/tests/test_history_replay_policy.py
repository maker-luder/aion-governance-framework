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
    comparison = compare_policies(_tree("train"), _policies())

    breadth = comparison.result_for("breadth")
    depth = comparison.result_for("depth")

    assert breadth.visited_nodes == ("root", "a", "b")
    assert depth.visited_nodes == ("root", "c", "c1")
    assert breadth.best_score == 2
    assert depth.best_score == 5
    assert breadth.cumulative_cost == depth.cumulative_cost == 3


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

    assert select_on_training_history(train).policy_id == "depth"
    assert held_out.result_for("breadth").best_score == 9
    assert held_out.result_for("depth").best_score == 5


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
